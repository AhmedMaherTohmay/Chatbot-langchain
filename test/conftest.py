import pytest
import google.generativeai as genai
from dotenv import load_dotenv

# Configure the API key for testing
load_dotenv()
@pytest.fixture(scope="session", autouse=True)
def configure_gemini():
    genai.configure(api_key="gemini_api_key")