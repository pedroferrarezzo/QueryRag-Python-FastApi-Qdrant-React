import re

def clean_text(text: str) -> str:
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