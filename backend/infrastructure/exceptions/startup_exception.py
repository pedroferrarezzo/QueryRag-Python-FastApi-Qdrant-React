class StartupException(Exception):
    """Exceção personalizada para erros de inicialização da aplicação."""

    def __init__(self, message: str, original_exception: Exception | None = None):
        """Inicializa a StartupException com uma mensagem personalizada."""
        
        super().__init__(message)
        self.original_exception = original_exception