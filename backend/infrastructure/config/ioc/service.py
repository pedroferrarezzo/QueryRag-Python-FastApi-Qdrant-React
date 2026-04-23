from infrastructure.adapters.driven import GeminiEmbeddingModel, QdrantVectorRepository, DoclingDocumentParser, GeminiLmmModel, MinioObjectStorageRepository
from application.ports.driving import EmbeddingUseCase, VectorUseCase, DocumentParserUseCase, LmmUseCase, ObjectStorageUseCase
from application.services import EmbeddingService, VectorService, DocumentParserService, LmmService, ObjectStorageService

def get_embedding_service() -> EmbeddingUseCase:
    """Factory function para obter a implementação do serviço de embedding."""
    return EmbeddingService(GeminiEmbeddingModel())

def get_vector_service() -> VectorUseCase:
    """Factory function para obter a implementação do serviço de vetor."""
    return VectorService(QdrantVectorRepository())

def get_document_parser_service() -> DocumentParserUseCase:
    """Factory function para obter a implementação do serviço de parser de documentos."""
    return DocumentParserService(DoclingDocumentParser())

def get_lmm_service() -> LmmUseCase:
    """Factory function para obter a implementação do serviço de LMM."""
    lmm_adapter = GeminiLmmModel(MinioObjectStorageRepository())

    return LmmService(lmm_adapter)

def get_object_storage_service() -> ObjectStorageUseCase:
    """Factory function para obter a implementação do serviço de armazenamento de objetos."""
    return ObjectStorageService(MinioObjectStorageRepository())