from model.metadata import Metadata

class Document:
    """Classe para representar um documento recuperado durante o RAG, incluindo seu conteúdo, metadados e pontuação."""

    def __init__(self, metadata: Metadata, score:float, rerank_score:float =None):
        """Inicializa um objeto document."""

        """Metadados do documento recuperado."""
        self.metadata = metadata

        """Pontuação do documento."""
        self.score = score

        """Pontuação de reranking do documento (opcional)."""
        self.rerank_score = rerank_score