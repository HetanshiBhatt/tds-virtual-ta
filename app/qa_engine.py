# app/qa_engine.py

from app.utils import load_json, embed_texts, get_top_match

# Load content from JSON files
course_data = load_json("course_content.json")
discourse_data = load_json("discourse_posts.json")

# Extract text chunks
course_chunks = [item["content"] for item in course_data]
discourse_chunks = [item["content"] for item in discourse_data]

# Combine both for answering
all_chunks = course_chunks + discourse_chunks
all_embeddings = embed_texts(all_chunks)

def answer_question(question: str) -> dict:
    """Given a question, return the most relevant content from course/discourse."""
    if not question.strip():
        return {"error": "Question is empty"}

    try:
        top_result = get_top_match(question, all_chunks, all_embeddings, top_k=1)[0]
        return {
            "answer": top_result["chunk"],
            "score": round(float(top_result["score"]), 3)  # ✅ Convert to float
        }
    except Exception as e:
        return {"error": str(e)}
