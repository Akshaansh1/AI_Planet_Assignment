from .config import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingClient:
    """Placeholder embedding client. Mistral embeddings are not implemented here.
    Methods return None and log warnings. This prevents crashes while other LLM
    logic was migrated to use Mistral for text generation.
    """

    def __init__(self):
        logger.warning(
            "EmbeddingClient initialized as placeholder — no embedding providers configured."
        )

    def get_openai_embedding(self, text: str, model: str = "text-embedding-ada-002"):
        logger.warning("OpenAI embeddings not available in this deployment.")
        return None

    def get_gemini_embedding(self, text: str, model: str = "models/embedding-001"):
        logger.warning("Gemini embeddings not available in this deployment.")
        return None

    def is_available(self):
        return False


# Create a global instance
try:
    embedding_client = EmbeddingClient()
except Exception as e:
    logger.error(f"Failed to initialize embedding client: {e}")
    embedding_client = None
