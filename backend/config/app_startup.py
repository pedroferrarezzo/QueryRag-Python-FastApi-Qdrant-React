from fastapi import FastAPI
from repository.vector_qdrant_repository import init_collection
from repository.minio_repository import initialize_minio
from contextlib import asynccontextmanager
from config.canonical_logger import configure_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa configurações necessárias para o funcionamento da aplicação."""
    
    configure_logging()

    await initialize_minio()
    await init_collection()
    
    yield