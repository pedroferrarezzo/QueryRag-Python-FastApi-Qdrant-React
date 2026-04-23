from pydantic import BaseModel
from .object_dto import ObjectDto

class VectorDto(BaseModel):
    """Classe para representar um conteúdo vetorizado via embedding."""

    vector: list[float]
    """vetor resultante do embedding."""

    type: str
    """tipo do conteúdo (ex: texto, imagem, etc)."""
    
    chunk: str | None = None
    """conteúdo a ser vetorizado."""

    source: str
    """fonte do conteúdo (ex: nome do arquivo, URL, etc)."""

    object: ObjectDto
    """Informações de objeto do conteúdo original."""
        