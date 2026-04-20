from typing import List, Union
from exceptions import InvalidValueException, LmmException
from ports import EmbeddingModel

class EmbeddingService:
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