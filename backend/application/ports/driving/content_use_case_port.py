from abc import ABC, abstractmethod
from typing import List

class ContentUseCase(ABC):
    """Porta de entrada para processamento de conteúdo extraído de documentos, transformando-o em uma estrutura adequada para embedding."""

    @abstractmethod
    def chunk_text(self, text: str, chunk_max_length: int) -> List[str]:
        """Divide o texto em chunks de tamanho máximo especificado."""
        pass
