# config/env.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY não definida")
if not QDRANT_HOST:
    raise ValueError("QDRANT_HOST não definida")
if not QDRANT_PORT:
    raise ValueError("QDRANT_PORT não definida")
if not QDRANT_COLLECTION:
    raise ValueError("QDRANT_COLLECTION não definida")