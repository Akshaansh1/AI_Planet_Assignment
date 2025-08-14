from fastapi import APIRouter
from pydantic import BaseModel
from ..core.chroma import chroma_client
from ..core.embeddings import embedding_client

router = APIRouter()

class KnowledgeQuery(BaseModel):
    query: str
    top_k: int = 3

@router.post("/query")
def query_knowledge_base(request: KnowledgeQuery):
    """
    Queries the knowledge base for relevant documents.
    """
    query_embedding = embedding_client.get_openai_embedding(request.query)
    collection = chroma_client.get_or_create_collection(name="documents")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=request.top_k
    )
    return results
