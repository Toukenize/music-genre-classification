from fastapi import APIRouter, File, Header, UploadFile, status

from ..classifier.predict import ID2LABEL, MODEL_DICT, predict_ensemble
from ..config import settings
from ..db import pg_client
from ..db_utils import upsert_df_to_db
from ..utils import check_auth_headers, read_csv_from_stream
from .constants import db_cols_dict, db_tab_name, upsert_col
from .preprocess import count_na_rows_and_drop, process_data
from .schema.data import df_schema
from .schema.response import Model

api_router = APIRouter(
    prefix=settings.API_PREFIX
)


@api_router.post('/predict-batch', response_model=Model)
def predict_batch(
        csv_file: UploadFile = File(...),
        client_id: str = Header(...),
        client_secret: str = Header(...)
):
    check_auth_headers(client_id, client_secret)

    df = read_csv_from_stream(csv_file)

    total_rows_raw = len(df)

    df, na_rows = count_na_rows_and_drop(df)

    df = df_schema.validate(df)

    df = process_data(df)

    preds = predict_ensemble(df, MODEL_DICT, ID2LABEL)

    df['preds'] = preds

    df.rename(columns=db_cols_dict, inplace=True)

    upsert_df_to_db(
        pg_client, df[db_cols_dict.values()], upsert_col, db_tab_name)

    return {
        "status": "success",
        "status_code": status.HTTP_200_OK,
        "info": {
            "total_rows_uploaded": total_rows_raw,
            "total_rows_w_na": na_rows,
            "total_rows_added_to_db": len(df)
        }
    }
