from pydantic import BaseModel
from .metadata_dto import MetadataDto

class DocumentDto(BaseModel):
    """Classe para representar um documento recuperado durante o RAG, incluindo seu conteúdo, metadados e pontuação."""

    metadata: MetadataDto
    """Metadados do documento recuperado."""

    score: float
    """Pontuação do documento."""

    rerank_score: float | None
    """Pontuação de reranking do documento (opcional)."""