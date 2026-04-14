import tempfile
import os

from config.canonical_logger import put_log_context

from typing import Optional

from fastapi import UploadFile, File, Form
from fastapi.responses import JSONResponse

from dto import VectorDto, IngestResultDto

from dto.object_storage_dto import ObjectStorageDto
from exceptions import InvalidValueException
from service.embedding_service import embed_data, embed_datas
from service.docling_service import extract_text
from repository.minio_repository import upload_file

from repository.vector_qdrant_repository import add_vector, search_vector, add_vectors

from utils.chunking_utils import chunk_text
from utils.text_utils import clean_text

from fastapi import APIRouter

router = APIRouter()

@router.post("/vectors/ingest")
async def ingest(
    file: UploadFile = File(None)
):
    if not file or not file.filename:
        raise InvalidValueException("Nenhum arquivo fornecido para ingestão.")
    
    ingest_result: IngestResultDto = IngestResultDto(chunks_stored=0)
    fileBytes = await file.read()
    object_storage = await upload_file(fileBytes, file.filename)

    if "image" in file.content_type or "video" in file.content_type or "audio" in file.content_type:
        vector = await embed_data(fileBytes, file.content_type)
  
        await add_vector(
            VectorDto(
                vector=vector,
                type=file.content_type,
                source=file.filename,
                object_storage=ObjectStorageDto(key=object_storage["key"], url=object_storage["url"], include_in_prompt=True)
            )
        )

        # Para arquivos binários, armazenamos apenas um vetor representando o arquivo inteiro, sem chunking
        chunks = [1]

        put_log_context("embedding_method_type", "direct_to_embedding_model")

    else:
        path = None

        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(fileBytes)
                
            path = tmp.name
            text = extract_text(path)
            text = clean_text(text)

            chunks = chunk_text(text)
            vectors = await embed_datas(contents=chunks)

            vector_dtos = [VectorDto(
                vector=vector,
                type=file.content_type,
                chunk=chunk,
                source=file.filename,
                object_storage=ObjectStorageDto(key=object_storage["key"], url=object_storage["url"], include_in_prompt=False)
            ) for chunk, vector in zip(chunks, vectors)]

            await add_vectors(vector_dtos)
        finally:        
            put_log_context("embedding_method_type", "docling_and_chunking")
            if path:
                os.remove(path)

    ingest_result.chunks_stored = len(chunks)

    return JSONResponse(status_code=201, content=ingest_result.model_dump())

@router.post("/vectors/query")
async def query(prompt: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):

    if not prompt and (not file or not file.filename):
        raise InvalidValueException("Forneça um prompt ou um arquivo para pesquisa.")

    if file and file.filename and prompt:
        raise InvalidValueException("Forneça ou um prompt ou um arquivo para pesquisa, não ambos.")
    
    query_vector = None

    if file and file.filename:
        fileBytes = await file.read()
        query_vector = await embed_data(fileBytes, file.content_type)
    else:
        query_vector = await embed_data(prompt)

    documents = await search_vector(query_vector, 20)

    put_log_context("user_query", prompt)
    put_log_context("documents_returned_size", len(documents))

    return JSONResponse(
        status_code=200,
        content=[doc.model_dump() for doc in documents]
    )