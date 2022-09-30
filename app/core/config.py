import os
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
from sqlalchemy.engine.url import URL


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    PROJECT_NAME: str = "dream-x-crud-api"
    SERVER_NAME: str = "dream-x-crud-api"
    SERVER_HOST: AnyHttpUrl = "http://0.0.0.0"

    ENVIRONMENT: str = os.environ["ENVIRONMENT"]

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:8080",
        "https://localhost",
        "https://localhost:8080",
    ]

    DB_POSTGRES_HOST: str = os.environ["DB_POSTGRES_HOST"]
    DB_POSTGRES_USER: str = os.environ["DB_POSTGRES_USER"]
    DB_POSTGRESS_PASSWORD: str = os.environ["DB_POSTGRESS_PASSWORD"]
    DB_POSTGRES_PORT: str = os.environ["DB_POSTGRES_PORT"]
    DB_POSTGRES_DATABASE: str = os.environ["DB_POSTGRES_DATABASE"]
    SQLALCHEMY_POSTGRES_URI: Optional[str] = None

    @validator("SQLALCHEMY_POSTGRES_URI", pre=True, check_fields=False)
    def create_postgres_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        print("create_postgres_uri")
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=values.get("DB_POSTGRES_HOST"),
            port=f"{values.get('DB_POSTGRES_PORT')}",
            user=values.get("DB_POSTGRES_USER"),
            password=values.get("DB_POSTGRESS_PASSWORD"),
            path=f"/{values.get('DB_POSTGRES_DATABASE') or ''}",
        )


settings = Settings()