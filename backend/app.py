from utils.cors_utils import get_cors_origins
from docling.exceptions import ConversionError
from fastapi import FastAPI

from config.app_startup import lifespan
from exceptions.global_exception_handler import docling_format_handler, invalid_value_handler, lmm_handler
from exceptions import LmmException, InvalidValueException
from middlewares.log_middleware import log_context_middleware
from fastapi.middleware.cors import CORSMiddleware
from config.env import QUERY_RAG_FRONTEND_URL

from controllers.vectors_controller import router as vectors_router
from controllers.rag_websocket_controller import router as websocket_router

app = FastAPI(lifespan=lifespan)

app.include_router(vectors_router)
app.include_router(websocket_router)

app.middleware("http")(log_context_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(QUERY_RAG_FRONTEND_URL),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(LmmException, lmm_handler)
app.add_exception_handler(InvalidValueException, invalid_value_handler)
app.add_exception_handler(ConversionError, docling_format_handler)