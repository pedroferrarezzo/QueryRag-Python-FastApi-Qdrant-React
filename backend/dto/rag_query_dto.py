from pydantic import BaseModel
from model.document import Document

class RagQueryDto(BaseModel):
    """Classe para representar o resultado de consulta de RAG."""
 
    query: str
    """Texto da consulta realizada."""

    documents: list[Document]
    """Lista de documentos recuperados como resposta à consulta."""