from PIL import Image
import re

# Overlap serve para garantir que o contexto seja mantido entre os chunks, evitando que informações importantes sejam perdidas na divisão do texto.
def chunk_text(text: str, max_size: int = 500, overlap: int = 50):
        # Validação
    if overlap >= max_size:
        raise ValueError("overlap deve ser menor que max_size")
    
    if not text or max_size <= 0:
        return []
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Define o fim do chunk
        end = start + max_size
        
        # Se não é o último chunk, tenta quebrar em uma sentença ou palavra
        if end < len(text):
            # Tenta quebrar no último ponto final antes de end
            last_period = text.rfind('.', start, end)
            if last_period != -1 and last_period > start + max_size // 2:
                end = last_period + 1
            else:
                # Caso contrário, tenta quebrar no último espaço
                last_space = text.rfind(' ', start, end)
                if last_space != -1 and last_space > start + max_size // 2:
                    end = last_space

        chunk = text[start:end].strip()
        
        if chunk and is_valid_chunk(chunk):
            chunks.append(chunk)
        
        # Move o início para o próximo chunk com overlap
        start = end - overlap
    
    return chunks


def is_valid_chunk(text: str) -> bool:
    text = text.strip()

    if len(text) < 50:
        return False

    letters = sum(c.isalnum() for c in text)

    # Calcula a proporção de caracteres alfanuméricos em relação ao total de caracteres. 
    # Se for muito baixo, provavelmente é um chunk "quebrado" ou com muitos símbolos, o que pode indicar que não é um chunk útil para embedding.
    ratio = letters / len(text)

    # mais restritivo
    if ratio < 0.6:
        return False

    # evita chunks "visualmente estruturais"
    if text.count("|") > 3:
        return False

    return True