# RAG Chatbot for Physical AI Book

This directory contains the implementation of a Retrieval-Augmented Generation (RAG) chatbot that can answer questions about the Physical AI book content.

## Components

1. **Backend (FastAPI)** - Handles document ingestion and question answering
2. **Frontend (React)** - User interface for interacting with the chatbot
3. **Vector Database (Qdrant)** - Stores document embeddings for semantic search

## Setup Instructions

### 1. Environment Setup

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Add your API keys to the `.env` file:
```bash
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=your_openai_api_key  # Required if using OpenAI for LLM
COHERE_API_KEY=your_cohere_api_key  # Required if using Cohere for LLM
EMBEDDING_PROVIDER=cohere           # Options: "openai" or "cohere"
LLM_PROVIDER=cohere                 # Options: "openai" or "cohere"
```

### 2. Backend Setup

1. Install Python dependencies:
```bash
cd chatbot
pip install -r requirements.txt
```

2. Run the ingestion script to process the book's markdown files:
```bash
python ingest.py
```

3. Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Integration

The React component `RagChatbot.js` can be imported and used in your existing React application:

```jsx
import RagChatbot from './components/RagChatbot';

function App() {
  return (
    <div className="App">
      {/* Your other components */}
      <RagChatbot />
    </div>
  );
}
```

## Features

- **Semantic Search**: Finds relevant content from the book using vector embeddings
- **Context-Aware Responses**: Answers questions based on the book's content
- **Text Selection**: Ask questions about selected text on the page
- **Source Attribution**: Shows which documents were used to generate responses

## API Endpoints

- `POST /rag` - Answer a question based on the book's content
  - Request: `{"q": "question", "selected": "optional selected text"}`
  - Response: `{"question": "...", "answer": "...", "sources": [...]}`

- `GET /health` - Health check endpoint

## Configuration

- **Embedding Provider**: Set `EMBEDDING_PROVIDER` in your environment to "openai" or "cohere"
- **LLM Provider**: Set `LLM_PROVIDER` in your environment to "openai" or "cohere"
- **Collection Name**: By default, uses "physical_ai_book" collection in Qdrant
- **Chunk Size**: Text is split into chunks of 512 tokens by default

## Architecture

The RAG system follows these steps:
1. Ingestion: Markdown files from `docs/**` are processed, chunked, and stored in Qdrant
2. Query Processing: Questions are converted to embeddings and searched against the vector database
3. Response Generation: Relevant content is sent to OpenAI to generate a contextually appropriate response