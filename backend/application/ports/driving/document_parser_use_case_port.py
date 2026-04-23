from abc import ABC, abstractmethod

class DocumentParserUseCase(ABC):
    """Porta de entrada para extração de texto de documentos."""

    @abstractmethod
    def extract_text(self, path: str) -> str:
        """Extrai o texto de um documento."""
        pass