import logging
import re
from typing import List, Tuple

import pandas as pd
from unidecode import unidecode

from ..errors import DataSchemaException
from ..utils import format_str
from .constants import stopwords
from .schema.input_data import df_schema


def count_na_rows_and_drop(
        df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:

    num_rows_before = len(df)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    num_rows_after = len(df)

    na_rows = num_rows_before - num_rows_after

    return df, na_rows


def process_data(df: pd.DataFrame) -> pd.DataFrame:

    # Generate new feature
    df['time_sig_mt4'] = (df['time_signature'] > 4).astype(float)

    # Combine key & mode, and one hot encode them
    df[['key', 'mode']] = (
        df[['key', 'mode']]
        .applymap(lambda x: f'{int(x):02d}')
    )

    df['key_mode'] = (
        df[['key', 'mode']]
        .apply(lambda x: '|'.join(x), axis=1)
    )

    key_mode_cols = sorted(df['key_mode'].unique())

    for col in key_mode_cols:
        df[col] = (df['key_mode'] == col).astype(float)

    df['processed_tags'] = (
        df['tags'].apply(lambda x: text_processing(x, stopwords))
    )

    return df


def text_processing(txt: str, stopwords: List = None) -> str:

    # Lowercasing - works on accented characters too
    txt = txt.lower()

    # Remove bracket & content
    txt = re.sub('\(.*?\)', ' ', txt)

    # Convert accented characters to their closest ASCII character
    # e.g. Gönül -> Gonul
    txt = unidecode(txt)

    # Remove anything that isn't a-z
    txt = re.sub('[^a-z ]', ' ', txt)

    # Standardize spacing
    txt = re.sub('\s+', ' ', txt).strip()

    if stopwords is not None:
        # Remove stopwords
        sw_pattern = '\\b(' + '|'.join(stopwords) + ')\\b'
        txt = re.sub(sw_pattern, ' ', txt)

        # Standardize spacing again
        txt = re.sub('\s+', ' ', txt).strip()

    return txt


def validate_df(df: pd.DataFrame) -> pd.DataFrame:

    try:
        df = df_schema.validate(df)
        return df

    except Exception as e:
        logging.error(e)
        message = format_str(
            """
            Input data did not pass validation check. Make sure
            all the required data fields are present and are of the
            right data type.
            """
        ) + ' Stack trace : ' + str(e)
        raise DataSchemaException(message)
