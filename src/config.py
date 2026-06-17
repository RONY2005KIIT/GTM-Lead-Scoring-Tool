import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file if it exists
load_dotenv()

# Configuration variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

def configure_gemini() -> bool:
    """
    Configure the Google Generative AI SDK with the loaded API key.
    
    Returns:
        bool: True if configuration was successful, False otherwise.
    """
    if not GEMINI_API_KEY:
        return False
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return True
    except Exception:
        # Configuration error handling skeleton
        return False

def get_model_name() -> str:
    """
    Returns the configured Gemini model name.
    """
    return GEMINI_MODEL

def is_configured() -> bool:
    """
    Checks if all required settings are configured properly.
    """
    return bool(GEMINI_API_KEY)
