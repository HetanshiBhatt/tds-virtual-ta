# app/utils.py

import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load and cache the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_json(filepath):
    """Load a JSON file and return the data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def embed_texts(text_list):
    """Embed a list of text chunks using the model."""
    return model.encode(text_list)

def get_top_match(question, content_chunks, content_embeddings, top_k=1):
    """Find the most relevant content chunk using cosine similarity."""
    question_embedding = model.encode([question])
    similarities = cosine_similarity(question_embedding, content_embeddings)[0]
    
    # Get top-k most similar indexes
    top_indices = similarities.argsort()[::-1][:top_k]
    
    top_results = [{
        "chunk": content_chunks[i],
        "score": similarities[i]
    } for i in top_indices]

    return top_results
