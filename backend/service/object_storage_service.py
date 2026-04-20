from exceptions import InvalidValueException
from ports import ObjectStorageRepository

class ObjectStorageService:
    """Serviço responsável por operações de armazenamento de objetos, como upload e download de arquivos."""

    def __init__(self, repository: ObjectStorageRepository):
        """Inicializa o serviço com uma instância do repositório de armazenamento de objetos."""
        self._repository = repository

    async def upload_object(self, file_content: bytes, file_name: str) -> dict[str, str]:
        """Realiza o upload de um objeto e retorna a chave do arquivo."""
        if not file_content or not file_name:
            raise InvalidValueException("O conteúdo do arquivo e o nome do arquivo são obrigatórios.")
        
        return await self._repository.upload_file(file_content, file_name)

    async def download_object(self, file_key: str) -> bytes:
        """Realiza o download de um objeto usando a chave do arquivo e retorna o conteúdo dele."""
        if not file_key:
            raise InvalidValueException("A chave do arquivo é obrigatória para realizar o download.")
        
        return await self._repository.download_file(file_key)