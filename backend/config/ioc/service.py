from service import EmbeddingService, VectorService, DocumentParserService, LmmService, ObjectStorageService
from adapters import GeminiEmbeddingModel, QdrantVectorRepository, DoclingDocumentParser, GeminiLmmModel, MinioObjectStorageRepository

def get_embedding_service() -> EmbeddingService:
    """Factory function para obter a implementação do serviço de embedding."""
    return EmbeddingService(GeminiEmbeddingModel())

def get_vector_service() -> VectorService:
    """Factory function para obter a implementação do serviço de vetor."""
    return VectorService(QdrantVectorRepository())

def get_document_parser_service() -> DocumentParserService:
    """Factory function para obter a implementação do serviço de parser de documentos."""
    return DocumentParserService(DoclingDocumentParser())

def get_lmm_service() -> LmmService:
    """Factory function para obter a implementação do serviço de LMM."""
    lmm_adapter = GeminiLmmModel(MinioObjectStorageRepository())

    return LmmService(lmm_adapter)

def get_object_storage_service() -> ObjectStorageService:
    """Factory function para obter a implementação do serviço de armazenamento de objetos."""
    return ObjectStorageService(MinioObjectStorageRepository())