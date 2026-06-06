from ingestion.chunking import chunk_data
from ingestion.embeddings import create_embedding_index
from ingestion.build_index import create_faiss_index
from app.resources import embedding_model
from app.resources import splitter
import faiss
import pickle
import pandas as pd

# load your processed data
data = pd.read_json("./data/diseases.json")

all_chunks = chunk_data(data, splitter())

# embeddings
embeddings, texts = create_embedding_index(all_chunks, embedding_model())

# build index
index = create_faiss_index(embeddings)

# save index
faiss.write_index(index, "./data/faiss/medical.index")

# save chunks
with open("./data/faiss/chunks.pkl", "wb") as f:

    pickle.dump(all_chunks, f)

print("Knowledge base built successfully.")