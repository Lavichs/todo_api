from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from authx import AuthX, AuthXConfig

authxConfig = AuthXConfig()
authxConfig.JWT_ALGORITHM = "HS256"
authxConfig.JWT_SECRET_KEY = "SECRET_KEY"


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    JWT_EXPIRATION_DELTA: int
    JWT_SECRET_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        # DSN
        # postgresql+asyncpg://postgres:postgres@localhost:5432/db
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
