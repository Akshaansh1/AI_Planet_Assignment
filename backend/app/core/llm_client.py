import requests
from .config import settings


class MistralClient:
    """Simple client for Mistral API using REST calls via requests."""

    BASE_URL = "https://api.mistral.ai"

    def __init__(self):
        self.api_key = settings.cleaned_mistral_key

    def _headers(self):
        if not self.api_key:
            raise RuntimeError("Mistral API key not configured in backend .env")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate(
        self, prompt: str, model: str = "mistral-small", temperature: float = 0.7
    ) -> str:
        """Call Mistral text generation endpoint and return text."""
        # Use the correct Mistral AI chat completions endpoint
        endpoint = "/v1/chat/completions"

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }

        url = f"{self.BASE_URL}{endpoint}"
        try:
            resp = requests.post(url, json=payload, headers=self._headers(), timeout=30)
        except Exception as e:
            raise RuntimeError(f"Network error calling {url}: {e}")

        if resp.status_code != 200:
            raise RuntimeError(
                f"Mistral API error {resp.status_code} at {url}: {resp.text}"
            )

        try:
            data = resp.json()
        except Exception:
            raise RuntimeError(f"Invalid JSON response from Mistral API: {resp.text}")

        if not isinstance(data, dict) or "choices" not in data or not data["choices"]:
            raise RuntimeError(f"Unexpected response format from Mistral API: {data}")

        # Get the response content from the first choice
        choice = data["choices"][0]
        if (
            not isinstance(choice, dict)
            or "message" not in choice
            or "content" not in choice["message"]
        ):
            raise RuntimeError(f"Unexpected choice format from Mistral API: {choice}")

        return choice["message"]["content"]

        # After trying all endpoints/payloads, raise last captured error
        raise RuntimeError(last_error or "Unknown error calling Mistral API")


mistral_client = MistralClient()


async def get_mistral_response(
    prompt: str, model: str = "mistral-small", temperature: float = 0.7
) -> str:
    return mistral_client.generate(prompt, model, temperature)
