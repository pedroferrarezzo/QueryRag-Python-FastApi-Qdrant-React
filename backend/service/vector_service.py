from dto import DocumentDto, VectorDto, ObjectStorageDto, MetadataDto
from model import Vector, ObjectStorage
from exceptions import InvalidValueException
from ports import VectorRepository

class VectorService:
    """Serviço para gerenciar vetores e realizar buscas de documentos relacionados."""

    def __init__(self, repository: VectorRepository):
        """Inicializa o serviço com um repositório de vetores."""
        self._repository = repository
    
    async def ingest_vector(self, vector_dto: VectorDto) -> None:
        """Adiciona um vetor com os metadados associados."""
        if not vector_dto.vector:
            raise InvalidValueException("O vetor não pode ser vazio para ser adicionado ao banco de dados.")
        
        object_storage = ObjectStorage(
            key=vector_dto.object_storage.key,
            url=vector_dto.object_storage.url,
            include_in_prompt=vector_dto.object_storage.include_in_prompt
        )
        
        vector = Vector(
            vector=vector_dto.vector,
            type=vector_dto.type,
            chunk=vector_dto.chunk,
            source=vector_dto.source,
            object_storage=object_storage
        )

        await self._repository.add_vector(vector)

    async def ingest_vectors(self, vector_dtos: list[VectorDto]) -> None:
        """Adiciona uma lista de vetores com os metadados associados."""
        if not vector_dtos:
            raise InvalidValueException("A lista de vetores não pode ser vazia para ser adicionada ao banco de dados.")
        
        object_storages = [
            ObjectStorage(
                key=vector_dto.object_storage.key,
                url=vector_dto.object_storage.url,
                include_in_prompt=vector_dto.object_storage.include_in_prompt
            )
            for vector_dto in vector_dtos
        ]
        vectors = [
            Vector(
                vector=vector_dto.vector,
                type=vector_dto.type,
                chunk=vector_dto.chunk,
                source=vector_dto.source,
                object_storage=object_storage
            )
            for vector_dto, object_storage in zip(vector_dtos, object_storages)
        ]

        await self._repository.add_vectors(vectors)

    async def search_documents(self, vector: list[float], k: int = 5) -> list[DocumentDto]:
        """Busca os vetores mais similares e retorna os documentos correspondentes."""
        if not vector:
            raise InvalidValueException("O vetor de consulta não pode ser vazio para realizar a busca.")
        
        documents = await self._repository.search_vector(vector, k)

        object_storage_dtos = [
            ObjectStorageDto(
                key=document.metadata.object_storage.key,
                url=document.metadata.object_storage.url,
                include_in_prompt=document.metadata.object_storage.include_in_prompt
            )
            for document in documents
        ]
        metadata_dtos = [
            MetadataDto(
                source=document.metadata.source,
                chunk=document.metadata.chunk,
                type=document.metadata.type,
                object_storage=object_storage_dto
            )
            for document, object_storage_dto in zip(documents, object_storage_dtos)
        ]
        document_dtos = [
            DocumentDto(
                metadata=metadata_dto,
                score=document.score,
                rerank_score=document.rerank_score
            )
            for document, metadata_dto in zip(documents, metadata_dtos)
        ]

        return document_dtos