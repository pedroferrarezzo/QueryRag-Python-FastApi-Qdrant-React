from abc import ABC, abstractmethod

class DocumentParser(ABC):
    """Interface para parsing de documentos."""

    @abstractmethod
    def extract_text(self, path: str) -> str:
        """Extrai o texto de um documento."""
        pass