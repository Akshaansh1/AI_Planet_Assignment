import chromadb
from .config import settings

class ChromaDBClient:
    """
    Client for interacting with ChromaDB.
    """
    def __init__(self):
        self.client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)

    def get_or_create_collection(self, name: str):
        """
        Gets or creates a collection in ChromaDB.
        """
        return self.client.get_or_create_collection(name=name)

chroma_client = ChromaDBClient()
