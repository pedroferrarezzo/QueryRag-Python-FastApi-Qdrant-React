from pydantic import BaseModel
from model.metadata import Metadata

class Document(BaseModel):
    """Classe para representar um documento recuperado durante o RAG, incluindo seu conteúdo, metadados e pontuação."""

    metadata: Metadata
    """Metadados do documento recuperado."""

    score: float
    """Pontuação do documento."""

    rerank_score: float | None
    """Pontuação de reranking do documento (opcional)."""