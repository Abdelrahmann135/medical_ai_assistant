INTENT_LABELS = [
    "medical_definition",
    "symptom_assessment",
    "possible_diagnosis",
    "treatment_information",
    "general_health_advice",
    "follow_up_question",
    "general_chat",
    "hospital_search",
    "clinic_search",
    "emergency_assessment",
    "drug_information",
    "side_effects_information",
    "drug_interactions_information"
]
MEDICAL_PIPELINE_LABELS = [
    "medical_definition",
    "symptom_assessment",
    "possible_diagnosis",
    "treatment_information",
    "general_health_advice",
    "follow_up_question",
    "general_chat"
]
HOSPITAL_SEARCH_LABELS = [
    "hospital_search",
    "clinic_search",
    "emergency_assessment"
]
DRUG_INFO_LABELS = [
    "drug_information",
    "side_effects_information",
    "drug_interactions_information"
]

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

NOISE_WORDS_FROM_ARTICLES_SCRAPING = [
    "pubmed", "google scholar", "external link",
    "related links", "advanced article search",
    "comments", "send to", "editors"
]

PIPER_PATH = r"C:\Users\User\AppData\Local\Programs\piper\piper.exe"
MODEL_PATH = r"C:\Users\User\AppData\Local\Programs\piper\en_US-amy-medium.onnx"
OUTPUT_FILE = "output.wav"