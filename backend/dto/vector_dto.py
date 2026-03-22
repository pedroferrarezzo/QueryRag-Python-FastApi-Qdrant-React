class VectorDto:
    """Classe para representar um conteúdo vetorizado via embedding."""
    
    def __init__(self, vector, type, chunk, source=None):
        """Inicializa um objeto."""

        """vetor resultante do embedding."""
        self.vector = vector

        """tipo do conteúdo (ex: texto, imagem, etc)."""
        self.type = type
        
        """conteúdo a ser vetorizado."""
        self.chunk = chunk

        """fonte do conteúdo (ex: nome do arquivo, URL, etc)."""
        self.source = source