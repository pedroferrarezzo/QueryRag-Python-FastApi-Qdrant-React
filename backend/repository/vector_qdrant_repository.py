import uuid
import numpy as np

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from model import Document, Metadata

from config.env import QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION
from service.embedding_service import EMBEDDING_DIMENSION

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Garante que a collection exista (não recria se já existir)
def init_collection():
    collections = client.get_collections().collections
    exists = any(c.name == QDRANT_COLLECTION for c in collections)

    if not exists:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMENSION,
                distance=Distance.COSINE  # similaridade de cosseno
            ),
        )

# Inicializa ao subir o módulo
init_collection()

def add_vector(vector_dto):
    vector = np.array(vector_dto.vector).astype("float32")

    client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),  # ID único
                vector=vector,
                payload={
                    "type": vector_dto.type,
                    "chunk": vector_dto.chunk,
                    "source": vector_dto.source,
                },
            )
        ],
    )


def search_vector(vector, k=5):

    vector = np.array(vector).astype("float32")

    results = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=vector,
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
                ),
                score=float(result.score),
            )
        )

    return documents