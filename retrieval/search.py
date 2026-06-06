import numpy as np
import faiss

def search(query, index, model, k=1):
    query_vec = model.encode([query])
    faiss.normalize_L2(query_vec)
    scores, ids = index.search(np.array(query_vec), k)
    return scores, ids