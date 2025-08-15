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
    MISTRAL_API_KEY: str
    SERPAPI_API_KEY: str

    @property
    def cleaned_openai_key(self) -> str:
        return self.OPENAI_API_KEY.strip() if self.OPENAI_API_KEY else ""

    @property
    def cleaned_gemini_key(self) -> str:
        key = self.GEMINI_API_KEY.strip() if self.GEMINI_API_KEY else ""
        if key.startswith("AIzaSy"):
            raise ValueError(
                "You are using a Google Cloud API key. For Gemini, you need a Google AI Studio API key instead.\n"
                "Please:\n"
                "1. Go to https://makersuite.google.com/app/apikey\n"
                "2. Create a new API key (it should start with 'AI', not 'AIzaSy')\n"
                "3. Update your .env file with the new key"
            )
        return key

    @property
    def cleaned_serpapi_key(self) -> str:
        return self.SERPAPI_API_KEY.strip() if self.SERPAPI_API_KEY else ""

    @property
    def cleaned_mistral_key(self) -> str:
        return self.MISTRAL_API_KEY.strip() if self.MISTRAL_API_KEY else ""

    # Frontend URL
    FRONTEND_URL: str

    # We no longer need CHROMA_HOST and CHROMA_PORT
    # because we are using a local, persistent ChromaDB client.

    class Config:
        env_file = ".env"


settings = Settings()
