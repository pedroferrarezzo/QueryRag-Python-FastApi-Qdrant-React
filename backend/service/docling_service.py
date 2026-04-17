from docling.document_converter import DocumentConverter

from exceptions import InvalidValueException

converter = DocumentConverter()

def extract_text(path: str) -> str:
    """Extrai o texto de um documento usando o Docling."""

    if not path:
        raise InvalidValueException("O caminho do documento não pode ser vazio para extrair o texto.")
    
    result = converter.convert(path)
    return result.document.export_to_text()