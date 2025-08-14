import chromadb
import os

persistent_directory = os.path.join(os.getcwd(), "chroma_data")

class ChromaDBClient:
    """
    Client for interacting with a persistent, local ChromaDB instance.
    """
    def __init__(self):
        self.client = chromadb.PersistentClient(path=persistent_directory)
        print(f"ChromaDB persistent client initialized at: {persistent_directory}")


    def get_or_create_collection(self, name: str):
        """
        Gets or creates a collection in ChromaDB.
        """
        return self.client.get_or_create_collection(name=name)

chroma_client = ChromaDBClient()
