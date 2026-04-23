from pydantic import BaseModel
from .object import Object

class Vector(BaseModel):
    """Classe para representar um conteúdo vetorizado via embedding."""

    vector: list[float]
    """vetor resultante do embedding."""

    type: str
    """tipo do conteúdo (ex: texto, imagem, etc)."""
    
    chunk: str | None = None
    """conteúdo a ser vetorizado."""

    source: str
    """fonte do conteúdo (ex: nome do arquivo, URL, etc)."""

    object: Object
    """Informações de objeto do conteúdo original."""
        