from pydantic import BaseModel

class ObjectStorage(BaseModel):
    """Classe para armazenar informações de armazenamento em object storage."""
    
    key: str
    """chave de armazenamento em object storage."""

    url: str
    """URL para acessar o objeto armazenado."""

    include_in_prompt: bool
    """Indica se o conteúdo do arquivo deve ser incluído em prompts"""