class LmmException(Exception):
    """Exceção personalizada para erros relacionados ao LMM (Large Multimodal Model)."""

    def __init__(self, message: str, original_exception: Exception | None = None):
        """Inicializa a LmmException com uma mensagem personalizada e opcionalmente inclui detalhes da exceção original para facilitar o diagnóstico de erros relacionados ao LMM."""
        
        full_message = message
        if original_exception:
            full_message = f"{message} | Detalhes: {str(original_exception)}"
        super().__init__(full_message)
        self.original_exception = original_exception