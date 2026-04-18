import logging

from fastapi import Request
import uuid

from config.canonical_logger import put_log_context, clear_log_context

logger = logging.getLogger("app")

async def log_context_middleware(request: Request, call_next):

    put_log_context("type", "http")
    put_log_context("request_id", str(uuid.uuid4()))
    put_log_context("method", request.method)
    put_log_context("url", str(request.url))

    response = None

    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error("request_error: %s", e)
        raise
    finally:
        if response:
            put_log_context("response_status_code", response.status_code)
            
        logger.info("request_completed")
        clear_log_context()