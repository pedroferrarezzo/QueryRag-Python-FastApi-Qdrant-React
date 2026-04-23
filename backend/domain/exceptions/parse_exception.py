class ParseException(Exception):
    """Exceção personalizada para erros de parsing de documentos."""

    def __init__(self, message: str, original_exception: Exception | None = None):
        """Inicializa a ParseException com uma mensagem personalizada."""
        
        super().__init__(message)
        self.original_exception = original_exception