# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Duy-Tan-Chatbox** is a Vietnamese language admission consulting chatbot powered by Retrieval Augmented Generation (RAG). It retrieves information from markdown documents about Duy Tan University's Computer Science & AI school and answers questions from prospective students and parents using an OpenAI LLM.

**Tech Stack:**
- **LangChain**: Framework for building RAG chains
- **ChromaDB**: Vector database for semantic search
- **OpenAI**: GPT-4o-mini for chat, text-embedding-3-small for embeddings
- **Pydantic**: Configuration management with BaseSettings
- **Python 3.13+**: Project requires Python 3.13 or higher

## Architecture

The project follows a modular pipeline architecture with three main layers:

### 1. Data Ingestion Pipeline (`src/ingest/`)
Converts markdown source documents into a searchable vector store.

- **MarkdownLoader** (`loader.py`): Loads all `.md` files from `data/sources/` using LangChain's DirectoryLoader. Handles both single and batch file loading.
- **DocumentChunker** (`chunker.py`): Two-stage splitting strategy:
  - Stage 1: Splits by markdown headers (#, ##, ###) to preserve document structure
  - Stage 2: Recursively chunks large sections (1000 char chunks, 100 char overlap)
- **VectorStoreManager** (`vectorstore.py`): Creates and manages ChromaDB vector store. Handles embedding generation and persistence at `data/chromadb/`.

**Pipeline Flow:** `run_ingest.py` orchestrates: Load → Chunk → Embed & Store

### 2. Agent Layer (`src/agent/`)
Implements a RAG-based chatbot that retrieves documents and generates answers.

- **AdmissionRetriever** (`retriever.py`): Wrapper around ChromaDB vector store. Performs similarity search to retrieve top-5 relevant documents.
- **AdmissionChatbot** (`chatbot.py`): Orchestrates the RAG chain:
  - Creates LangChain retrieval chain
  - Chains retriever → document combination → LLM
  - Returns both answer and retrieved context
- **Prompts** (`prompts.py`): Vietnamese system prompt for admission consultant persona. Instructs LLM to only use provided context and decline to answer out-of-scope questions.

**Query Flow:** User question → Retriever (vector search) → Prompt + Context → LLM → Answer

### 3. Configuration Layer (`src/config/`)
Centralized settings using Pydantic.

- **Settings** (`settings.py`): Single source of truth for all configuration:
  - OpenAI API key and model names
  - LangSmith tracing configuration
  - Paths to data directories (sources, chromadb)
  - ChromaDB collection name
  - Loads from `.env` file using python-dotenv

## Development Commands

**Setup:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
# or: uv pip install -e .
```

**Configuration:**
1. Create `.env` file at project root with:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `LANGCHAIN_TRACING_V2`: Set to "true" to enable LangSmith
   - `LANGCHAIN_API_KEY`: LangSmith API key (optional, only if tracing enabled)
   - `LANGCHAIN_PROJECT`: Project name for LangSmith (optional)

2. Place markdown source documents in `data/sources/` directory

**Ingestion:**
```bash
python run_ingest.py
```
Loads markdown files, chunks them, generates embeddings, and stores in ChromaDB. Creates `data/chromadb/` if it doesn't exist.

**Chat (Basic CLI):**
```bash
python src/agent/chatbot.py
# Or uncomment the interactive loop in chatbot.py main block
```

**Testing/Evaluation:**
```bash
python tests/evaluate_agent.py
```
Runs chatbot against test cases in `tests/playbook.csv` and outputs similarity scores to `tests/answerbook.csv`. Uses cosine similarity between expected and generated embeddings.

**Individual Module Testing:**
```bash
# Test markdown loader
python src/ingest/loader.py

# Test document chunker
python src/ingest/chunker.py

# Test retriever
python src/agent/retriever.py

# Test vector store
python src/ingest/vectorstore.py
```
Each module has a `__main__` block with mock data or local testing examples.

## Key Patterns & Implementation Details

### Import Structure
- All imports use absolute paths from project root (`from src.agent.chatbot import ...`)
- Each module can run standalone with `python module.py` for testing
- Configuration is injected via `from src.config.settings import settings`

### Vector Store Persistence
- ChromaDB stores embeddings at `data/chromadb/`
- Collection name: `"admission_data"` (configured in settings)
- Embeddings use OpenAI's `text-embedding-3-small` model
- Data persists between runs; reloading documents updates the collection

### Error Handling & Logging
- Uses print statements for logging (see `src/utils/logger.py` - minimal implementation)
- Data ingestion provides progress bars via LangChain's `show_progress=True`
- Graceful fallback if no documents found (checks `if not documents`)

### Language & Localization
- System prompt and expected use cases are in Vietnamese
- Supports Vietnamese language queries and responses

## Data Structure

```
data/
├── sources/           # Input: markdown documents to ingest
│   └── *.md
└── chromadb/          # Output: vector store (auto-created)
    ├── ...chroma files...
```

Test files:
```
tests/
├── playbook.csv       # Input: questions and expected answers (id, input, target)
└── answerbook.csv     # Output: evaluation results with scores
```

## Common Workflows

**Adding New Information:**
1. Add markdown file to `data/sources/`
2. Run `python run_ingest.py` to chunk and embed
3. Chatbot automatically uses updated vector store on next query

**Improving RAG Quality:**
- Adjust `DocumentChunker` parameters: `chunk_size` and `chunk_overlap` in `run_ingest.py`
- Adjust `AdmissionRetriever` k-value: `search_kwargs={"k": 5}` in `chatbot.py`
- Modify system prompt in `prompts.py` to change bot behavior
- Change embedding model in settings (currently `text-embedding-3-small`)

**Debugging Retrieval:**
1. Run `python src/agent/retriever.py` to test vector search
2. Check `tests/answerbook.csv` scores to identify low-quality answers
3. Verify documents were chunked correctly with `python src/ingest/chunker.py`

**Enabling Tracing:**
- Set `LANGCHAIN_TRACING_V2=true` and provide `LANGCHAIN_API_KEY` in `.env`
- All LangChain operations will be logged to LangSmith dashboard
