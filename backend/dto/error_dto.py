from datetime import datetime

class ErrorDto:
    """Classe para representar um erro ocorrido durante o processamento de uma requisição."""
    
    def __init__(self, message: str):
        """Inicializa um objeto."""
        self.message = message
        self.timestamp = datetime.now().isoformat()