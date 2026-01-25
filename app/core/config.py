import os
from typing import Literal, Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings managed by Pydantic.

    This class loads configuration from environment variables.
    A .env file is loaded only if present (useful for local development).
    """

    # Database connection string (PostgreSQL)
    # Must include SSL mode if required by Supabase (e.g. ?sslmode=require)
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")
    SSL_MODE: Literal[
        "disable", "allow", "prefer", "require", "verify-ca", "verify-full"
    ] = Field("prefer", validation_alias="SSL_MODE")

    # DB Pool Settings (important for Cloud Run)
    DB_POOL_SIZE: int = Field(5, validation_alias="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(10, validation_alias="DB_MAX_OVERFLOW")

    # Security settings
    SECRET_KEY: str = Field(..., validation_alias="SECRET_KEY")
    ALGORITHM: str = Field("HS256", validation_alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        7, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS"
    )

    # Environment indicator
    ENV: str = Field("production", validation_alias="ENV")

    # CORS settings - Comma separated string in env, list in python
    BACKEND_CORS_ORIGINS: list[str] | str = Field(
        ["*"], validation_alias="BACKEND_CORS_ORIGINS"
    )

    @field_validator(
        "SSL_MODE", "DATABASE_URL", "SECRET_KEY", "ALGORITHM", "ENV", mode="before"
    )
    @classmethod
    def strip_quotes(cls, v: Any) -> Any:
        if isinstance(v, str):
            return v.strip('"').strip("'")
        return v

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> Any:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        env_file={
            "production": ".env.prod",
            "staging": ".env.stage",
        }.get(os.getenv("ENV"), ".env.dev"),
        extra="ignore",
    )


settings = Settings()  # type: ignore
