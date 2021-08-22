from fastapi import APIRouter, File, Header, UploadFile, status

from ..classifier.predict import ID2LABEL, MODEL_DICT, predict_ensemble
from ..config import settings
from ..db import pg_client
from ..db_utils import upsert_df_to_db
from ..utils import check_auth_headers, read_csv_from_stream
from .constants import db_cols_dict, db_tab_name, upsert_col
from .preprocess import count_na_rows_and_drop, process_data, validate_df
from .schema.predict_batch import Model

api_router = APIRouter(
    prefix=settings.API_PREFIX
)


@api_router.post('/predict-batch', response_model=Model)
def predict_batch_api(
        csv_file: UploadFile = File(...),
        client_id: str = Header(...),
        client_secret: str = Header(...)
):
    """
    **Description:**

    Given a csv file, predict the data rows' genre and upload the predictions
    to postgres database.

    **Request Body**
    - **csv_file**: Data file containing all required columns, in the correct
        data format

    **Response Structure**
    - **info**
        - **total_rows_uploaded** - The total number of rows detected in the
            uploaded csv.
        - **total_rows_w_na** - The number of rows with at least 1 NA field,
            which are dropped before the prediction.
        - **total_rows_added_to_db** - The total number of rows upserted to
            database. (Note that entries which already exist in the database
            will be updated).

    **Backend Logic**
    1. Validate dataframe (field, order, data type).
    2. Process dataframe & generate features (including the use of individual
        model's vectorizer).
    3. Generate predictions followed by simple averaging of the logits across
        models (lightgbm with the same parameter, trained using different
        fold of data).
    4. Predictions (trackid, title and predicted genre) are upserted to
        database.
    """
    check_auth_headers(client_id, client_secret)

    df = read_csv_from_stream(csv_file)

    total_rows_raw = len(df)

    df, na_rows = count_na_rows_and_drop(df)

    df = validate_df(df)

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
