import faiss
import json 
import numpy as np 
from sentence_transformers import SentenceTransformer


MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def load_index():
    index = faiss.read_index("vector_index.faiss")