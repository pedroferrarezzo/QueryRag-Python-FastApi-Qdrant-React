from miniopy_async import Minio
from infrastructure.config.env_config import MINIO_CONSOLE_PORT, MINIO_HOST, MINIO_PORT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE, MINIO_BUCKET_NAME

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