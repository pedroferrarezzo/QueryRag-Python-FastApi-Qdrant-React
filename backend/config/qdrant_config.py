from qdrant_client import AsyncQdrantClient 
from qdrant_client.models import Distance, VectorParams

from config.env_config import QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION, EMBEDDING_DIMENSION

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