from pydantic import BaseModel

class Metadata(BaseModel):
    """Classe para armazenar metadados de um documento recuperado durante o RAG."""

    type: str
    """Tipo do documento."""

    chunk: str | None
    """Conteúdo do documento."""

    source: str
    """Fonte do documento."""

    object_storage_key: str | None
    """chave de armazenamento em object storage, se aplicável."""