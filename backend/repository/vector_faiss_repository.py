import faiss
import numpy as np
from dto import VectorDto
from model import Document, Metadata
from service.embedding_service import EMBEDDING_DIMENSION

# Banco vetorial em memória usando FAISS. Ele trabalha melhor com similaridade de cosseno ao invés de distância euclidiana
# Para utilizar similaridade cosseno, normalizamos os vetores e utilizamos Inner Product (IP)
# Após normalização L2, o inner product é equivalente à similaridade cosseno
index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)

# Lista para armazenar os metadados associados a cada vetor inserido
documents_metadata = []


def add_vector(vector_dto: VectorDto):
    
    # Transforma o vetor em um array numpy de tipo float32 (recomendado para o FAISS) e adiciona ao índice FAISS. O shape será (1, dimension)
    vector = np.array([vector_dto.vector]).astype("float32")

    # Normaliza o vetor para norma L2 = 1
    # Isso permite que o inner product represente a similaridade cosseno
    faiss.normalize_L2(vector)

    # Cada vetor recebe implicitamente um ID baseado na ordem de inserção
    index.add(vector)

    documents_metadata.append(Metadata(type=vector_dto.type, chunk=vector_dto.chunk, source=vector_dto.source))

def search_vector(vector, k=5):

    vector = np.array([vector]).astype("float32")

    # Normaliza o vetor de consulta para manter consistência com os vetores armazenados
    faiss.normalize_L2(vector)

    '''
    Executa o algoritmo de machine learning KNN (K-Nearest Neighbors) para encontrar os vetores mais próximos no índice FAISS. 
    O processo envolve medir proximidade + ordenar + pegar os k mais próximos:
        Medir proximidade → similaridade de cosseno (via produto interno com vetores normalizados)
        Ordenar → decrescente pelo score
        Pegar os k mais próximos → o k do search_vector(vector, k=5)
    '''
    # ids (shape: (1, k)) → índices dos vetores no índice FAISS
    # scores (shape: (1, k)) → valores de similaridade (quanto maior, mais similar)
    scores, ids = index.search(vector, k)

    documents = []

    # Recupera os metadados associados aos vetores retornados
    for idx, score in zip(ids[0], scores[0]):
        if idx == -1:
            continue

        if idx < len(documents_metadata):
            documents.append(Document(metadata=documents_metadata[idx], score=float(score)))

    return documents