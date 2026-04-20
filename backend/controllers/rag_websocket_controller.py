import json
import base64
import logging
import magic
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from dto import ErrorDto, LmmResponseDto
from exceptions import LmmException
from config.canonical_logger_config import put_log_context, clear_log_context
from fastapi import APIRouter, Depends
from utils.parse_utils import convert_webm_to_wav
from config.ioc.service import get_embedding_service, get_vector_service, get_lmm_service
from service import EmbeddingService, VectorService, LmmService

router = APIRouter()
logger = logging.getLogger("app")

@router.websocket("/rag/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_service: VectorService = Depends(get_vector_service),
    lmm_service: LmmService = Depends(get_lmm_service)
):
    await websocket.accept()

    try:
        while True and websocket.client_state == WebSocketState.CONNECTED:
            message = await websocket.receive()

            questionId = None
            prompt = None
            prompt_b64 = None
            prompt_raw_bytes = None
            prompt_mime_type = None

            try:
                if "text" in message:
                    payload = json.loads(message["text"])
                    prompt = payload.get("prompt")
                    questionId = payload.get("questionId")
                    prompt_b64 = payload.get("prompt_b64")
                
                    if not questionId:
                        await websocket.send_json(ErrorDto(data="questionId é obrigatório.", timestamp=datetime.now().isoformat()).model_dump())
                        continue
                
                put_log_context("type", "websocket")

                if prompt_b64:
                    prompt_raw_bytes = base64.b64decode(prompt_b64)
                    mime = magic.Magic(mime=True)
                    prompt_mime_type = mime.from_buffer(prompt_raw_bytes)

                    if prompt_mime_type == "video/webm":
                        try:
                            prompt_raw_bytes = convert_webm_to_wav(prompt_raw_bytes)
                            prompt_mime_type = "audio/wav"
                        except Exception as e:
                            logger.error("request_error: %s", e)
                            clear_log_context()

                            await websocket.send_json(ErrorDto(data="Erro na conversão de áudio Webm para Wav.", timestamp=datetime.now().isoformat()).model_dump())
                            continue

            except Exception as e:
                logger.error("request_error: %s", e)
                clear_log_context()

                await websocket.send_json(ErrorDto(data="Erro ao decodificar a mensagem.", timestamp=datetime.now().isoformat()).model_dump())
                continue

            if not prompt and not prompt_raw_bytes:
                continue

            put_log_context("prompt_received", prompt if prompt else "binary_data_received")
            put_log_context("mime_type", prompt_mime_type if prompt_mime_type else "N/A")

            try:
                if prompt_raw_bytes:
                    put_log_context("query_vector_embed_type", "binary")
                    query_vector = await embedding_service.get_vector(prompt_raw_bytes, prompt_mime_type)
                else:
                    put_log_context("query_vector_embed_type", "text")
                    query_vector = await embedding_service.get_vector(prompt)

                put_log_context("query_vector_length", len(query_vector) if query_vector else 0)
                documents = await vector_service.search_documents(query_vector, 5)

                if not documents:
                    await websocket.send_json(ErrorDto(
                        data="Nenhum documento relevante encontrado para a consulta.",
                        timestamp=datetime.now().isoformat()
                    ).model_dump())
                    continue

                responses = await lmm_service.contact_ai(prompt if prompt else "", documents, prompt_raw_bytes, prompt_mime_type)

                async for response in responses:
                    for part in response.candidates[0].content.parts:
                        if part.text:
                            await websocket.send_json(LmmResponseDto(
                                type="text",
                                data=part.text,
                                documents=documents,
                                timestamp=datetime.now().isoformat(),
                                questionId=questionId
                            ).model_dump())

                        elif part.inline_data:
                            b64_data = base64.b64encode(part.inline_data.data).decode('utf-8')
                            await websocket.send_json(LmmResponseDto(
                                type="binary",
                                mime_type=part.inline_data.mime_type,
                                data=b64_data,
                                documents=documents,
                                timestamp=datetime.now().isoformat(),
                                questionId=questionId
                            ).model_dump())
                
                await websocket.send_json(LmmResponseDto(
                                type="end",
                                data="End of response",
                                documents=documents,
                                timestamp=datetime.now().isoformat(),
                                questionId=questionId
                            ).model_dump())

                logger.info("request_completed")
                clear_log_context()

            except LmmException as e:
                logger.error("request_error: %s", e)
                clear_log_context()

                await websocket.send_json(ErrorDto(
                    data=str(e),
                    timestamp=datetime.now().isoformat()
                ).model_dump())
            except Exception as e:
                logger.error("request_error: %s", e)
                clear_log_context()

                await websocket.send_json(ErrorDto(
                    data="Erro inesperado durante o processamento da resposta: " + str(e),
                    timestamp=datetime.now().isoformat()
                ).model_dump())

    except WebSocketDisconnect:
        logger.info("websocket_disconnected")