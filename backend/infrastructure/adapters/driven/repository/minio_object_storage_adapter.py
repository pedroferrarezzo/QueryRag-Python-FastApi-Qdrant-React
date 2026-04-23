from io import BytesIO
import uuid

from infrastructure.config.env_config import MINIO_BUCKET_NAME
from infrastructure.config.minio_config import client, base_console_url

from domain.ports.driven.object_storage_port import ObjectStorageRepository

class MinioObjectStorageRepository(ObjectStorageRepository):
    """Implementação do repositório de armazenamento usando o MinIO."""

    async def upload_file(self, file_content: bytes, file_name: str) -> dict[str, str]:
        """Realiza o upload de um arquivo para o MinIO e retorna um dicionário com informações sobre o arquivo."""

        file_id = str(uuid.uuid4())
        file_key = f"{file_id}_{file_name}"

        await client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=file_key,
            data=BytesIO(file_content),
            length=len(file_content),
        )

        object_console_url = f"{base_console_url}/browser/{MINIO_BUCKET_NAME}/{file_key}"

        return {"key": file_key, "url": object_console_url}

    async def download_file(self, file_key: str) -> bytes:
        """Realiza o download de um arquivo do MinIO usando a chave do arquivo e retorna o conteúdo do arquivo."""

        response = await client.get_object(MINIO_BUCKET_NAME, file_key)
        file_bytes = await response.read()

        return file_bytes