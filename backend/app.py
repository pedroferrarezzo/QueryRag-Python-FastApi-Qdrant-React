import tempfile
import os
import json

from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect

from dto import VectorDto, RagQueryDto, IngestResultDto, ErrorDto

from service.embedding_service import embed_text
from service.reranker_service import rerank
from service.docling_service import extract_text
from service.gemini_service import contact_ai

from repository.vector_qdrant_repository import add_vector, search_vector

from utils.chunking_utils import chunk_text
from utils.text_utils import clean_text

app = FastAPI()

@app.post("/ingest")
async def ingest(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    if not text and not file:
        return ErrorDto(message="Nenhum texto ou arquivo fornecido para ingestão.")
    
    ingest_result: IngestResultDto = IngestResultDto(chunks_stored=0)

    if text:
        text = clean_text(text)
        chunks = chunk_text(text)

        for chunk in chunks:

            vector = embed_text(chunk)

            add_vector(
                VectorDto(
                    vector=vector,
                    type="text",
                    chunk=chunk
                )
            )

        ingest_result.chunks_stored = len(chunks)

    if file and file.filename:

        with tempfile.NamedTemporaryFile(delete=False) as tmp:

            tmp.write(await file.read())

            path = tmp.name   

        text = extract_text(path)
        text = clean_text(text)

        chunks = chunk_text(text)

        for chunk in chunks:

            vector = embed_text(chunk)

            add_vector(
                  VectorDto(
                    vector=vector,
                    type=file.content_type,
                    chunk=chunk,
                    source=file.filename
                )
            )

        os.remove(path)

        ingest_result.chunks_stored += len(chunks)

    return ingest_result

@app.get("/query")
async def query(prompt: str):

    query_vector = embed_text(prompt)

    documents = search_vector(query_vector, 20)
    documents = rerank(prompt, documents, 5)

    return RagQueryDto(query=prompt, documents=documents)

@app.websocket("/ws/rag")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            prompt = payload.get("prompt")

            if not prompt:
                continue

            query_vector = embed_text(prompt)
            documents = search_vector(query_vector, 20)
            documents = rerank(prompt, documents, 5)
            responses = contact_ai(prompt, documents)
            
            for chunk in responses:
                await websocket.send_text(chunk.text)

    except WebSocketDisconnect:
        print("Cliente desconectado")