from docling.exceptions import ConversionError
from qdrant_client.models import datetime

from domain.exceptions import LmmException, InvalidValueException, ParseException
from fastapi.responses import JSONResponse
from fastapi import Request
from application.dto import ErrorDto

async def lmm_handler(request: Request, exc: LmmException):
    """Handler para exceções do tipo LmmException."""
    return JSONResponse(
        status_code=500,
        content=ErrorDto(data=str(exc), timestamp=datetime.now().isoformat()).model_dump()
    )

async def invalid_value_handler(request: Request, exc: InvalidValueException):
    """Handler para exceções do tipo InvalidValueException."""
    return JSONResponse(
        status_code=400,
        content=ErrorDto(data=str(exc), timestamp=datetime.now().isoformat()).model_dump()
    )

async def docling_format_handler(request: Request, exc: ConversionError):
    """Handler para exceções do tipo ConversionError do docling."""
    return JSONResponse(
        status_code=400,
        content=ErrorDto(data="Formato de arquivo inválido", timestamp=datetime.now().isoformat()).model_dump()
    )

async def parse_exception_handler(request: Request, exc: ParseException):
    """Handler para exceções do tipo ParseException."""
    return JSONResponse(
        status_code=400,
        content=ErrorDto(data=str(exc), timestamp=datetime.now().isoformat()).model_dump()
    )

async def value_error_exception_handler(request: Request, exc: ValueError):
    """Handler para exceções do tipo ValueError."""
    return JSONResponse(
        status_code=400,
        content=ErrorDto(data=str(exc), timestamp=datetime.now().isoformat()).model_dump()
    )