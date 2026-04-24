from typing import List

from domain.exceptions import InvalidValueException
from domain.model import Content
from application.ports.driving import ContentUseCase

class ContentService(ContentUseCase):
    """Serviço responsável por processar o conteúdo extraído de documentos, transformando-o em uma estrutura adequada para embedding."""

    def chunk_text(self, text: str, chunk_max_length: int) -> List[str]:
        """
        Divide o texto em chunks de tamanho máximo especificado.
        """
        
        contents = Content(
            content=text,
            chunk_max_length=chunk_max_length
        )
                
        chunks_text = [chunk.content for chunk in contents.chunks]

        return chunks_text