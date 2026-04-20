from abc import ABC, abstractmethod
from typing import AsyncIterator
from model import Document

class LmmModel(ABC):
    """Interface para modelos de linguagem multimodal."""

    @abstractmethod
    async def get_interator(self, final_prompt: str, documents: list[Document], prompt_raw_bytes: bytes | None, prompt_mime_type: str | None) -> AsyncIterator:
        """Obtém um iterador assíncrono para a resposta gerada pelo modelo de linguagem multimodal com base no prompt final e nos documentos fornecidos."""
        pass