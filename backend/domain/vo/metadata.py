from pydantic import BaseModel

from .object import Object

class Metadata(BaseModel):
    """Value Object para armazenar metadados de um documento recuperado durante o RAG."""

    type: str
    """Tipo do documento."""

    chunk: str | None
    """Conteúdo do documento."""

    source: str
    """Fonte do documento."""

    object: Object
    """Informações de objeto."""