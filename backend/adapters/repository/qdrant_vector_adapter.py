import uuid
import numpy as np
from qdrant_client.models import PointStruct

from model import Document, Metadata, Vector
from config.env_config import QDRANT_COLLECTION
from config.qdrant_config import client

from ports.vector_port import VectorRepository

class QdrantVectorRepository(VectorRepository):
    """Implementação do repositório de vetores usando o Qdrant."""

    async def add_vector(self, vector_object: Vector) -> None:
        """Adiciona um vetor ao Qdrant com os metadados associados."""

        vector = np.array(vector_object.vector).astype("float32")

        await client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "type": vector_object.type,
                        "chunk": vector_object.chunk,
                        "source": vector_object.source,
                        "object": {
                            "key": vector_object.object.key,
                            "url": vector_object.object.url,
                            "include_in_prompt": vector_object.object.include_in_prompt
                        }
                    },
                )
            ],
        )

    async def add_vectors(self, vectors: list[Vector]) -> None:
        """Adiciona vetores ao Qdrant com os metadados associados."""

        points = []
        for vector_object in vectors:
            vector = np.array(vector_object.vector).astype("float32")
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "type": vector_object.type,
                        "chunk": vector_object.chunk,
                        "source": vector_object.source,
                        "object": {
                            "key": vector_object.object.key,
                            "url": vector_object.object.url,
                            "include_in_prompt": vector_object.object.include_in_prompt
                        }
                    },
                )
            )

        await client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=points,
        )

    async def search_vector(self, vector: list[float], k: int = 5) -> list[Document]:
        """Busca os vetores mais similares no Qdrant e retorna os documentos correspondentes."""

        np_vector = np.array(vector).astype("float32")

        results = await client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=np_vector,
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
                        object=payload.get("object")
                    ),
                    score=float(result.score),
                    rerank_score=None  # Reranking pode ser implementado posteriormente
                )
            )

        return documents