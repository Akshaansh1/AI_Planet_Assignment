import google.generativeai as genai
from openai import OpenAI
from .config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMClient:
    """
    Client for interacting with Language Models (OpenAI and Gemini)
    """

    def __init__(self):
        logger.info("Initializing LLM clients...")
        self._init_openai()
        self._init_gemini()

    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            self.openai_client = OpenAI(api_key=settings.cleaned_openai_key)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.openai_client = None

    def _init_gemini(self):
        """Initialize Gemini client"""
        try:
            # Configure Gemini with API key
            api_key = settings.cleaned_gemini_key
            if not api_key:
                raise ValueError("Gemini API key is not set")

            logger.info(
                f"Initializing Gemini with key starting with: {api_key[:10]}..."
            )
            genai.configure(api_key=api_key)
            logger.info("Gemini configured successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            raise RuntimeError(f"Gemini initialization failed: {str(e)}")

    def get_openai_response(self, prompt: str, model="gpt-3.5-turbo", temperature=0.7):
        """Get response from OpenAI"""
        if not self.openai_client:
            raise RuntimeError("OpenAI client not initialized")

        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            logger.error(f"OpenAI API error: {error_msg}")

            if "insufficient_quota" in error_msg:
                raise RuntimeError("OpenAI API quota exceeded")
            elif "invalid_api_key" in error_msg:
                raise RuntimeError("Invalid OpenAI API key")
            else:
                raise RuntimeError(f"OpenAI error: {error_msg}")

    def get_gemini_response(self, prompt: str, model="gemini-pro", temperature=0.7):
        """Get response from Gemini"""
        try:
            # Validate API key format
            api_key = settings.cleaned_gemini_key
            if not api_key.startswith("AI"):
                raise ValueError(
                    "Invalid Gemini API key format. Please get a valid API key from "
                    "Google AI Studio (https://makersuite.google.com/app/apikey). "
                    "The key should start with 'AI'. The key you provided looks like "
                    "a Google Cloud API key, which won't work with Gemini."
                )

            # Create a new model instance for each request
            gemini_model = genai.GenerativeModel(model)

            # Simple request without extra config to minimize potential issues
            response = gemini_model.generate_content(prompt)

            logger.info("Received response from Gemini")

            if response and response.text:
                return response.text
            else:
                raise RuntimeError("Gemini returned empty response")

        except ValueError as ve:
            # Re-raise validation errors with clear messages
            raise RuntimeError(str(ve))
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Gemini API error: {type(e).__name__} - {error_msg}")

            if "API key not valid" in error_msg:
                raise RuntimeError(
                    "Invalid Gemini API key. Please:\n"
                    "1. Go to https://makersuite.google.com/app/apikey\n"
                    "2. Sign in with your Google account\n"
                    "3. Click 'Create API key'\n"
                    "4. Copy the new API key (should start with 'AI')\n"
                    "5. Update your .env file with the new key"
                )
            else:
                raise RuntimeError(f"Gemini error: {error_msg}")


# Create a global instance
llm_client = LLMClient()


# Async wrapper functions
async def get_openai_response(
    prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7
) -> str:
    return llm_client.get_openai_response(prompt, model, temperature)


async def get_gemini_response(
    prompt: str, model: str = "gemini-pro", temperature: float = 0.7
) -> str:
    return llm_client.get_gemini_response(prompt, model, temperature)
