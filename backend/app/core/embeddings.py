from openai import OpenAI
import google.generativeai as genai
from .config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingClient:
    """
    Client for generating text embeddings using different models.
    """
    def __init__(self):
        self.openai_available = False
        self.gemini_available = False
        
        # Initialize OpenAI client
        try:
            if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.openai_available = True
                logger.info("OpenAI client initialized successfully")
            else:
                logger.warning("OpenAI API key not configured")
        except Exception as e:
            logger.warning(f"Could not initialize OpenAI client: {e}")
        
        # Initialize Gemini client
        try:
            if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_available = True
                logger.info("Gemini client initialized successfully")
            else:
                logger.warning("Gemini API key not configured")
        except Exception as e:
            logger.warning(f"Could not initialize Gemini client: {e}")

    def get_openai_embedding(self, text: str, model="text-embedding-ada-002"):
        """
        Generates embeddings using OpenAI's model.
        """
        if not self.openai_available:
            logger.warning("OpenAI client not available")
            return None
        
        try:
            text = text.replace("\n", " ")
            response = self.openai_client.embeddings.create(input=[text], model=model)
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating OpenAI embedding: {e}")
            return None

    def get_gemini_embedding(self, text: str, model="models/embedding-001"):
        """
        Generates embeddings using Gemini's model.
        """
        if not self.gemini_available:
            logger.warning("Gemini client not available")
            return None
        
        try:
            return genai.embed_content(model=model, content=text)["embedding"]
        except Exception as e:
            logger.error(f"Error generating Gemini embedding: {e}")
            return None

    def is_available(self):
        """Check if any embedding service is available"""
        return self.openai_available or self.gemini_available

# Create a global instance
try:
    embedding_client = EmbeddingClient()
except Exception as e:
    logger.error(f"Failed to initialize embedding client: {e}")
    embedding_client = None
