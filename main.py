from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.qa_engine import answer_question

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "Virtual Teaching Assistant is running!"}

@app.post("/ask")
def ask_question(question: str = Form(...)):
    try:
        print(f"❓ Received question: {question}")
        result = answer_question(question)
        print(f"✅ Answered: {result}")
        return JSONResponse(content=result)
    except Exception as e:
        print(f"❌ Error in /ask: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
