import tempfile
import os
from infrastructure.config.canonical_logger_config import put_log_context
from typing import Annotated
from fastapi import UploadFile, File, Form, APIRouter, Depends, status
from application.dto import IngestResultDto, VectorDto, ObjectDto, ErrorDto, DocumentDto
from infrastructure.config.ioc.service import get_object_storage_service, get_embedding_service, get_vector_service, get_document_parser_service, get_content_service
from infrastructure.config.env_config import CHUNK_LIST_MAX_LENGTH
from application.ports.driving import ObjectStorageUseCase, EmbeddingUseCase, VectorUseCase, DocumentParserUseCase, ContentUseCase

router = APIRouter(tags=["Vectors"])

@router.post(
    "/vectors/ingest",
    status_code=status.HTTP_201_CREATED,
    response_model=IngestResultDto,
    summary="Ingerir e vetorizar arquivo",
    description="Recebe um arquivo, gera embeddings e salva os vetores na base vetorial.",
    responses={
        400: {"model": ErrorDto, "description": "Arquivo ausente ou inválido."},
        500: {"model": ErrorDto, "description": "Erro interno durante ingestão."},
    },
)
async def ingest(
    file: Annotated[
        UploadFile | None,
        File(description="Arquivo para ingestão (texto, imagem, áudio ou vídeo)."),
    ] = None,
    object_storage_service: ObjectStorageUseCase = Depends(get_object_storage_service),
    embedding_service: EmbeddingUseCase = Depends(get_embedding_service),
    vector_service: VectorUseCase = Depends(get_vector_service),
    document_parser_service: DocumentParserUseCase = Depends(get_document_parser_service),
    content_service: ContentUseCase = Depends(get_content_service)
):
    if not file or not file.filename:
        raise ValueError("Nenhum arquivo fornecido para ingestão.")
    
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

            chunks = content_service.chunk_text(text, CHUNK_LIST_MAX_LENGTH)
            vectors = await embedding_service.get_vectors(contents=chunks)

            vectors = [VectorDto(
                vector=vector,
                type=file.content_type,
                chunk=chunk,
                source=file.filename,
                object=ObjectDto(key=object_data["key"], url=object_data["url"], include_in_prompt=False)
            ) for chunk, vector in zip(chunks, vectors)]

            await vector_service.ingest_vectors(vectors)

            ingest_result.chunks_stored = len(vectors)
            put_log_context("embedding_method_type", "docling_and_chunking")
        finally:        
            if path:
                os.remove(path)

    return ingest_result

@router.post(
    "/vectors/query",
    status_code=status.HTTP_200_OK,
    response_model=list[DocumentDto],
    summary="Consultar documentos similares",
    description="Busca documentos semanticamente similares a um prompt textual ou a um arquivo.",
    responses={
        400: {"model": ErrorDto, "description": "Entrada inválida (prompt/arquivo)."},
        500: {"model": ErrorDto, "description": "Erro interno durante consulta."},
    },
)
async def query(
    prompt: Annotated[
        str | None,
        Form(description="Prompt textual para busca semântica."),
    ] = None,
    file: Annotated[
        UploadFile | None,
        File(description="Arquivo para busca semântica (alternativo ao prompt)."),
    ] = None,
    embedding_service: EmbeddingUseCase = Depends(get_embedding_service),
    vector_service: VectorUseCase = Depends(get_vector_service)
):

    if not prompt and (not file or not file.filename):
        raise ValueError("Forneça um prompt ou um arquivo para pesquisa.")

    if file and file.filename and prompt:
        raise ValueError("Forneça ou um prompt ou um arquivo para pesquisa, não ambos.")
    
    query_vector = None

    if file and file.filename:
        fileBytes = await file.read()
        query_vector = await embedding_service.get_vector(fileBytes, file.content_type)
    else:
        query_vector = await embedding_service.get_vector(prompt)

    documents = await vector_service.search_documents(query_vector, 20)

    put_log_context("user_query", prompt)
    put_log_context("documents_returned_size", len(documents))

    return [doc.model_dump() for doc in documents]