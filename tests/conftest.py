import pytest
import google.generativeai as genai
from dotenv import load_dotenv
from config.config import Config

load_dotenv()
# Configure the API key for testing
@pytest.fixture(scope="session", autouse=True)
def configure_gemini():
    gemini_api_key = Config.GEMINI_API_KEY
    genai.configure(api_key=gemini_api_key)