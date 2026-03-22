class IngestResultDto:
    """Classe para representar o resultado de ingestão de um documento."""
 
    def __init__(self, chunks_stored: int):
        """Inicializa um objeto."""
 
        """Número de chunks armazenados."""
        self.chunks_stored = chunks_stored