from pydantic import BaseModel

class ObjectStorageDto(BaseModel):
    """Classe para representar informações de armazenamento em object storage."""
    
    key: str
    """Chave de armazenamento em object storage."""

    url: str
    """URL de acesso ao arquivo armazenado."""

    include_in_prompt: bool
    """Indica se o conteúdo do arquivo deve ser incluído em prompts"""