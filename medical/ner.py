def NER_extract(text, ner):
    entites = ner(text)
    return entites