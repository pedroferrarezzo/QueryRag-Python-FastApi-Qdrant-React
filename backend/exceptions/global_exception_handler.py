from docling.exceptions import ConversionError
from qdrant_client.models import datetime

from exceptions import LmmException, InvalidValueException, ParseException
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

async def docling_format_handler(request: Request, exc: ConversionError):
    return JSONResponse(
        status_code=400,
        content=ErrorDto(data="Formato de arquivo inválido", timestamp=datetime.now().isoformat()).model_dump()
    )

async def parse_exception_handler(request: Request, exc: ParseException):
    return JSONResponse(
        status_code=400,
        content=ErrorDto(data=str(exc), timestamp=datetime.now().isoformat()).model_dump()
    )