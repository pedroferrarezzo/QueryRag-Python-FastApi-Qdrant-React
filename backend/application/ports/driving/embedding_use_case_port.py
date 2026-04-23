from abc import ABC, abstractmethod
from typing import List, Union

class EmbeddingUseCase(ABC):
    """Porta de entrada para geração de embeddings."""

    @abstractmethod
    async def get_vector(self, content: Union[str, bytes], mime_type: str | None) -> list[float]:
        """Gera um vetor de embedding a partir do conteúdo fornecido de forma independente do provedor."""
        pass

    @abstractmethod
    async def get_vectors(self, contents: List[Union[str, bytes]], mime_types: List[str | None]) -> List[List[float]]:
        """Gera embeddings em lote a partir de uma lista de conteúdos (texto ou bytes), de forma independente do provedor."""
        pass

    @abstractmethod
    def chunk_text(self, text: str) -> list[str]:
        """Realiza a quebra do texto em chunks semânticos para geração de embeddings."""
        pass