from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ErrorDto(BaseModel):
    """Classe para representar um erro ocorrido durante o processamento de uma requisição."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "data": "Forneça um prompt ou um arquivo para pesquisa.",
                "timestamp": "2026-04-24T10:30:00",
                "type": "error",
            }
        }
    )

    data: str = Field(description="Mensagem de erro detalhada para o cliente.")
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp do erro, no formato ISO 8601.",
    )
    type: str = Field(default="error", description="Tipo do DTO, sempre 'error'.")