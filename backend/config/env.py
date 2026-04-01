# config/env.py
import os

from dotenv import load_dotenv

from exceptions.startup_exception import StartupException

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
MINIO_HOST = os.getenv("MINIO_HOST")
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_SECURE = os.getenv("MINIO_SECURE")

if not GEMINI_API_KEY:
    raise StartupException("GEMINI_API_KEY não definida")
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
if not MINIO_ACCESS_KEY:
    raise StartupException("MINIO_ACCESS_KEY não definida")
if not MINIO_SECRET_KEY:
    raise StartupException("MINIO_SECRET_KEY não definida")
if not MINIO_BUCKET_NAME:
    raise StartupException("MINIO_BUCKET_NAME não definida")
if not MINIO_SECURE:
    raise StartupException("MINIO_SECURE não definida")

MINIO_SECURE = MINIO_SECURE.lower() == "true"