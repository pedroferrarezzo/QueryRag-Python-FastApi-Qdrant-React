from exceptions import InvalidValueException, ParseException
from ports import DocumentParser
from utils.text_utils import clean_text

class DocumentParserService:
    """Serviço responsável por extração de texto de documentos de forma agnóstica à biblioteca utilizada."""

    def __init__(self, repository: DocumentParser):
        """Inicializa o serviço de extração de texto."""
        self._repository = repository

    def extract_text(self, path: str) -> str:
        """Extrai o texto de um documento."""

        if not path:
            raise InvalidValueException("O caminho do documento não pode ser vazio para extrair o texto.")
        
        extracted_text = self._repository.extract_text(path)
        if not extracted_text:
            raise ParseException("Não foi possível extrair texto do documento fornecido.")
        
        extracted_text = clean_text(extracted_text)

        return extracted_text