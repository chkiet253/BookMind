from pydantic_settings import BaseSettings, SettingConfigDict

class Setting(BaseSettings):
    model_config = SettingConfigDict(
        env_file =".env",
        env_file_encoding ="utf-8",
        extra='ignore'
    )
    ENVIRONMENT: str = "local"
    
    DATABASE_URL: str
    
    QDRANT_URL: str = "http://localhost:6340"
    QDRANT_COLLECTION_NAME: str = "books_collection"
    
    # LLM Config
    LLM_API_KEY: str

settings = Setting()