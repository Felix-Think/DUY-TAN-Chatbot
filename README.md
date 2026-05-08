# Duy Tân Chatbot

Duy Tân Chatbot là ứng dụng RAG chatbot cho tư vấn tuyển sinh, gồm:

- Backend FastAPI dùng LangChain, ChromaDB và OpenAI.
- Frontend React Vite được build và serve bằng Nginx khi chạy Docker.

## Cấu trúc dự án

- `main.py`: entrypoint backend FastAPI.
- `run_ingest.py`: script nạp dữ liệu vào ChromaDB.
- `src/`: mã nguồn backend.
  - `agent/`: chatbot, retriever và prompt.
  - `ingest/`: load, chunk và lưu tài liệu vào vector store.
  - `config/`: cấu hình ứng dụng.
  - `api/`, `services/`, `schemas/`: tầng HTTP và service.
- `frontend/`: mã nguồn frontend React Vite.
- `data/sources/`: tài liệu nguồn dạng markdown.
- `data/chromadb/`: dữ liệu vector ChromaDB sau khi ingest.
- `tests/`: script test và dữ liệu đánh giá.

## Yêu cầu

- Docker Desktop hoặc Docker Engine có Docker Compose.
- File `.env` ở thư mục gốc dự án.
- `OPENAI_API_KEY` hợp lệ nếu muốn chatbot gọi OpenAI.
- Dữ liệu đã ingest trong `data/chromadb/` nếu muốn RAG trả lời theo tài liệu.

## Cấu hình môi trường

Tạo file `.env` ở thư mục gốc:

```bash
OPENAI_API_KEY=your_openai_api_key
VITE_API_URL=http://localhost:8000
```

Nếu dự án có dùng thêm LangSmith, có thể bổ sung các biến tương ứng vào `.env`.

Không commit file `.env`.

## Chạy bằng Docker

Chạy 2 service chính là backend `api` và frontend `frontend`:

```bash
docker compose up --build -d api frontend
```

Sau khi chạy xong:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

Kiểm tra trạng thái container:

```bash
docker compose ps api frontend
```

Xem log:

```bash
docker compose logs -f api frontend
```

Tắt container:

```bash
docker compose stop api frontend
```

Tắt và xoá container/network:

```bash
docker compose down
```

## Nạp dữ liệu cho RAG

Chatbot cần dữ liệu trong `data/chromadb/`. Nếu chưa có vector store hoặc đã thay đổi tài liệu trong `data/sources/`, chạy ingest trước.

Nếu chạy bằng môi trường Python local:

```bash
python run_ingest.py
```

Nếu muốn chạy ingest bằng Docker:

```bash
docker compose run --rm api python run_ingest.py
```

Sau khi ingest xong, khởi động lại backend nếu cần:

```bash
docker compose restart api
```

## Ghi chú về proxy

Trong `docker-compose.yml` có service `proxy-manager` dùng cho reverse proxy/domain/SSL. Khi chạy local để phát triển hoặc demo trên máy cá nhân, chỉ cần chạy:

```bash
docker compose up --build -d api frontend
```

Không cần bật `proxy-manager` trừ khi bạn muốn cấu hình domain hoặc HTTPS.

## Chạy local không dùng Docker

Backend:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python run_ingest.py
python main.py
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Kiểm thử

Các script test cần `.env` hợp lệ, OpenAI API key và dữ liệu đã ingest.

Smoke test RAG:

```bash
python tests/test_rag_pipeline.py
```

Đánh giá từ `tests/testcase.csv`:

```bash
python tests/evaluate_agent.py
```

Kết quả được ghi vào `tests/testcase_answer.csv`.
