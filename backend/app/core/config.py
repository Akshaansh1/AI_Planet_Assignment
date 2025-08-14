from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the application.
    Reads environment variables from a .env file.
    """
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str
    SERPAPI_API_KEY: str
    CHROMA_HOST: str
    CHROMA_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()
