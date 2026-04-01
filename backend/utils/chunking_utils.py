import re

CHUNCK_LIST_MAX_LENGTH = 70

def chunk_text(text: str) -> list[str]:
    """Realiza a quebra do texto em chunks semânticos para geração de embeddings."""
    if not text:
        return []

    # 1. quebra semântica
    units = split_semantic(text)

    # 3. garantir limite de chunks
    chunks = enforce_max_chunks(units, CHUNCK_LIST_MAX_LENGTH)

    # 4. validação final
    return [c for c in chunks if is_valid_chunk(c)]

def split_semantic(text: str) -> list[str]:
    """Divide o texto em unidades semânticas, como parágrafos ou sentenças, para preservar o contexto e a coesão do conteúdo, o que pode resultar em chunks mais significativos para a geração de embeddings."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    
    # fallback se não houver estrutura
    if len(paragraphs) <= 1:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    return paragraphs

def enforce_max_chunks(chunks: list[str], max_chunks: int) -> list[str]:
    """Garante que a lista de chunks não exceda o limite máximo, mesclando chunks adjacentes quando necessário."""
    if len(chunks) <= max_chunks:
        return chunks

    factor = len(chunks) // max_chunks + 1
    new_chunks = []

    for i in range(0, len(chunks), factor):
        merged = " ".join(chunks[i:i+factor])
        new_chunks.append(merged)

    return new_chunks

def is_valid_chunk(text: str) -> bool:
    """Valida se um chunk é útil para gerar um embedding, filtrando chunks muito curtos ou com baixa proporção de caracteres alfanuméricos, o que pode indicar que o chunk é "quebrado" ou contém principalmente símbolos, e portanto pode não ser útil para representação semântica."""
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