import logging
import textwrap
from io import StringIO

import pandas as pd
from fastapi import File

from config import settings
from errors import FileTypeException, UnauthorizedException


def check_auth_headers(id, secret):
    if id != settings.CLIENT_ID or secret != settings.CLIENT_SECRET:
        message = "Unauthorized. Did you pass in the correct headers?"
        logging.error(message)
        raise UnauthorizedException(message)


def read_csv_from_stream(csv_file: File):
    if csv_file.filename.endswith('.csv'):

        # https://stackoverflow.com/a/67330875/10841164
        df = pd.read_csv(
            StringIO(str(csv_file.file.read(), 'utf-8')), encoding='utf-8')

        return df
    else:
        message = format_str(f"""
        The extension of input file `{csv_file.filename}` is
        not supported. Only `.csv` files can be processed.
        """)
        logging.error(message)
        raise FileTypeException(message)


def format_str(multiline_str: str):
    formatted = (
        textwrap
        .dedent(multiline_str)
        .replace('\n', ' ')
        .strip()
    )
    return formatted
