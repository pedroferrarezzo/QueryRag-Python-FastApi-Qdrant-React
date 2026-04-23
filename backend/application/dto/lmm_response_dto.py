from pydantic import BaseModel
from .document_dto import DocumentDto

class LmmResponseDto(BaseModel):
    """Classe para representar o resultado de consulta ao LMM."""
    
    type: str
    """Tipo do conteúdo retornado (ex: 'text', 'binary', etc.)"""
    
    data: str
    """Conteúdo retornado, que pode ser texto ou dados binários codificados em base64."""

    mime_type: str | None = None
    """Tipo MIME do conteúdo, presente apenas para dados binários."""

    timestamp: str
    """Timestamp da resposta, no formato ISO 8601."""

    questionId: str
    """ID da pergunta associada à resposta."""

    documents: list[DocumentDto]
    """Documentos recuperados durante o RAG e utilizados pelo LMM para gerar a resposta."""