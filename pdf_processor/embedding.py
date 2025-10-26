import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from .utils import extract_text_from_pdf


MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, chunk_size=500):
    words = text.split()

    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def build_faiss_index(pdf_path):
    text = extract_text_from_pdf(pdf_path)

    # We need to convert small chunks because 
    # embedding model has size limit
    chunks = chunk_text(text)

    # convert the list of chunks (text strings) into 
    # a corresponding list of numerical vectors 
    # (embeddings).
    embeddings = MODEL.encode(chunks)

    # FAISS index initialization
    # faiss.IndexFlatL2 creates the simplest type of 
    # FAISS index, which performs an exhaustive, 
    # brute-force search using the L2 (Euclidean) distance.
    # embeddings.shape[1] provides the dimension of the 
    # vectors (e.g., 768 or 1536) to the FAISS index, 
    # telling it the size of the vectors it will store.
    index = faiss.IndexFlatL2(embeddings.shape[1])
    # index.add(np.array(embeddings, dtype='float32')): 
    # This loads the vectors into the initialized index.
    # np.array(embeddings, dtype='float32') ensures 
    # the data is converted to a NumPy array with the 
    # correct $\text{float}32$ data type, which FAISS 
    # requires.
    # index.add(...) inserts all the vectors into 
    # the FAISS search structure.
    index.add(np.array(embeddings, dtype='float32'))

    faiss.write_index(index, "vector_index.faiss")

    with open("text_chunks.json", "w") as f:
        json.dump(chunks, f)