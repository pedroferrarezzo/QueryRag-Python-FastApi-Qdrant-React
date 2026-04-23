from abc import ABC, abstractmethod
from typing import AsyncIterator
from application.dto import DocumentDto

class LmmUseCase(ABC):
    """Porta de entrada para modelos multimodais."""

    @abstractmethod
    async def contact_ai(
        self,
        final_prompt: str,
        documents: list[DocumentDto],
        prompt_raw_bytes: bytes | None,
        prompt_mime_type: str | None
    ) -> AsyncIterator:
        """Orquestra a preparação do contexto e delega a geração de conteúdo a um provedor de LLM multimodal."""
        pass