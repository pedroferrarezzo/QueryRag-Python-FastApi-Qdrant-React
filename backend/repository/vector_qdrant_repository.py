import uuid
import numpy as np

from qdrant_client import AsyncQdrantClient 
from qdrant_client.models import Distance, VectorParams, PointStruct

from dto.vector_dto import VectorDto
from exceptions.invalid_value_exception import InvalidValueException
from model import Document, Metadata

from config.env import QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION
from service.embedding_service import EMBEDDING_DIMENSION

client = AsyncQdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Garante que a collection exista (não recria se já existir)
async def init_collection():
    """Verifica se a coleção do Qdrant existe e a cria se necessário."""

    collections = (await client.get_collections()).collections
    exists = any(c.name == QDRANT_COLLECTION for c in collections)

    if not exists:
        await client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMENSION,
                # Define que o Qdrant deve calcular a proximidade entre os vetores usando o cosseno do ângulo entre eles
                distance=Distance.COSINE
            ),
        )

async def add_vector(vector_dto: VectorDto):
    """Adiciona um vetor ao Qdrant com os metadados associados."""

    if not vector_dto.vector:
        raise InvalidValueException("O vetor não pode ser vazio para ser adicionado ao banco de dados.")

    vector = np.array(vector_dto.vector).astype("float32")

    await client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "type": vector_dto.type,
                    "chunk": vector_dto.chunk,
                    "source": vector_dto.source,
                    "object_storage": {
                        "key": vector_dto.object_storage.key,
                        "url": vector_dto.object_storage.url,
                        "include_in_prompt": vector_dto.object_storage.include_in_prompt
                    }
                },
            )
        ],
    )

async def add_vectors(vector_dtos: list[VectorDto]):
    """Adiciona vetores ao Qdrant com os metadados associados."""

    if not vector_dtos:
        raise InvalidValueException("A lista de vetores não pode ser vazia para ser adicionada ao banco de dados.")

    points = []
    for vector_dto in vector_dtos:
        vector = np.array(vector_dto.vector).astype("float32")
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "type": vector_dto.type,
                    "chunk": vector_dto.chunk,
                    "source": vector_dto.source,
                    "object_storage": {
                        "key": vector_dto.object_storage.key,
                        "url": vector_dto.object_storage.url,
                        "include_in_prompt": vector_dto.object_storage.include_in_prompt
                    }
                },
            )
        )

    await client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=points,
    )


async def search_vector(vector: list[float], k: int = 5) -> list[Document]:
    """Busca os vetores mais similares no Qdrant e retorna os documentos correspondentes."""

    if not vector:
        raise InvalidValueException("O vetor de consulta não pode ser vazio para realizar a busca.")

    vector = np.array(vector).astype("float32")

    results = await client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=vector,
        # instrui o motor de busca a retornar os vetores com a maior pontuação de similaridade em relação ao vetor de consulta
        limit=k,
    )

    documents = []

    for result in results.points:
        payload = result.payload or {}

        documents.append(
            Document(
                metadata=Metadata(
                    type=payload.get("type"),
                    chunk=payload.get("chunk"),
                    source=payload.get("source"),
                    object_storage=payload.get("object_storage")
                ),
                score=float(result.score),
                rerank_score=None  # Reranking pode ser implementado posteriormente
            )
        )

    return documents