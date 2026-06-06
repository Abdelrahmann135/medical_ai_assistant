from pipeline.medical_pipeline import medical_pipeline
from pipeline.drug_pipeline import drug_pipeline
from pipeline.hospital_pipeline import hospital_pipeline
from intent.classifier import classify_intent
import asyncio
from app.config import INTENT_LABELS, MEDICAL_PIPELINE_LABELS, HOSPITAL_SEARCH_LABELS, DRUG_INFO_LABELS

def router(query):
    result = classify_intent(query, INTENT_LABELS)
    intent = result["labels"][0]
    
    if intent in MEDICAL_PIPELINE_LABELS:
        response = medical_pipeline(query)
        print("Medical pipeline")
    elif intent in HOSPITAL_SEARCH_LABELS:
        response = hospital_pipeline(query)
        print("Hospital pipeline")
    elif intent in DRUG_INFO_LABELS:
        response = drug_pipeline(query)
        print("Drug pipeline")
    else:
        response = "Sorry, I couldn't understand your request."
    return response
    