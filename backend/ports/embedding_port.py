from abc import ABC, abstractmethod
from typing import List, Union

class EmbeddingModel(ABC):
    """Interface para modelos de embedding."""

    @abstractmethod
    async def embed_data(
        self,
        content: str | bytes,
        mime_type: str | None = None
    ) -> list[float]:
        """Gera um vetor de embedding a partir de um único conteúdo."""
        pass

    @abstractmethod
    async def embed_datas(
        self,
        contents: List[Union[str, bytes]],
        mime_types: List[str] | None = None
    ) -> List[List[float]]:
        """Gera embeddings em lote a partir de múltiplos conteúdos."""
        pass