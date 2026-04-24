from pydantic import BaseModel, ConfigDict, Field

class ObjectDto(BaseModel):
    """Classe para armazenar informações de um objeto."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "key": "objects/relatorio.pdf",
                "url": "https://minio.local/objects/relatorio.pdf",
                "include_in_prompt": False,
            }
        }
    )

    key: str = Field(description="Chave de armazenamento do objeto.")
    url: str = Field(description="URL para acessar o objeto armazenado.")
    include_in_prompt: bool = Field(
        description="Indica se o conteúdo do arquivo deve ser incluído em prompts."
    )