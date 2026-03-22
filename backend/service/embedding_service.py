from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-base")

# Dimensão dos vetores gerados pelo modelo de embedding
# A dimensão corresponde na prática a quantidade de índices do vetor de embedding
EMBEDDING_DIMENSION = 768

def embed_text(text: str):
    return model.encode(text)