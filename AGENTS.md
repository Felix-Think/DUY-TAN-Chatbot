# Repository Guidelines

## Project Structure & Module Organization

This repository contains a FastAPI RAG chatbot backend and a Vite React frontend. Backend code lives in `src/`: `agent/` contains the LangChain chatbot, retriever, and prompts; `ingest/` loads, chunks, and stores source documents; `config/` manages settings; `services/`, `schemas/`, and `api/` support the HTTP layer. The API entrypoint is `main.py`; ingestion starts from `run_ingest.py`. Frontend code is in `frontend/src/`, with assets in `frontend/public/` and `frontend/src/assets/`. Test data lives in `tests/`. Runtime data is expected under `data/sources/` and `data/chromadb/`.

## Build, Test, and Development Commands

- `python -m venv .venv && source .venv/bin/activate`: create a Python environment.
- `pip install -e .` or `uv pip install -e .`: install backend dependencies.
- `python main.py`: run the FastAPI API on port `8000`.
- `python run_ingest.py`: load markdown files from `data/sources/`, chunk them, and persist embeddings to ChromaDB.
- `python tests/test_rag_pipeline.py`: run a manual retrieval and answer smoke test.
- `python tests/evaluate_agent.py`: evaluate questions from `tests/testcase.csv` and write `tests/testcase_answer.csv`.
- `cd frontend && npm install && npm run dev`: run the frontend locally.
- `cd frontend && npm run build` / `npm run lint`: build or lint the frontend.
- `docker compose up --build`: run proxy, API, and frontend containers.

## Coding Style & Naming Conventions

Use Python 3.13+ with absolute imports, for example `from src.agent.chatbot import AdmissionChatbot`. Follow 4-space Python indentation and keep modules focused by layer. Use `snake_case` for Python files, functions, and variables; `PascalCase` for classes; and uppercase for constants or environment keys. Frontend files use JSX modules, 2-space indentation, and ESLint rules from `frontend/eslint.config.js`.

## Testing Guidelines

Current tests are script-style integration checks that require a valid `.env`, OpenAI access, and an ingested vector store. Keep new inputs in `tests/testcase.csv` with clear expected targets. When changing retrieval, prompts, chunking, or models, run ingestion first, then `python tests/evaluate_agent.py`, and compare `tests/testcase_answer.csv`.

## Commit & Pull Request Guidelines

Recent commits use short messages such as `Fix UI alignment with important flags` and `Modified front-end`. Keep commits focused and describe the user-visible change. Pull requests should include a summary, backend/frontend impact, environment changes, test results, and screenshots for UI changes.

## Security & Configuration Tips

Keep secrets in `.env`; do not commit API keys or generated ChromaDB data. Important variables include `OPENAI_API_KEY`, optional LangSmith settings, and `VITE_API_URL` for frontend builds. Review CORS and proxy settings before production deployment.
