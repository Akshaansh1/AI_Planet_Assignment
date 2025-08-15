from ..core.llm_client import mistral_client, get_mistral_response
from ..core.search_client import search_client
from ..core.chroma import chroma_client
from ..core.embeddings import embedding_client


class LLMService:
    """
    Service for orchestrating LLM interactions, including context retrieval and web search.
    """

    def generate_response(
        self,
        query: str,
        llm_provider: str = "openai",
        use_knowledge_base: bool = False,
        use_search: bool = False,
    ):
        """
        Generates a response by orchestrating different components.
        """
        context = ""
        prompt = query

        # 1. Retrieve context from KnowledgeBase if enabled
        if use_knowledge_base:
            query_embedding = embedding_client.get_openai_embedding(query)
            collection = chroma_client.get_or_create_collection(name="documents")
            results = collection.query(query_embeddings=[query_embedding], n_results=2)
            if results and results["documents"]:
                context += "\n\n--- Knowledge Base Context ---\n"
                for doc in results["documents"][0]:
                    context += doc + "\n"

        # 2. Perform web search if enabled
        if use_search:
            search_results = search_client.search_serpapi(query)
            if search_results:
                context += "\n\n--- Web Search Results ---\n"
                for result in search_results[:3]:  # Use top 3 results
                    context += f"Title: {result.get('title')}\nSnippet: {result.get('snippet')}\n\n"

        # 3. Construct the final prompt
        if context:
            prompt = f"Based on the following context, please answer the query.\n\nContext:{context}\n\nQuery: {query}"

        # 4. Get response from the selected LLM (Mistral is the default and only supported provider now)
        if (
            llm_provider == "mistral"
            or llm_provider == "openai"
            or llm_provider == "gemini"
        ):
            # We support calling mistral regardless of frontend-selected provider to simplify migration
            response = mistral_client.generate(prompt)
        else:
            return "Invalid LLM provider selected. Use 'mistral'."

        return response


llm_service = LLMService()
