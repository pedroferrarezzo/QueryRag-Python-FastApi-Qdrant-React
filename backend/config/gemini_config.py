from config.env_config import GEMINI_API_KEY
from google import genai

client=genai.Client(api_key=GEMINI_API_KEY)