from sentence_transformers import CrossEncoder
from model import Document

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, documents: list[Document], k: int = 5):
    if not documents:
        return []

    # Extrai conteúdo corretamente do metadata
    pairs = [
        (query, document.metadata.chunk)
        for document in documents
    ]

    # Score de relevância do cross-encoder
    scores = reranker.predict(pairs)

    # Anexa score mantendo estrutura original
    for document, score in zip(documents, scores):
        document.rerank_score = float(score)

    # Ordena pelo score do reranker (não pelo FAISS)
    documents_sorted = sorted(
        documents,
        key=lambda document: document.rerank_score,
        reverse=True
    )

    return documents_sorted[:k]