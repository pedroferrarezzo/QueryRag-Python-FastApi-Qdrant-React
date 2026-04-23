print(
r"""
  ____                               ____                
 / __ \ _   _   ___  _ __  _   _    |  _ \  __ _   __ _ 
| |  | | | | | / _ \| '__|| | | |   | |_) |/ _` | / _` |
| |__| | |_| ||  __/| |   | |_| |   |  _ <| (_| || (_| |
 \___\_\\____| \___||_|    \__, |   |_| \_\\____| \___ |
                           |___/                  |___/ 
"""
)

# Precisa ser importado primeiro para adicionar o binário do ffmpeg ao PATH antes de qualquer operação que dependa do ffmpeg.
import static_ffmpeg
static_ffmpeg.add_paths()

from infrastructure.utils.cors_utils import get_cors_origins
from docling.exceptions import ConversionError
from fastapi import FastAPI

from infrastructure.config.app_startup_config import lifespan
from infrastructure.adapters.driving.controllers.exceptions.global_exception_handler import docling_format_handler, invalid_value_handler, lmm_handler, value_error_exception_handler
from domain.exceptions import LmmException, InvalidValueException
from infrastructure.adapters.driving.controllers.middlewares.log_middleware import log_context_middleware
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.config.env_config import QUERY_RAG_FRONTEND_URL

from infrastructure.adapters.driving.controllers.vectors_controller import router as vectors_router
from infrastructure.adapters.driving.controllers.rag_websocket_controller import router as websocket_router

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
app.add_exception_handler(ValueError, value_error_exception_handler)