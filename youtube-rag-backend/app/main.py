from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.services.transcript import fetch_transcript
from app.services.chunker import chunk_transcript
from app.services.vector_store import get_or_create_vector_store

from app.services.rag_chain import build_rag_chain

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="YouTube RAG Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptRequest(BaseModel):
    video_id: str


class QuestionRequest(BaseModel):
    video_id: str
    question: str

class VideoRequest(BaseModel):
    video_id: str



@app.get("/")
def health_check():
    return {"status": "Backend is running 🚀"}

@app.post("/transcript")
def get_transcript(req: TranscriptRequest):
    try:
        transcript = fetch_transcript(req.video_id)
        return {
            "video_id": req.video_id,
            "transcript_preview": transcript[:500]  # preview only
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chunk-preview")
def chunk_preview(req: TranscriptRequest):
    transcript = fetch_transcript(req.video_id)
    docs = chunk_transcript(transcript)

    return {
        "total_chunks": len(docs),
        "sample_chunk": docs[0].page_content[:500]
    }


@app.post("/index-video")
def index_video(req: VideoRequest):
    try:
        vector_store = get_or_create_vector_store(req.video_id)
        return {"status": "indexed"}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/ask")
def ask_question(req: QuestionRequest):
    chain = build_rag_chain(req.video_id)
    answer = chain.invoke(req.question)

    return {
        "video_id": req.video_id,
        "question": req.question,
        "answer": answer
    }