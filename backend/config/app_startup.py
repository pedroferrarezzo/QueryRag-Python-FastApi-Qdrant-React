import logging

from utils.cors_utils import get_cors_origins
from fastapi import FastAPI

from repository.vector_qdrant_repository import init_collection
from repository.minio_repository import initialize_minio
from contextlib import asynccontextmanager
from config.canonical_logger import configure_app_logging, put_log_context

from config.env import QUERY_RAG_FRONTEND_URL

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa configurações necessárias para o funcionamento da aplicação."""
    
    configure_app_logging()

    app_logger = logging.getLogger("app")

    put_log_context("type", "app_startup")
    app_logger.info(f"CORS Origins configurado para: {get_cors_origins(QUERY_RAG_FRONTEND_URL)}")

    await initialize_minio()
    await init_collection()
    
    yield