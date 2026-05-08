# Duy Tân Chatbot

Duy Tân Chatbot là một dự án ứng dụng RAG (Retrieval-Augmented Generation) với backend được xây dựng bằng FastAPI, LangChain, ChromaDB và frontend được xây dựng bằng React (Vite).

## Cấu trúc dự án

- `src/`: Chứa mã nguồn backend (FastAPI).
  - `agent/`: Chứa logic chatbot của LangChain, retriever và các prompt.
  - `ingest/`: Chứa code để xử lý (load, chunk) và lưu trữ tài liệu (vector store).
  - `config/`: Quản lý các cài đặt cấu hình.
  - `services/`, `schemas/`, `api/`: Hỗ trợ tầng HTTP của ứng dụng.
- `frontend/`: Chứa mã nguồn frontend (React Vite).
- `data/sources/`: Chứa các tài liệu markdown (nguồn dữ liệu) để đưa vào vector store.
- `data/chromadb/`: Nơi lưu trữ cơ sở dữ liệu vector ChromaDB.
- `tests/`: Chứa mã nguồn test và dữ liệu test (`testcase.csv`).

## Yêu cầu hệ thống

- Python 3.13+
- Node.js & npm (cho frontend)
- Docker & Docker Compose (tùy chọn)
- OpenAI API Key

## Hướng dẫn cài đặt và chạy (Local)

### 1. Thiết lập Backend

Tạo và kích hoạt môi trường ảo (Virtual Environment):
```bash
python -m venv .venv
# Trên macOS/Linux:
source .venv/bin/activate
# Trên Windows:
# .venv\Scripts\activate
```

Cài đặt các thư viện phụ thuộc:
```bash
pip install -e .
# Hoặc nếu bạn dùng uv:
# uv pip install -e .
```

Cấu hình môi trường:
- Tạo một file `.env` ở thư mục gốc của dự án.
- Thiết lập biến môi trường `OPENAI_API_KEY` của bạn trong file `.env`. (Tuyệt đối không commit file `.env` lên Git).
- Tùy chọn: thiết lập các biến LangSmith nếu cần thiết.

### 2. Nạp dữ liệu (Ingestion)

Trước khi trò chuyện với chatbot, bạn cần nạp kiến thức cho hệ thống (lấy từ các tài liệu trong `data/sources/`):
```bash
python run_ingest.py
```

### 3. Khởi động Backend (FastAPI API)

Khởi động server API. Server sẽ chạy trên cổng `8000`:
```bash
python main.py
```

### 4. Thiết lập và chạy Frontend

Mở một terminal mới (hoặc tab khác), chuyển đến thư mục `frontend`:
```bash
cd frontend
npm install
npm run dev
```

*(Lưu ý: Thiết lập biến môi trường `VITE_API_URL` trong frontend cho phù hợp nếu cần).*

---

## Hướng dẫn chạy bằng Docker

Để chạy nhanh toàn bộ dự án (Bao gồm API, Frontend, Proxy) bằng Docker, hãy chạy:

```bash
docker compose up --build
```

---

## Kiểm thử (Testing)

**Yêu cầu:** Cần cấu hình file `.env` hợp lệ, quyền truy cập API OpenAI và đã chạy lệnh nạp dữ liệu (ingest vector store).

- Để chạy kiểm thử RAG cơ bản (smoke test):
  ```bash
  python tests/test_rag_pipeline.py
  ```

- Để đánh giá (evaluate) ứng dụng dựa trên các câu hỏi từ `tests/testcase.csv`:
  ```bash
  python tests/evaluate_agent.py
  ```
  *(Kết quả sẽ được xuất ra file `tests/testcase_answer.csv`)*.

---

## Một số quy tắc phát triển (Coding Guidelines)
- Backend viết bằng Python 3.13+. Sử dụng `snake_case` cho file, biến, hàm và `PascalCase` cho class. Sử dụng import tuyệt đối (`from src.agent...`).
- Frontend sử dụng JSX modules, 2-space indentation và tuân thủ ESLint rules từ `frontend/eslint.config.js`.
