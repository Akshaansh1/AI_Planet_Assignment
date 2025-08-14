from openai import OpenAI
import google.generativeai as genai
from .config import settings

class EmbeddingClient:
    """
    Client for generating text embeddings using different models.
    """
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        genai.configure(api_key=settings.GEMINI_API_KEY)

    def get_openai_embedding(self, text: str, model="text-embedding-ada-002"):
        """
        Generates embeddings using OpenAI's model.
        """
        text = text.replace("\n", " ")
        return self.openai_client.embeddings.create(input=[text], model=model).data[0].embedding

    def get_gemini_embedding(self, text: str, model="models/embedding-001"):
        """
        Generates embeddings using Gemini's model.
        """
        return genai.embed_content(model=model, content=text)["embedding"]

embedding_client = EmbeddingClient()
