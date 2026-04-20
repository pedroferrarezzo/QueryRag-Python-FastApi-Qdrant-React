from pydantic import BaseModel

from .object import Object

class Metadata(BaseModel):
    """Classe para armazenar metadados de um documento recuperado durante o RAG."""

    type: str
    """Tipo do documento."""

    chunk: str | None
    """Conteúdo do documento."""

    source: str
    """Fonte do documento."""

    object: Object
    """Informações de objeto."""