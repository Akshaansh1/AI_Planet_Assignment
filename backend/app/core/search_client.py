from serpapi import GoogleSearch
from .config import settings


class SearchClient:
    """
    Client for performing web searches using SerpAPI.
    """

    def __init__(self):
        self.serpapi_api_key = settings.SERPAPI_API_KEY

    def search_serpapi(self, query: str):
        """
        Performs a search using SerpAPI.
        """
        params = {"q": query, "api_key": self.serpapi_api_key}
        # The correct class for this version is GoogleSearch
        client = GoogleSearch(params)
        results = client.get_dict()
        return results.get("organic_results", [])


search_client = SearchClient()
