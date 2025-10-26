import faiss
import json 
import numpy as np 
from sentence_transformers import SentenceTransformer


MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def load_index():
    index = faiss.read_index("vector_index.faiss")
    with open("text_chunks.json", "r") as f:
        chunks = json.load(f)
    return index, chunks

def find_similar_chunks(question, index, chunks, top_k=3):
    # Vectorize the Query: Uses the pre-loaded embedding 
    # MODEL to convert the text question into a numerical
    # vector. This step involves tokenization and 
    # embedding, ensuring the query is in the same vector
    # space as the indexed documents.
    query_embedding = MODEL.encode([question])

    # Search the Index: Performs the core similarity 
    # search on the FAISS index.
    # D (Distances): A list of the $\text{top\_k}$ 
    # distances (scores) between the query and the 
    # closest document vectors.
    # I (Indices): A list of the internal IDs (indices) 
    # of the $\text{top\_k}$ closest vectors found in the
    # index.
    D, I = index.search(np.array(query_embedding, dtype='float32'), top_k)
    # Retrieve Text Chunks
    results = [chunks[i] for i in I[0]]
    return results