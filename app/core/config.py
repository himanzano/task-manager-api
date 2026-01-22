from typing import Literal
from pydantic import Field
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

    # Security settings
    SECRET_KEY: str = Field(..., validation_alias="SECRET_KEY")
    ALGORITHM: str = Field("HS256", validation_alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS")

    # Environment indicator
    ENV: str = Field("production", validation_alias="ENV")

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore",
        # env_ignore_missing=True might be causing type issues in some editors
        # We can safely remove it if we rely on 'extra="ignore"' or standard behavior
    )

settings = Settings() # type: ignore