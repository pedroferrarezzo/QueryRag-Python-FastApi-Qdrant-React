from pydantic import BaseModel, ConfigDict, Field

from .object_dto import ObjectDto

class MetadataDto(BaseModel):
    """Classe para armazenar metadados de um documento recuperado durante o RAG."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "application/pdf",
                "chunk": "Trecho do documento vetorizado.",
                "source": "relatorio.pdf",
                "object": {
                    "key": "objects/relatorio.pdf",
                    "url": "https://minio.local/objects/relatorio.pdf",
                    "include_in_prompt": False,
                },
            }
        }
    )

    type: str = Field(description="Tipo do documento.")
    chunk: str | None = Field(default=None, description="Conteúdo do documento.")
    source: str = Field(description="Fonte do documento.")
    object: ObjectDto = Field(description="Informações de objeto.")