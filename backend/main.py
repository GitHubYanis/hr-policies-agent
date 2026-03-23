from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import AskRequest, AskResponse, SourceItem
from rag import init_rag as rag_state
from rag.pipeline import ask_hr_policy

@asynccontextmanager
async def lifespan(_: FastAPI):
    rag_state.init_rag()
    yield

app = FastAPI(title="HR Policies Agent", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def root():
    return {"message": "HR Policy RAG API is running", "status": "ok"}

@app.get("/status")
def status():
    is_ready = rag_state.collection is not None
    return {
        "status": "ready" if is_ready else "not_ready",
        "collection_size": rag_state.collection.count() if is_ready else 0,
    }

@app.post("/ask", response_model=AskResponse)
def ask(body: AskRequest):
    if rag_state.collection is None:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialised.")
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = ask_hr_policy(body.question, top_k=body.top_k, threshold=body.threshold)
    return AskResponse(
        question=result["question"],
        answer=result["answer"],
        sources=[SourceItem(**s) for s in result["sources"]],
    )