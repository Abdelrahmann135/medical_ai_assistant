from sentence_transformers import SentenceTransformer
from transformers import pipeline
from langchain_ollama import ChatOllama
from transformers import pipeline
import faiss
import pickle
import whisper
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.utilities import SerpAPIWrapper
import os
# =====================
# splitter
# =====================
def splitter():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=0.5
        )
    return splitter
print("Splitter resource loaded successfully")

# =====================
# Embedding Model
# =====================
def embedding_model():
    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    ).to("cuda")
    return embedding_model
print("Resources loaded successfully")
# =====================
# LLM
# =====================
def llm():
    llm = ChatOllama(
    model="llama3:8b",
    temperature=0
    )
    return llm
print("LLM resource loaded successfully")

# =====================
# NER Model
# =====================
def ner_pipeline():
    ner_pipeline = pipeline(
        "ner",
        model="d4data/biomedical-ner-all",
        aggregation_strategy="simple"
    )
    return ner_pipeline

print("NER pipeline resource loaded successfully")
# =====================
# Intent Classifier
# =====================
def intent_classifier():
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )
    return classifier
# =====================
# Vector Index
# =====================
def get_index():
    index = faiss.read_index(
        "data/faiss/medical.index"
    )
    return index


print("Vector index resource loaded successfully")

# =====================
# Stored Chunks
# =====================
def all_chunks():
    with open("data/faiss/chunks.pkl", "rb") as f:
        all_chunks = pickle.load(f)
    return all_chunks

print("Stored chunks resource loaded successfully")
# =====================
# google search
# =====================
def google_search():
    google_search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
    return google_search

# =====================
# Stored Chunks
# =====================
def whisper_model():
    model = whisper.load_model("medium")
    return model
print("Whisper model resource loaded successfully")