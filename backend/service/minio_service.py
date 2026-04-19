from exceptions import InvalidValueException

from repository.minio_repository import upload_file, download_file

async def upload_object(file_content: bytes, file_name: str) -> dict[str, str]:
    """Realiza o upload de um objeto e retorna a chave do arquivo."""
    if not file_content or not file_name:
        raise InvalidValueException("O conteúdo do arquivo e o nome do arquivo são obrigatórios.")
    
    return await upload_file(file_content, file_name)

async def download_object(file_key: str) -> bytes:
    """Realiza o download de um objeto usando a chave do arquivo e retorna o conteúdo dele."""
    if not file_key:
        raise InvalidValueException("A chave do arquivo é obrigatória para realizar o download.")
    
    return await download_file(file_key)