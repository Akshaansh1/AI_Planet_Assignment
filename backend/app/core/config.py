import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the application.
    Reads environment variables from a .env file.
    """
    # Database Settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # API Key Settings
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str
    SERPAPI_API_KEY: str

    # We no longer need CHROMA_HOST and CHROMA_PORT
    # because we are using a local, persistent ChromaDB client.

    class Config:
        env_file = ".env"

settings = Settings()
