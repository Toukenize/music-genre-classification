from sqlalchemy import create_engine

from .config import settings

pg_client = create_engine(
    "postgresql://" + settings.POSTGRES_URI
)
pg_client.connect()
