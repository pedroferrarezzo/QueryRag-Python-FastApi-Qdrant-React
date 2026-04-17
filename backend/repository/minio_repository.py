

from miniopy_async import Minio
from io import BytesIO
import uuid
from config.env import MINIO_CONSOLE_PORT, MINIO_HOST, MINIO_PORT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE, MINIO_BUCKET_NAME
from exceptions import InvalidValueException

client = Minio(
    endpoint=f"{MINIO_HOST}:{MINIO_PORT}",
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE,
)

scheme = "https" if MINIO_SECURE else "http"
base_console_url = f"{scheme}://{MINIO_HOST}:{MINIO_CONSOLE_PORT}"

async def initialize_minio():
    """Inicializa o MinIO, criando o bucket se ele não existir."""
    
    if not await client.bucket_exists(MINIO_BUCKET_NAME):
        await client.make_bucket(MINIO_BUCKET_NAME)

async def upload_file(file_content: bytes, file_name: str) -> dict[str, str]:
    """Realiza o upload de um arquivo para o MinIO e retorna a chave do arquivo."""

    if not file_content or not file_name:
        raise InvalidValueException("O conteúdo do arquivo e o nome do arquivo são obrigatórios.")

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

async def download_file(file_key: str) -> bytes:
    """Realiza o download de um arquivo do MinIO usando a chave do arquivo e retorna o conteúdo do arquivo."""

    if not file_key:
        raise InvalidValueException("A chave do arquivo é obrigatória para realizar o download.")

    response = await client.get_object(MINIO_BUCKET_NAME, file_key)
    file_bytes = await response.read()

    return file_bytes