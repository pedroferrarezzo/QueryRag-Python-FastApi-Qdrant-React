import re
from exceptions import InvalidValueException, ParseException
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
        
        extracted_text = self._repository.extract_text(path)
        if not extracted_text:
            raise ParseException("Não foi possível extrair texto do documento fornecido.")
        
        extracted_text = self._clean_text(extracted_text)

        return extracted_text


    def _clean_text(self, text: str) -> str:
        """Limpa o texto extraído, removendo linhas que são compostas principalmente por símbolos ou que têm uma baixa proporção de caracteres alfanuméricos, o que pode indicar que são partes "quebradas" ou não informativas do documento. Melhorando a qualidade do texto antes do chunking e embedding."""
        # Remove linhas compostas só por símbolos/tabelas
        text = re.sub(r'^[\s\|\-\+\.\(\)◎○]+$', '', text, flags=re.MULTILINE)

        # Remove linhas com muitos símbolos e poucos caracteres alfanuméricos
        text = re.sub(r'^(?=.*[\|\u25CB\u25CE◎○])(?!.{0,20}[a-zA-Z0-9]).*$', '', text, flags=re.MULTILINE)

        # Remove múltiplos pipes
        text = re.sub(r'\|+', ' ', text)

        # Remove espaços excessivos
        text = re.sub(r'\s+', ' ', text)

        return text.strip()