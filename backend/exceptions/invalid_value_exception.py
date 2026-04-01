class InvalidValueException(Exception):
    """Exceção personalizada para erros relacionados a valores inválidos."""

    def __init__(self, message: str, original_exception: Exception | None = None):
        """Inicializa a InvalidValueException com uma mensagem personalizada."""

        super().__init__(message)
        self.original_exception = original_exception