import json
import base64
import logging

from fastapi import WebSocket, WebSocketDisconnect

from dto import ErrorDto, LmmResponseDto

from exceptions import LmmException
from service.embedding_service import embed_data
from service.gemini_service import contact_ai

from repository.vector_qdrant_repository import search_vector

import magic

from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger("app")

@router.websocket("/rag/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            message = await websocket.receive()

            prompt = None
            prompt_raw_bytes = None
            prompt_mime_type = None

            try:
                if "text" in message:
                    payload = json.loads(message["text"])
                    prompt = payload.get("prompt")

                elif "bytes" in message:
                    prompt_raw_bytes = message["bytes"]
                    mime = magic.Magic(mime=True)
                    prompt_mime_type = mime.from_buffer(prompt_raw_bytes)

            except Exception:
                await websocket.send_json(ErrorDto(error_message="Erro ao decodificar a mensagem.").model_dump())
                continue

            if not prompt and not prompt_raw_bytes:
                continue

            try:
                if prompt_raw_bytes:
                    query_vector = await embed_data(prompt_raw_bytes, prompt_mime_type)
                else:
                    query_vector = await embed_data(prompt)

                documents = await search_vector(query_vector, 5)

                if not documents:
                    await websocket.send_json(ErrorDto(
                        error_message="Nenhum documento relevante encontrado para a consulta."
                    ).model_dump())
                    continue

                responses = await contact_ai(prompt if prompt else "", documents, prompt_raw_bytes, prompt_mime_type)

                async for response in responses:
                    for part in response.candidates[0].content.parts:
                        if part.text:
                            await websocket.send_json(LmmResponseDto(
                                type="text",
                                data=part.text,
                                documents=documents
                            ).model_dump())

                        elif part.inline_data:
                            b64_data = base64.b64encode(part.inline_data.data).decode('utf-8')
                            await websocket.send_json(LmmResponseDto(
                                type="binary",
                                mime_type=part.inline_data.mime_type,
                                data=b64_data,
                                documents=documents
                            ).model_dump())
                
                await websocket.send_json({
                    "type": "end"
                })

            except LmmException as e:
                await websocket.send_json(ErrorDto(
                    error_message=str(e)
                ).model_dump())
            except Exception as e:
                await websocket.send_json(ErrorDto(
                    error_message="Erro inesperado durante o processamento da resposta: " + str(e)
                ).model_dump())

    except WebSocketDisconnect:
        logger.info("websocket_disconnected")