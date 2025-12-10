"""
Lightweight test to verify ingestion pipeline
"""

import os
import sys
from dotenv import load_dotenv

sys.path.append(".")

# Load env
load_dotenv("chatbot/.env")

def test_ingestion():
    print("🔍 Testing ingestion pipeline...\n")

    required_vars = [
        "QDRANT_URL",
        "QDRANT_API_KEY",
        "EMBEDDING_PROVIDER"
    ]

    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        print(f"⚠️ Missing env vars: {missing}")
        return False

    print("✅ Environment variables OK")

    try:
        from chatbot.ingest import read_markdown_files, chunk_text
        print("✅ ingest.py imported successfully")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

    try:
        docs = read_markdown_files("docs")
        print(f"✅ Read {len(docs)} markdown files")

        if docs:
            chunks = chunk_text(docs[0]["content"])
            print(f"✅ Chunking works ({len(chunks)} chunks)")
    except Exception as e:
        print(f"❌ Document processing error: {e}")
        return False

    print("\n🎉 Ingestion setup is VALID")
    print("👉 Run full ingestion with:")
    print("   python -m chatbot.ingest")

    return True


if __name__ == "__main__":
    test_ingestion()
