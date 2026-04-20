from abc import ABC, abstractmethod
from model import Document, Vector

class VectorRepository(ABC):
    """Interface para o repositório de vetores."""

    @abstractmethod
    async def add_vector(self, vector_object: Vector) -> None:
        """Adiciona um vetor ao banco de dados vetorial."""
        pass

    @abstractmethod
    async def add_vectors(self, vectors: list[Vector]) -> None:
        """Adiciona uma lista de vetores ao banco de dados vetorial."""
        pass

    @abstractmethod
    async def search_vector(self, vector: list[float], k: int = 5) -> list[Document]:
        """Busca os vetores mais similares e retorna os documentos correspondentes."""
        pass