from abc import ABC, abstractmethod

class ObjectStorageRepository(ABC):
    """Interface para o repositório de armazenamento de objetos."""

    @abstractmethod
    async def upload_file(self, file_content: bytes, file_name: str) -> dict[str, str]:
        """Realiza o upload de um arquivo e retorna a chave e URL do arquivo."""
        pass

    @abstractmethod
    async def download_file(self, file_key: str) -> bytes:
        """Realiza o download de um arquivo usando a chave e retorna seu conteúdo."""
        pass