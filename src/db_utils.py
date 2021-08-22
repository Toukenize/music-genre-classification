import logging

import pandas as pd
from sqlalchemy import engine
from sqlalchemy.sql import text

from .errors import PostgresConnectionException


def upsert_df_to_db(
        engine: engine,
        df: pd.DataFrame,
        upsert_col: str,
        table_name: str):

    if len(df) == 0:
        logging.info(
            f"Tried to upsert a empty dataframe of shape: {df.shape}")
        return

    with engine.connect() as conn:

        try:
            trans = conn.begin()
            delete_query = text(f"""
            DELETE FROM {table_name} WHERE {upsert_col} IN :list_to_update
            """)
            conn.execute(
                delete_query, list_to_update=tuple(df[upsert_col].tolist())
            )
            df.to_sql(table_name, conn, if_exists="append", index=False)
            trans.commit()

        except Exception as e:
            trans.rollback()
            logging.error(e)
            raise PostgresConnectionException(
                f"Failed to upsert data for {table_name} table") from e
    return
