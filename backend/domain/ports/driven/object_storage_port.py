from abc import ABC, abstractmethod

class ObjectStorageRepository(ABC):
    """Porta de saída para o repositório de armazenamento de objetos."""

    @abstractmethod
    async def upload_file(self, file_content: bytes, file_name: str) -> dict[str, str]:
        """Realiza o upload de um arquivo e retorna um dicionário com informações sobre o arquivo."""
        pass

    @abstractmethod
    async def download_file(self, file_key: str) -> bytes:
        """Realiza o download de um arquivo usando a chave e retorna seu conteúdo."""
        pass