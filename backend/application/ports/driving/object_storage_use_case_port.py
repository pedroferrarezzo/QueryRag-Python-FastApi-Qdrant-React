from abc import ABC, abstractmethod

class ObjectStorageUseCase(ABC):
    """Porta de entrada para armazenamento de objetos."""

    @abstractmethod
    async def upload_object(self, file_content: bytes, file_name: str) -> dict[str, str]:
        """Realiza o upload de um objeto e retorna um dicionário com informações sobre o arquivo."""
        pass

    @abstractmethod
    async def download_object(self, file_key: str) -> bytes:
        """Realiza o download de um objeto usando a chave do arquivo e retorna o conteúdo dele."""
        pass