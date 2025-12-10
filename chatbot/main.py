from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import logging
from dotenv import load_dotenv
from qdrant_client import QdrantClient

from embedding_utils import get_query_embedding
from llm_utils import generate_chat_response

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "cohere")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# --------------------------------------------------
# Validation
# --------------------------------------------------
if not QDRANT_URL or not QDRANT_API_KEY:
    raise RuntimeError("❌ QDRANT_URL or QDRANT_API_KEY missing")

if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY missing")

if LLM_PROVIDER == "cohere" and not COHERE_API_KEY:
    raise RuntimeError("❌ COHERE_API_KEY missing")

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag-api")

# --------------------------------------------------
# Qdrant Client
# --------------------------------------------------
qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=10
)

COLLECTION_NAME = "physical_ai_book"

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------
app = FastAPI(
    title="Physical AI RAG API",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Models
# --------------------------------------------------
class RAGRequest(BaseModel):
    q: str
    selected: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "q": "What is the main concept discussed in this book?",
                "selected": "Optional highlighted text for strict mode"
            }
        }


class Source(BaseModel):
    excerpt: str
    source_file: str
    score: float

    class Config:
        json_schema_extra = {
            "example": {
                "excerpt": "Sample text from the document...",
                "source_file": "chapter1.md",
                "score": 0.85
            }
        }


class RAGResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the main concept discussed in this book?",
                "answer": "The book discusses physical AI concepts...",
                "sources": [
                    {
                        "excerpt": "Sample text from the document...",
                        "source_file": "chapter1.md",
                        "score": 0.85
                    }
                ]
            }
        }

# --------------------------------------------------
# Vector Search
# --------------------------------------------------
def search_qdrant(query: str, limit: int = 5):
    try:
        vector = get_query_embedding(query)
    except Exception as e:
        logger.error(f"Embedding error: {e}")
        raise HTTPException(status_code=500, detail="Embedding failed")

    try:
        hits = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limit,
            with_payload=True
        )

        results = []
        for hit in hits:
            results.append({
                "content": hit.payload.get("content", ""),
                "source_file": hit.payload.get("source_file", ""),
                "score": hit.score
            })

        return results

    except Exception as e:
        logger.error(f"Qdrant search error: {e}")
        raise HTTPException(status_code=500, detail="Vector search failed")

# --------------------------------------------------
# Answer Generation
# --------------------------------------------------
def generate_answer(question: str, context: str, strict: bool):
    system_prompt = (
        "You are a helpful assistant for a technical book.\n"
        "Answer ONLY using the provided context.\n"
        "If the answer is not present, say you do not know."
    )

    if strict:
        system_prompt += (
            "\nThe user highlighted specific text.\n"
            "Answer ONLY from that highlighted content."
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}"
        }
    ]

    return generate_chat_response(
        messages=messages,
        temperature=0.2,
        max_tokens=400
    )

# --------------------------------------------------
# RAG Endpoint ✅
# --------------------------------------------------
@app.post(
    "/rag",
    response_model=RAGResponse,
    summary="RAG Endpoint to answer questions based on book content",
    description="Accepts a question and optional selected text, then returns an answer based on the book content using RAG (Retrieval Augmented Generation)"
)
async def rag_endpoint(rag_request: RAGRequest = Body(...)):
    logger.info(f"RAG query: {rag_request.q}")

    search_text = rag_request.selected or rag_request.q
    search_results = search_qdrant(search_text)

    if not search_results:
        return RAGResponse(
            question=rag_request.q,
            answer="I could not find relevant information in the book.",
            sources=[]
        )

    context = "\n\n".join(r["content"] for r in search_results)

    answer = generate_answer(
        question=rag_request.q,
        context=context,
        strict=bool(rag_request.selected)
    )

    sources = [
        Source(
            excerpt=r["content"][:200] + "...",
            source_file=r["source_file"],
            score=r["score"]
        )
        for r in search_results
    ]

    return RAGResponse(
        question=rag_request.q,
        answer=answer,
        sources=sources
    )

# --------------------------------------------------
# Health Check
# --------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# --------------------------------------------------
# Local Run
# --------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
