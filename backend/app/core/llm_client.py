from openai import OpenAI
import google.generativeai as genai
from .config import settings

class LLMClient:
    """
    Client for interacting with Large Language Models (LLMs).
    """
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-pro')

    def get_openai_response(self, prompt: str, model="gpt-3.5-turbo"):
        """
        Gets a response from OpenAI's GPT model.
        """
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting response from OpenAI: {e}")
            return None

    def get_gemini_response(self, prompt: str):
        """
        Gets a response from Google's Gemini model.
        """
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error getting response from Gemini: {e}")
            return None

llm_client = LLMClient()
