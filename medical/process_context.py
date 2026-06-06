from medical.ner import NER_extract
from medical.entity_filter import filter_entities

def process_context(texts, ner, query):
    context = "\n\n".join(texts)

    context_entities = NER_extract(context, ner)
    query_entities = NER_extract(query, ner)

    return {
        "context": context,
        "context_symptoms": list(set(filter_entities(context_entities, "Sign_symptom"))),
        "query_symptoms": list(set(filter_entities(query_entities, "Sign_symptom"))),
        "context_diseases": list(set(filter_entities(context_entities, "Disease"))),
        "query_diseases": list(set(filter_entities(query_entities, "Disease"))),
    }