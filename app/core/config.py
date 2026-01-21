from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings managed by Pydantic.
    
    This class loads configuration from environment variables and/or a .env file.
    """
    
    # Database connection string (PostgreSQL)
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")

    # Security settings
    SECRET_KEY: str = Field(..., validation_alias="SECRET_KEY")
    ALGORITHM: str = Field("HS256", validation_alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings() # type: ignore