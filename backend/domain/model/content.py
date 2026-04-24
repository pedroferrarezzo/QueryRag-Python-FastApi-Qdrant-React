from pydoc import text
import re
from pydantic import BaseModel, model_validator
from domain.vo import Chunk
from domain.exceptions import InvalidValueException

class Content(BaseModel):
    """Entidade de domínio para representar um conteúdo que será vetorizado via embedding."""

    chunk_max_length: int
    """Número máximo de chunks que um conteúdo pode ser dividido para geração de embeddings"""

    chunks: list[Chunk]
    """Lista de chunks que serão vetorizados."""

    @model_validator(mode="before")
    @classmethod
    def parse_input(cls, value):
        if isinstance(value, dict) and "chunks" not in value:
            content_value = value.get("content")
            max_len = value.get("chunk_max_length", 50)

            if not content_value or not content_value.strip():
                raise InvalidValueException("O texto não pode ser vazio.")
        
            if max_len <= 0:
                raise InvalidValueException("O tamanho máximo do chunk deve ser maior que zero.")
            
            if isinstance(content_value, (str, bytes)):
                chunks = []
                if isinstance(content_value, str):
                    raw_chunks = cls._chunk_text(content_value, max_len)
                    for raw_chunk in raw_chunks:
                        try:
                            chunk = Chunk(content=raw_chunk)
                            chunks.append(chunk)
                        except InvalidValueException:
                            continue
                        
                    return {"chunks": chunks, "chunk_max_length": max_len}
                    
                chunks.append(Chunk(content=content_value))
                return {"chunks": chunks, "chunk_max_length": max_len}

        return value
    
    @staticmethod
    def _chunk_text(text: str, max_chunks: int) -> list[str]:
        """Realiza a quebra do texto em chunks semânticos para geração de embeddings."""
        if not text:
            return []

        # 1. quebra semântica
        units = Content._split_semantic(text)

        # 2. garantir limite de chunks
        return Content._enforce_max_chunks(units, max_chunks)

    @staticmethod
    def _split_semantic(text: str) -> list[str]:
        """Divide o texto em unidades semânticas, como parágrafos ou sentenças, para preservar o contexto e a coesão do conteúdo, o que pode resultar em chunks mais significativos para a geração de embeddings."""
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        
        # fallback se não houver estrutura
        if len(paragraphs) <= 1:
            sentences = re.split(r'(?<=[.!?])\s+', text)
            return [s.strip() for s in sentences if s.strip()]
        
        return paragraphs

    @staticmethod
    def _enforce_max_chunks(chunks: list[str], max_chunks: int) -> list[str]:
        """Garante que a lista de chunks não exceda o limite máximo, mesclando chunks adjacentes quando necessário."""
        if len(chunks) <= max_chunks:
            return chunks

        factor = (len(chunks) + max_chunks - 1) // max_chunks
        new_chunks = []

        for i in range(0, len(chunks), factor):
            merged = " ".join(chunks[i:i+factor])
            new_chunks.append(merged)

        return new_chunks