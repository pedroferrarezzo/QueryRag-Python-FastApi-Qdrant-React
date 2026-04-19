from pydantic import BaseModel

from .object_storage_dto import ObjectStorageDto

class MetadataDto(BaseModel):
    """Classe para armazenar metadados de um documento recuperado durante o RAG."""

    type: str
    """Tipo do documento."""

    chunk: str | None
    """Conteúdo do documento."""

    source: str
    """Fonte do documento."""

    object_storage: ObjectStorageDto
    """Informações de armazenamento em object storage."""