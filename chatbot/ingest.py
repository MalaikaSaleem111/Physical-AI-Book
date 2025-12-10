import os
import glob
import uuid
import logging
from typing import List, Dict

import markdown
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct

from embedding_utils import get_embedding, get_embedding_dimension

# -------------------------------------------------
# ENV & LOGGING
# -------------------------------------------------
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise RuntimeError("❌ QDRANT_URL or QDRANT_API_KEY missing in .env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("INGEST")

# -------------------------------------------------
# QDRANT CLIENT
# -------------------------------------------------
qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=20
)

# -------------------------------------------------
# READ MARKDOWN FILES
# -------------------------------------------------
def read_markdown_files(docs_dir: str) -> List[Dict]:
    markdown_files = glob.glob(f"{docs_dir}/**/*.md", recursive=True)
    documents = []

    for path in markdown_files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                md_content = f.read()

            html = markdown.markdown(md_content)
            text = BeautifulSoup(html, "html.parser").get_text(" ")

            documents.append({
                "content": text.strip(),
                "source_file": os.path.basename(path)
            })

            logger.info(f"✅ Loaded {path}")

        except Exception as e:
            logger.error(f"❌ Failed reading {path}: {e}")

    return documents

# -------------------------------------------------
# CHUNK TEXT
# -------------------------------------------------
def chunk_text(text: str, max_chars: int = 1200) -> List[str]:
    chunks = []
    current = ""

    for sentence in text.split(". "):
        if len(current) + len(sentence) < max_chars:
            current += sentence + ". "
        else:
            chunks.append(current.strip())
            current = sentence + ". "

    if current.strip():
        chunks.append(current.strip())

    return chunks

# -------------------------------------------------
# INGEST DOCUMENTS
# -------------------------------------------------
def ingest_documents(collection_name: str = "physical_ai_book"):
    logger.info("🚀 Starting ingestion")

    # Always recreate collection (important when switching embeddings)
    try:
        qdrant.delete_collection(collection_name)
        logger.info("🗑️ Old collection deleted")
    except Exception:
        logger.info("ℹ️ Collection did not exist")

    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=get_embedding_dimension(),
            distance=models.Distance.COSINE
        )
    )

    logger.info(f"📦 Collection created ({get_embedding_dimension()} dims)")

    docs_path = "docs" if os.path.exists("docs") else "../docs"
    documents = read_markdown_files(docs_path)

    if not documents:
        logger.warning("⚠️ No markdown documents found")
        return

    points = []

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for i, chunk in enumerate(chunks):
            try:
                embedding = get_embedding(chunk)

                points.append(
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={
                            "content": chunk,
                            "source_file": doc["source_file"],
                            "chunk_index": i
                        }
                    )
                )

            except Exception as e:
                logger.error(f"❌ Embedding failed: {e}")

    if not points:
        logger.warning("⚠️ No embeddings created")
        return

    qdrant.upsert(collection_name=collection_name, points=points)
    logger.info(f"✅ Ingested {len(points)} chunks successfully")

# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    ingest_documents()
