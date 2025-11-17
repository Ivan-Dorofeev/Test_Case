import os
from typing import List, Optional

from pydantic_settings import BaseSettings


class S3Config:
    """Конфигурация S3 хранилища"""

    ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
    BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "documents")
    SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    REGION: str = os.getenv("MINIO_REGION", "us-east-1")


class Settings(BaseSettings):
    PROJECT_NAME: str = "БИРЖА"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    TEST_DATABASE_URL: Optional[str] = os.getenv("TEST_DATABASE_URL")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    S3_CONFIG: S3Config = S3Config()

    EMAIL_HOST: str = "smtp.yandex.ru"
    EMAIL_PORT: int = 587
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str = "noreply@example.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
