from domain import Document
from typing import AsyncIterator
from google.genai import types
from infrastructure.config.gemini_config import client
from infrastructure.config.env_config import GEMINI_LMM_MODEL
from domain.ports.driven import ObjectStorageRepository, LmmModel

class GeminiLmmModel(LmmModel):
    """Implementação do modelo de linguagem multimodal para o Google Gemini."""

    def __init__(self, object_storage_repository: ObjectStorageRepository):
        """Inicializa o modelo de linguagem multimodal."""
        self._object_storage_repository = object_storage_repository

    async def get_interator(self, final_prompt: str, documents: list[Document], prompt_raw_bytes: bytes | None, prompt_mime_type: str | None) -> AsyncIterator:
        """Obtém um iterador assíncrono para a resposta gerada pelo modelo de linguagem multimodal com base no prompt final e nos documentos fornecidos."""

        parts = [types.Part.from_text(text=final_prompt)]    
        if prompt_raw_bytes and prompt_mime_type:
            parts.append(types.Part.from_bytes(data=prompt_raw_bytes, mime_type=prompt_mime_type))

        for document in documents:
            if document.metadata.object.include_in_prompt:
                object_file_bytes = await self._object_storage_repository.download_file(document.metadata.object.key)
                # Eventualmente pode ser alterado para from_url, caso o objeto seja acessível publicamente via URL, evitando a necessidade de download e reupload do arquivo para a API do Gemini
                parts.append(types.Part.from_bytes(data=object_file_bytes, mime_type=document.metadata.type))

        content = types.Content(
                role="user",
                parts=parts
        )
          
        # https://github.com/google-gemini/api-examples/blob/856e8a0f566a2810625cecabba6e2ab1fe97e496/python/text_generation.py#L37-L45
        # Futuramente podemos utilizar um modelo que seja generativo multimodal
        content_response_iterator = await client.aio.models.generate_content_stream(
                                    model=GEMINI_LMM_MODEL, contents=[content]
                                )

        return content_response_iterator