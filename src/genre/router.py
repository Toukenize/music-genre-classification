import logging

import pandas as pd
from fastapi import APIRouter, Header, status
from fastapi.param_functions import Depends
from sqlalchemy.sql import text

from ..config import settings
from ..db import pg_client
from ..errors import PostgresConnectionException
from ..utils import check_auth_headers
from .schema import genre_list, input_data, title_list

api_router = APIRouter(
    prefix=settings.API_PREFIX
)


@api_router.get('/genre/title-list', response_model=title_list.Model)
def title_list_api(
        args: input_data.TitleListArgs = Depends(),
        client_id: str = Header(...),
        client_secret: str = Header(...)
):
    """
    **Description:**

    Get the list of titles that is classified under the selected genre.

    **Request Body**
    - **genre**: The genre of interest. Must be one of ["metal", "folk",
        "jazz and blues", "soul and reggae", "classic pop and rock", "punk",
        "dance and electronica", "pop"].

    **Response Structure**
    - **genre** - The genre queried.
    - **titles** - The list of sorted titles associated with the queried genre.
    """

    check_auth_headers(client_id, client_secret)

    try:
        df = pd.read_sql(
            text(
                """
                SELECT title
                FROM music_genre_tab
                WHERE genre = :genre
                ORDER BY title
                """
            ),
            params={'genre': args.genre.value},
            con=pg_client
        )

        print(df)
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "genre": args.genre.value,
            "titles": df['title'].tolist()
        }

    except Exception as e:
        logging.error(e)
        raise PostgresConnectionException("Unable to execute query." + str(e))


@ api_router.get('/genre/list', response_model=genre_list.Model)
def genre_list_api(
        client_id: str = Header(...),
        client_secret: str = Header(...)
):
    """
    **Description:**

    Get the list of genres available in the database.

    **Response Structure**
    - **genre** - The full list of genre available in the database.
    """

    check_auth_headers(client_id, client_secret)

    try:
        df = pd.read_sql(
            """SELECT DISTINCT(genre) FROM music_genre_tab""",
            pg_client)
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "genre": df['genre'].tolist()
        }

    except Exception as e:
        logging.error(e)
        raise PostgresConnectionException("Unable to execute query." + str(e))
