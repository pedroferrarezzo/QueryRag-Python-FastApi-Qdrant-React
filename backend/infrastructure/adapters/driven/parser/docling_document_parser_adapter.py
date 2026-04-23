from domain.ports.driven import DocumentParser
from infrastructure.config.docling_config import converter

class DoclingDocumentParser(DocumentParser):
    """Implementação de parser usando Docling."""

    def extract_text(self, path: str) -> str:
        """Extrai o texto de um documento usando Docling."""

        result = converter.convert(path)
        return result.document.export_to_text()