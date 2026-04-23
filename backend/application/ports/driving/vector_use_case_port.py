from abc import ABC, abstractmethod
from application.dto import DocumentDto, VectorDto

class VectorUseCase(ABC):
    """Porta de entrada para persistência e busca vetorial."""

    @abstractmethod
    async def ingest_vector(self, vector: VectorDto) -> None:
        """Adiciona um vetor com os metadados associados."""
        pass

    @abstractmethod
    async def ingest_vectors(self, vectors: list[VectorDto]) -> None:
        """Adiciona uma lista de vetores com os metadados associados."""
        pass

    @abstractmethod
    async def search_documents(self, vector: list[float], k: int) -> list[DocumentDto]:
        """Busca os vetores mais similares e retorna os documentos correspondentes."""
        pass