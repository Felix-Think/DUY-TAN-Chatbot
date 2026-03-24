from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from src.schemas.chat import ChatRequest, ChatResponse
from src.api.dependencies import get_chatbot_service, verify_token
from src.services.chat_service import ChatService
from src.agent.chatbot import AdmissionChatbot

app = FastAPI(
    title="Duy Tan University Admission Chatbot API",
    description="Professional RAG-based API for University Admission Consulting.",
    version="1.0.0"
)

# --- CORS CONFIGURATION ---
# Cho phép tất cả các nguồn (origins), phương thức (methods) và headers.
# Trong môi trường production, bạn nên liệt kê cụ thể domain của Frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Cho phép mọi domain truy cập
    allow_credentials=True,
    allow_methods=["*"],           # Cho phép tất cả các phương thức HTTP (GET, POST, etc.)
    allow_headers=["*"],           # Cho phép tất cả các headers (bao gồm X-API-KEY của chúng ta)
)
# ---------------------------

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Duy Tan University Admission Chatbot API!"}

# Single Chat Endpoint with Dependencies: Cache Instance & Auth Check
@app.post("/api/v1/chat/ask")
async def ask_chatbot(
    request: ChatRequest,
    agent: AdmissionChatbot = Depends(get_chatbot_service),
    auth: dict = Depends(verify_token)
):
    """
    Asks the admission bot a question with a streaming response.
    - Requires 'X-API-KEY' header for mock authentication.
    - Uses a singleton chatbot instance for performance.
    """
    service = ChatService(agent)
    return StreamingResponse(
        service.get_streaming_response(request),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
