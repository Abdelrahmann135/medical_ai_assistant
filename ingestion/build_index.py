import numpy as np
import faiss

def create_faiss_index(embeddings):
    embeddings = np.array(embeddings).astype('float32')
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index