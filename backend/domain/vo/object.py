from pydantic import BaseModel

class Object(BaseModel):
    """Value Object para armazenar informações de um objeto."""
    
    key: str
    """chave de armazenamento do objeto."""

    url: str
    """URL para acessar o objeto armazenado."""

    include_in_prompt: bool
    """Indica se o conteúdo do arquivo deve ser incluído em prompts"""