from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings managed by Pydantic.
    
    This class loads configuration from environment variables and/or a .env file.
    """
    
    # Database connection string (PostgreSQL)
    # Format: postgresql://user:password@host:port/dbname
    # Field(...) indicates this is a required field, but handled by Pydantic's env loading
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")

    # Configuration for loading settings
    # env_file specifies the file to read environment variables from
    # extra="ignore" allows extra environment variables without raising errors
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings() # type: ignore
