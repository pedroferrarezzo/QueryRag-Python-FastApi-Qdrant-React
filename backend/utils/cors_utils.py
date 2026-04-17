from urllib.parse import urlparse
from exceptions import StartupException

DEFAULT_PORTS = {
    "http": 80,
    "https": 443,
}

def get_cors_origins(query_rag_frontend_url: str):
    """Retorna origins válidos para CORS a partir da URL do frontend."""

    parsed = urlparse(query_rag_frontend_url)

    if not parsed.scheme or not parsed.hostname:
        raise StartupException(f"Formato da URL inválido: {query_rag_frontend_url}")

    origins = set()

    if parsed.port and parsed.port != DEFAULT_PORTS.get(parsed.scheme, None):
        origins.add(f"{parsed.scheme}://{parsed.hostname}:{parsed.port}")
    else:
        origins.add(f"{parsed.scheme}://{parsed.hostname}")

    return list(origins)