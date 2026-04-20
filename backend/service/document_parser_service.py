from exceptions import InvalidValueException
from ports import DocumentParser

class DocumentParserService:
    """Serviço responsável por extração de texto de documentos de forma agnóstica à biblioteca utilizada."""

    def __init__(self, repository: DocumentParser):
        """Inicializa o serviço de extração de texto."""
        self._repository = repository

    def extract_text(self, path: str) -> str:
        """Extrai o texto de um documento."""

        if not path:
            raise InvalidValueException("O caminho do documento não pode ser vazio para extrair o texto.")
        
        return self._repository.extract_text(path)