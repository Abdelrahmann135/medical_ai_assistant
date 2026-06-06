from retrieval.search import search

def retrieve_context(all_chunks, query, index, model, k=3):
    scores, ids = search(query, index, model, k)

    texts = []
    metas = []

    for i in ids[0]:
        texts.append(all_chunks[i]["text"])
        metas.append(all_chunks[i]["metadata"])

    return texts, metas, scores, ids