import tempfile
import os
from config.canonical_logger_config import put_log_context
from typing import Optional
from fastapi import UploadFile, File, Form
from fastapi.responses import JSONResponse
from dto import IngestResultDto, VectorDto, ObjectDto
from exceptions import InvalidValueException
from fastapi import APIRouter, Depends
from config.ioc.service import get_object_storage_service, get_embedding_service, get_vector_service, get_document_parser_service
from service import ObjectStorageService, EmbeddingService, VectorService, DocumentParserService

router = APIRouter()

@router.post("/vectors/ingest")
async def ingest(
    file: UploadFile = File(None),
    object_storage_service: ObjectStorageService = Depends(get_object_storage_service),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_service: VectorService = Depends(get_vector_service),
    document_parser_service: DocumentParserService = Depends(get_document_parser_service)
):
    if not file or not file.filename:
        raise InvalidValueException("Nenhum arquivo fornecido para ingestão.")
    
    ingest_result: IngestResultDto = IngestResultDto(chunks_stored=0)
    fileBytes = await file.read()
    object_data = await object_storage_service.upload_object(fileBytes, file.filename)

    if "image" in file.content_type or "video" in file.content_type or "audio" in file.content_type:
        vector = await embedding_service.get_vector(fileBytes, file.content_type)
  
        await vector_service.ingest_vector(
            VectorDto(
                vector=vector,
                type=file.content_type,
                source=file.filename,
                object=ObjectDto(key=object_data["key"], url=object_data["url"], include_in_prompt=True)
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
            text = document_parser_service.extract_text(path)

            chunks = embedding_service.chunk_text(text)
            vectors = await embedding_service.get_vectors(contents=chunks)

            vectors = [VectorDto(
                vector=vector,
                type=file.content_type,
                chunk=chunk,
                source=file.filename,
                object=ObjectDto(key=object_data["key"], url=object_data["url"], include_in_prompt=False)
            ) for chunk, vector in zip(chunks, vectors)]

            await vector_service.ingest_vectors(vectors)
        finally:        
            put_log_context("embedding_method_type", "docling_and_chunking")
            if path:
                os.remove(path)

    ingest_result.chunks_stored = len(chunks)

    return JSONResponse(status_code=201, content=ingest_result.model_dump())

@router.post("/vectors/query")
async def query(
    prompt: Optional[str] = Form(None), 
    file: Optional[UploadFile] = File(None),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_service: VectorService = Depends(get_vector_service)
):

    if not prompt and (not file or not file.filename):
        raise InvalidValueException("Forneça um prompt ou um arquivo para pesquisa.")

    if file and file.filename and prompt:
        raise InvalidValueException("Forneça ou um prompt ou um arquivo para pesquisa, não ambos.")
    
    query_vector = None

    if file and file.filename:
        fileBytes = await file.read()
        query_vector = await embedding_service.get_vector(fileBytes, file.content_type)
    else:
        query_vector = await embedding_service.get_vector(prompt)

    documents = await vector_service.search_documents(query_vector, 20)

    put_log_context("user_query", prompt)
    put_log_context("documents_returned_size", len(documents))

    return JSONResponse(
        status_code=200,
        content=[doc.model_dump() for doc in documents]
    )