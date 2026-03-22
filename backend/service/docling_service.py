from docling.document_converter import DocumentConverter

converter = DocumentConverter()

def extract_text(path: str) -> str:
    result = converter.convert(path)
    return result.document.export_to_text()