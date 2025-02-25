from typing import ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict as ConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = ConfigDict(env_file='../../.env', env_file_encoding='utf-8')

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DB_DRIVER_NAME: ClassVar[str] = 'postgresql+psycopg2'

settings = Settings()
