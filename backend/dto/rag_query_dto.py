class RagQueryDto:
    """Classe para representar o resultado de consulta de RAG."""
 
    def __init__(self, query: str, documents: list):
        """Inicializa um objeto."""

        """Texto da consulta realizada."""
        self.query = query

        """Lista de documentos recuperados como resposta à consulta."""
        self.documents = documents