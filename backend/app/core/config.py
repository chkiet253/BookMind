from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file =".env",
        env_file_encoding ="utf-8",
        extra='ignore'
    )

    APP_NAME: str = "BookMind"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    ENVIRONMENT: str = "local"
    
    DATABASE_URL: str
    
    QDRANT_URL: str = "http://localhost:6340"
    QDRANT_COLLECTION_NAME: str = "books_collection"
    
    # LLM Config
    LLM_API_KEY: str | None = None

settings = Settings()