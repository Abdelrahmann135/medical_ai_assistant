from retrieval.retrieve_context import retrieve_context
from app.resources import embedding_model, ner_pipeline, get_index, all_chunks
from medical.disease_confidence import disease_confidence
from medical.process_context import process_context
from retrieval.fallback_search import web_search
from prompts.medical_prompt import medical_build_prompt
from llm.response_generator import run_chain

def medical_pipeline(query, threeshold=0.5, user_id="user_1"):
    
    print(type(embedding_model))

    context_texts, context_metas, scores, ids = retrieve_context(all_chunks(), query, get_index(), embedding_model(), k=3)


    context_data = process_context(context_texts, ner_pipeline(), query)
    disease_conf = disease_confidence(ids, scores, all_chunks())
    top_conf = disease_conf[0][1] if disease_conf else 0
    if top_conf < threeshold:
        print("Low confidence in retrieved context, performing web search...")
        context_texts = web_search(query)
        context_data = process_context(context_texts, ner_pipeline(), query)
        print("Using web search results as context")

    prompt = medical_build_prompt()

    response = run_chain(prompt, {
            "query": query,
            "context": context_data["context"],
            "context_symptoms": context_data["context_symptoms"],
            "context_diseases": context_data["context_diseases"],
            "query_symptoms": context_data["query_symptoms"],
            "query_diseases": context_data["query_diseases"],
        }, user_id)

    return response