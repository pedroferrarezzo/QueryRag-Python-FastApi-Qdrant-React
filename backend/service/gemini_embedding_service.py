from google import genai
from google.genai import types
from typing import List, Union
from config.env_config import GEMINI_API_KEY
from exceptions import InvalidValueException, LmmException

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-embedding-2-preview"

# Dimensão dos vetores gerados pelo modelo de embedding
# A dimensão corresponde na prática a quantidade de índices do vetor de embedding
# https://ai.google.dev/gemini-api/docs/embeddings?hl=pt-br#control-embedding-size
EMBEDDING_DIMENSION = 3072

async def embed_data(content: str | bytes, mime_type: str | None = None) -> list[float]:
    """Gera um vetor de embedding a partir do conteúdo fornecido, utilizando o modelo de embedding multi-modal do Gemini."""

    if not content:
        raise InvalidValueException("O conteúdo não pode ser vazio para gerar um embedding.")

    if isinstance(content, bytes):
        if not mime_type:
            raise InvalidValueException("Mime type deve ser fornecido para conteúdos em bytes.")
        part = types.Part.from_bytes(data=content, mime_type=mime_type)
    else:
        part = types.Part.from_text(text=content)

    try:
        response = await client.aio.models.embed_content(
            model=MODEL_ID,
            contents=part,
            config={'output_dimensionality': EMBEDDING_DIMENSION}
        )

        return response.embeddings[0].values

    except Exception as e:
        raise LmmException(
            "Erro durante a geração de embedding com a API do Gemini",
            e
        ) from e


async def embed_datas(contents: List[Union[str, bytes]], mime_types: List[str] = []) -> List[List[float]]:
    """
    Gera embeddings em lote a partir de uma lista de conteúdos (texto ou bytes),utilizando o modelo multi-modal do Gemini.
    """

    if not contents:
        raise InvalidValueException("A lista de conteúdos não pode ser vazia para gerar embeddings.")

    if len(contents) != len(mime_types) and isinstance(contents[0], bytes):
        raise InvalidValueException("contents e mime_types devem ter o mesmo tamanho.")

    # Se mime_types não for fornecido, preenchemos com None para cada conteúdo, assumindo que são textos. Isso é necessário para o bloco zip abaixo
    if len(mime_types) == 0:
        mime_types = [None] * len(contents)

    parts = []
    for content, mime in zip(contents, mime_types):
        if not content:
            raise InvalidValueException("O conteúdo não pode ser vazio para gerar embeddings.")

        if isinstance(content, bytes):
            if not mime:
                raise InvalidValueException("Mime type deve ser fornecido para conteúdos em bytes.")
            parts.append(types.Part.from_bytes(data=content, mime_type=mime))
        else:
            parts.append(types.Part.from_text(text=content))

    try:
        response = await client.aio.models.embed_content(
            model=MODEL_ID,
            contents=parts,
            config={'output_dimensionality': EMBEDDING_DIMENSION}
        )

        return [embedding.values for embedding in response.embeddings]

    except Exception as e:
        raise LmmException(
            "Erro durante a geração de embeddings em lote com a API do Gemini",
            e
        ) from e