from pydantic import BaseModel, ConfigDict, Field

class IngestResultDto(BaseModel):
    """Classe para representar o resultado de ingestão de um documento."""

    model_config = ConfigDict(
        json_schema_extra={"example": {"chunks_stored": 12}}
    )

    chunks_stored: int = Field(description="Número de chunks armazenados.", examples=[12])