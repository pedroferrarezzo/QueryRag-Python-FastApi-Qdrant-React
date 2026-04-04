from qdrant_client.models import datetime

from exceptions import LmmException, InvalidValueException
from fastapi.responses import JSONResponse
from fastapi import Request

from dto import ErrorDto

async def lmm_handler(request: Request, exc: LmmException):
    return JSONResponse(
        status_code=500,
        content=ErrorDto(data=str(exc), timestamp=datetime.now().isoformat()).model_dump()
    )

async def invalid_value_handler(request: Request, exc: InvalidValueException):
    return JSONResponse(
        status_code=400,
        content=ErrorDto(data=str(exc), timestamp=datetime.now().isoformat()).model_dump()
    )