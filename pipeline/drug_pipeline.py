from drugs.medicine_search import drug_search
from drugs.drug_cleaning import clean_drug_text
from prompts.drug_prompt import drug_build_prompt
from llm.response_generator import run_chain

def drug_pipeline(query, user_id="user_1"):
    response = drug_search(query)
    cleaned_response = clean_drug_text(response)
    prompt = drug_build_prompt()
    response = run_chain(prompt, {"query": query, "context": cleaned_response}, user_id)
    return response
