from typing import List, Union
from google.genai import types

from infrastructure.config.gemini_config import client
from infrastructure.config.env_config import GEMINI_EMBEDDING_MODEL, EMBEDDING_DIMENSION

from domain.ports.driven import EmbeddingModel

class GeminiEmbeddingModel(EmbeddingModel):
    """Implementação do modelo de embeddings utilizando o Google Gemini."""

    async def embed_data(
        self,
        content: str | bytes,
        mime_type: str | None = None
    ) -> list[float]:
        """Gera um vetor de embedding a partir de um único conteúdo."""

        if isinstance(content, bytes):
            part = types.Part.from_bytes(data=content, mime_type=mime_type)
        else:
            part = types.Part.from_text(text=content)

        response = await client.aio.models.embed_content(
            model=GEMINI_EMBEDDING_MODEL,
            contents=part,
            config={'output_dimensionality': EMBEDDING_DIMENSION}
        )

        return response.embeddings[0].values

    async def embed_datas(
        self,
        contents: List[Union[str, bytes]],
        mime_types: List[str] = []
    ) -> List[List[float]]:
        """Gera embeddings em lote a partir de múltiplos conteúdos."""

        # Se mime_types não for fornecido, preenchemos com None para cada conteúdo, assumindo que são textos. Isso é necessário para o bloco zip abaixo
        if len(mime_types) == 0:
            mime_types = [None] * len(contents)

        parts = []
        for content, mime in zip(contents, mime_types):
            if isinstance(content, bytes):
                parts.append(types.Part.from_bytes(data=content, mime_type=mime))
            else:
                parts.append(types.Part.from_text(text=content))

        response = await client.aio.models.embed_content(
            model=GEMINI_EMBEDDING_MODEL,
            contents=parts,
            config={'output_dimensionality': EMBEDDING_DIMENSION}
        )

        return [embedding.values for embedding in response.embeddings]