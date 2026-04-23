# config/env.py
import os

from dotenv import load_dotenv

from infrastructure.exceptions import StartupException

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_LMM_MODEL = os.getenv("GEMINI_LMM_MODEL")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
MINIO_HOST = os.getenv("MINIO_HOST")
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_CONSOLE_PORT = os.getenv("MINIO_CONSOLE_PORT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_SECURE = os.getenv("MINIO_SECURE")
QUERY_RAG_FRONTEND_URL = os.getenv("QUERY_RAG_FRONTEND_URL")
EMBEDDING_DIMENSION = os.getenv("EMBEDDING_DIMENSION")
CHUNK_LIST_MAX_LENGTH = os.getenv("CHUNK_LIST_MAX_LENGTH")

if not GEMINI_API_KEY:
    raise StartupException("GEMINI_API_KEY não definida")
if not GEMINI_LMM_MODEL:
    raise StartupException("GEMINI_LMM_MODEL não definida")
if not GEMINI_EMBEDDING_MODEL:
    raise StartupException("GEMINI_EMBEDDING_MODEL não definida")
if not QDRANT_HOST:
    raise StartupException("QDRANT_HOST não definida")
if not QDRANT_PORT:
    raise StartupException("QDRANT_PORT não definida")
if not QDRANT_COLLECTION:
    raise StartupException("QDRANT_COLLECTION não definida")
if not MINIO_HOST:
    raise StartupException("MINIO_HOST não definida")
if not MINIO_PORT:
    raise StartupException("MINIO_PORT não definida")
if not MINIO_CONSOLE_PORT:
    raise StartupException("MINIO_CONSOLE_PORT não definida")
if not MINIO_ACCESS_KEY:
    raise StartupException("MINIO_ACCESS_KEY não definida")
if not MINIO_SECRET_KEY:
    raise StartupException("MINIO_SECRET_KEY não definida")
if not MINIO_BUCKET_NAME:
    raise StartupException("MINIO_BUCKET_NAME não definida")
if not MINIO_SECURE:
    raise StartupException("MINIO_SECURE não definida")
if not QUERY_RAG_FRONTEND_URL:
    raise StartupException("QUERY_RAG_FRONTEND_URL não definida")
if not EMBEDDING_DIMENSION:
    raise StartupException("EMBEDDING_DIMENSION não definida")
if not CHUNK_LIST_MAX_LENGTH:
    raise StartupException("CHUNK_LIST_MAX_LENGTH não definida")

EMBEDDING_DIMENSION = int(EMBEDDING_DIMENSION)
CHUNK_LIST_MAX_LENGTH = int(CHUNK_LIST_MAX_LENGTH)

MINIO_SECURE = MINIO_SECURE.lower() == "true"