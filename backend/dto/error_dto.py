from datetime import datetime
from pydantic import BaseModel

class ErrorDto(BaseModel):
    """Classe para representar um erro ocorrido durante o processamento de uma requisição."""
    
    message: str
    """Mensagem de erro detalhada para o cliente."""

    timestamp: str = datetime.now().isoformat()
    """Timestamp do erro, no formato ISO 8601."""

    type: str = "error"
    """Tipo do DTO, sempre 'error' para esta classe."""