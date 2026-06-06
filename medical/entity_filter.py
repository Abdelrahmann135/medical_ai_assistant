def filter_entities(entities, label):
    return [
        e["word"] for e in entities
        if e["entity_group"] == label and e["score"] > 0.8
    ]