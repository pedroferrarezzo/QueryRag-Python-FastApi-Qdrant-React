import re

def clean_text(text: str) -> str:
    # Remove linhas compostas só por símbolos/tabelas
    text = re.sub(r'^[\s\|\-\+\.\(\)◎○]+$', '', text, flags=re.MULTILINE)

    # Remove linhas com muitos símbolos e poucos caracteres alfanuméricos
    text = re.sub(r'^(?=.*[\|\u25CB\u25CE◎○])(?!.{0,20}[a-zA-Z0-9]).*$', '', text, flags=re.MULTILINE)

    # Remove múltiplos pipes
    text = re.sub(r'\|+', ' ', text)

    # Remove espaços excessivos
    text = re.sub(r'\s+', ' ', text)

    return text.strip()