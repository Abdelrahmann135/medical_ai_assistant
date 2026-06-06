def split_text(text, splitter, overlap_size=1):
    chunks = splitter.split_text(text)
    new_chunks = []

    for i in range(len(chunks)):
        chunk = chunks[i]

        if i > 0:
            prev_part = chunks[i-1].split()[-overlap_size:]
            chunk = " ".join(prev_part) + " " + chunk

        new_chunks.append(chunk)

    return new_chunks    


def chunk_data(data, splitter):
    all_chunks = []
    for row in data.itertuples():
        disease = row.Disease
        chapter = row.Chapter
        domain = row.Domain

        for article in row.Article:
            chunks = split_text(article, splitter, overlap_size=10)
            for c in chunks:
                all_chunks.append({
                    "text": c.strip(),
                    "metadata": {
                    "disease": disease,
                    "chapter": chapter,
                    "domain": domain,
                    }
                })
    return all_chunks