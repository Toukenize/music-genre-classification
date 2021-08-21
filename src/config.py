import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

import src

IS_LOCAL = os.getenv('IS_LOCAL', True)

if IS_LOCAL:
    load_dotenv('../env/api-service.env')


class Settings(BaseSettings):
    API_NAME: str = "Music Genre Services API"
    API_PREFIX: str = '/api/v1'
    API_VERSION: str = src.__version__
    PORT: int = 5000
    POSTGRES_URI: str
    MODEL_PATH: str
    CLIENT_SECRET: str
    CLIENT_ID: str


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
