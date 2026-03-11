from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.rag.pipeline import RAGPipeline
from src.dto.schemas import QuestionRequest, AnswerResponse

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app = FastAPI(title="Legal AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = RAGPipeline()

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

@app.get("/health")
def health_check():
    return {
        "status":"alive"
    }

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    result = pipeline.ask(request.question, request.use_smart_retrieval)
    return result