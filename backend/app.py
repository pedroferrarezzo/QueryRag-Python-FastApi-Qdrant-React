from fastapi import FastAPI

from config.app_startup import lifespan
from exceptions.global_exception_handler import invalid_value_handler, lmm_handler
from exceptions import LmmException, InvalidValueException
from middlewares.log_middleware import log_context_middleware

from controllers.vectors_controller import router as vectors_router
from controllers.rag_websocket_controller import router as websocket_router

app = FastAPI(lifespan=lifespan)

app.include_router(vectors_router)
app.include_router(websocket_router)

app.middleware("http")(log_context_middleware)

app.add_exception_handler(LmmException, lmm_handler)
app.add_exception_handler(InvalidValueException, invalid_value_handler)