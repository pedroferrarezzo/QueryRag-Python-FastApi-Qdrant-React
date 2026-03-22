class Metadata:
    """Classe para armazenar metadados de um documento recuperado durante o RAG."""

    def __init__(self, type: str, chunk: str, source: str):
        """Inicializa um objeto metadata."""

        """Tipo do documento."""
        self.type = type

        """Conteúdo do documento."""
        self.chunk = chunk

        """Fonte do documento."""
        self.source = source