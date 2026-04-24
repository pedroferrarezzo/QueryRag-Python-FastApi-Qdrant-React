from pydantic import BaseModel, ConfigDict, Field
from .metadata_dto import MetadataDto

class DocumentDto(BaseModel):
    """Classe para representar um documento recuperado durante o RAG, incluindo seu conteúdo, metadados e pontuação."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "metadata": {
                    "type": "application/pdf",
                    "chunk": "Trecho do documento vetorizado.",
                    "source": "relatorio.pdf",
                    "object": {
                        "key": "objects/relatorio.pdf",
                        "url": "https://minio.local/objects/relatorio.pdf",
                        "include_in_prompt": False,
                    },
                },
                "score": 0.87,
                "rerank_score": 0.93,
            }
        }
    )

    metadata: MetadataDto = Field(description="Metadados do documento recuperado.")
    score: float = Field(description="Pontuação do documento.", examples=[0.87])
    rerank_score: float | None = Field(
        default=None,
        description="Pontuação de reranking do documento (opcional).",
        examples=[0.93],
    )