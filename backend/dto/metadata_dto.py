from pydantic import BaseModel

from .object_dto import ObjectDto

class MetadataDto(BaseModel):
    """Classe para armazenar metadados de um documento recuperado durante o RAG."""

    type: str
    """Tipo do documento."""

    chunk: str | None
    """Conteúdo do documento."""

    source: str
    """Fonte do documento."""

    object: ObjectDto
    """Informações de objeto."""