from pydantic import BaseModel

class IngestResultDto(BaseModel):
    """Classe para representar o resultado de ingestão de um documento."""
    
    chunks_stored: int
    """Número de chunks armazenados."""