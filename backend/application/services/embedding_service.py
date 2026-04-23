import re
from typing import List, Union
from domain.exceptions import InvalidValueException, LmmException
from infrastructure.config.env_config import CHUNK_LIST_MAX_LENGTH
from domain.ports.driven import EmbeddingModel
from application.ports.driving import EmbeddingUseCase

class EmbeddingService(EmbeddingUseCase):
    """Serviço responsável por orquestrar a geração de embeddings de forma agnóstica ao provedor de embeddings."""

    def __init__(self, repository: EmbeddingModel):
        """Inicializa o serviço com uma instância do repositório de embeddings."""
        self._repository = repository

    async def get_vector(self, content: str | bytes, mime_type: str | None = None) -> list[float]:
        """Gera um vetor de embedding a partir do conteúdo fornecido de forma independente do provedor."""

        if not content:
            raise InvalidValueException("O conteúdo não pode ser vazio para gerar um embedding.")

        if isinstance(content, bytes):
            if not mime_type:
                raise InvalidValueException("Mime type deve ser fornecido para conteúdos em bytes.")

        try:
            return await self._repository.embed_data(content, mime_type)
        except Exception as e:
            raise LmmException(
                "Erro durante a geração de embedding",
                e
            ) from e

    async def get_vectors(self, contents: List[Union[str, bytes]], mime_types: List[str] = []) -> List[List[float]]:
        """
        Gera embeddings em lote a partir de uma lista de conteúdos (texto ou bytes), de forma independente do provedor.
        """

        if not contents:
            raise InvalidValueException("A lista de conteúdos não pode ser vazia para gerar embeddings.")

        if len(contents) != len(mime_types) and isinstance(contents[0], bytes):
            raise InvalidValueException("contents e mime_types devem ter o mesmo tamanho.")

        # Se mime_types não for fornecido, preenchemos com None para cada conteúdo, assumindo que são textos. Isso é necessário para o bloco zip abaixo
        if len(mime_types) == 0:
            mime_types = [None] * len(contents)

        for content, mime in zip(contents, mime_types):
            if not content:
                raise InvalidValueException("O conteúdo não pode ser vazio para gerar embeddings.")

            if isinstance(content, bytes):
                if not mime:
                    raise InvalidValueException("Mime type deve ser fornecido para conteúdos em bytes.")
                
        try:
            return await self._repository.embed_datas(contents, mime_types)

        except Exception as e:
            raise LmmException(
                "Erro durante a geração de embeddings em lote",
                e
            ) from e
    
    def chunk_text(self, text: str) -> list[str]:
        """Realiza a quebra do texto em chunks semânticos para geração de embeddings."""
        if not text:
            return []

        # 1. quebra semântica
        units = self._split_semantic(text)

        # 3. garantir limite de chunks
        chunks = self._enforce_max_chunks(units, CHUNK_LIST_MAX_LENGTH)

        # 4. validação final
        return [c for c in chunks if self._is_valid_chunk(c)]

    def _split_semantic(self, text: str) -> list[str]:
        """Divide o texto em unidades semânticas, como parágrafos ou sentenças, para preservar o contexto e a coesão do conteúdo, o que pode resultar em chunks mais significativos para a geração de embeddings."""
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        
        # fallback se não houver estrutura
        if len(paragraphs) <= 1:
            sentences = re.split(r'(?<=[.!?])\s+', text)
            return [s.strip() for s in sentences if s.strip()]
        
        return paragraphs

    def _enforce_max_chunks(self, chunks: list[str], max_chunks: int) -> list[str]:
        """Garante que a lista de chunks não exceda o limite máximo, mesclando chunks adjacentes quando necessário."""
        if len(chunks) <= max_chunks:
            return chunks

        factor = len(chunks) // max_chunks + 1
        new_chunks = []

        for i in range(0, len(chunks), factor):
            merged = " ".join(chunks[i:i+factor])
            new_chunks.append(merged)

        return new_chunks

    def _is_valid_chunk(self, text: str) -> bool:
        """Valida se um chunk é útil para gerar um embedding, filtrando chunks muito curtos ou com baixa proporção de caracteres alfanuméricos, o que pode indicar que o chunk é "quebrado" ou contém principalmente símbolos, e portanto pode não ser útil para representação semântica."""
        text = text.strip()

        if len(text) < 50:
            return False

        letters = sum(c.isalnum() for c in text)

        # Calcula a proporção de caracteres alfanuméricos em relação ao total de caracteres. 
        # Se for muito baixo, provavelmente é um chunk "quebrado" ou com muitos símbolos, o que pode indicar que não é um chunk útil para embedding.
        ratio = letters / len(text)

        # mais restritivo
        if ratio < 0.6:
            return False

        # evita chunks "visualmente estruturais"
        if text.count("|") > 3:
            return False

        return True