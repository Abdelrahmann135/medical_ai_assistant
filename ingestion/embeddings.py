import faiss

def create_embedding_index(all_chunks, model):
    
    texts = [item["text"] for item in all_chunks]

    embeddings = model.encode(texts)
    faiss.normalize_L2(embeddings)
    return embeddings, texts
