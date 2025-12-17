from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import List

ROOT_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env'
    )

    PROJECT_NAME: str
    API_V1: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    #GOOGLE
    OAUTHLIB_INSECURE_TRANSPORT: str #alternatif https required untuk google oaut2
    GOOGLE_CLIENT_SECRET_PATH: str
    GOOGLE_SCOPES: List[str]
    GOOGLE_REDIRECT_URI: str

    # REDIS
    REDIS_URI: str

    #POSTGRESQL
    DATABASE_URL: str

settings = Settings()