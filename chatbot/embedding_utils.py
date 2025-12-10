import os
from dotenv import load_dotenv
from openai import OpenAI
import cohere

# -------------------------------------------------
# LOAD ENV
# -------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai").lower()

# -------------------------------------------------
# CLIENTS
# -------------------------------------------------
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
cohere_client = cohere.Client(api_key=COHERE_API_KEY) if COHERE_API_KEY else None


# -------------------------------------------------
# DOCUMENT EMBEDDING (FOR INGESTION)
# -------------------------------------------------
def get_embedding(text: str):
    if not text or not text.strip():
        raise ValueError("Text for embedding cannot be empty")

    if EMBEDDING_PROVIDER == "openai":
        if not openai_client:
            raise RuntimeError("OPENAI_API_KEY missing")

        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    elif EMBEDDING_PROVIDER == "cohere":
        if not cohere_client:
            raise RuntimeError("COHERE_API_KEY missing")

        response = cohere_client.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings[0]

    else:
        raise ValueError(f"Unsupported embedding provider: {EMBEDDING_PROVIDER}")


# -------------------------------------------------
# QUERY EMBEDDING (FOR SEARCH)
# -------------------------------------------------
def get_query_embedding(text: str):
    if not text or not text.strip():
        raise ValueError("Query text cannot be empty")

    if EMBEDDING_PROVIDER == "openai":
        if not openai_client:
            raise RuntimeError("OPENAI_API_KEY missing")

        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    elif EMBEDDING_PROVIDER == "cohere":
        if not cohere_client:
            raise RuntimeError("COHERE_API_KEY missing")

        response = cohere_client.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        return response.embeddings[0]

    else:
        raise ValueError(f"Unsupported embedding provider: {EMBEDDING_PROVIDER}")


# -------------------------------------------------
# EMBEDDING DIMENSIONS (VERY IMPORTANT FOR QDRANT)
# -------------------------------------------------
def get_embedding_dimension():
    if EMBEDDING_PROVIDER == "openai":
        return 1536  # text-embedding-3-small
    elif EMBEDDING_PROVIDER == "cohere":
        return 1024  # embed-english-v3.0
    else:
        raise ValueError(f"Unsupported embedding provider: {EMBEDDING_PROVIDER}")
