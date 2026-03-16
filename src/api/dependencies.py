from functools import lru_cache
from fastapi import Header, HTTPException, Depends
from src.agent.chatbot import AdmissionChatbot

# 1. Singleton pattern with lru_cache for Chatbot Instance
@lru_cache()
def get_chatbot_instance():
    """Returns a singleton instance of the chatbot."""
    print("--- Initializing Admission Chatbot (Singleton) ---")
    return AdmissionChatbot()

# 2. Mock Authentication (Simple API Key Check)
async def verify_token(x_api_key: str = Header(..., description="API Key for Admission Bot Access")):
    """Mock authentication before real user/pass backend."""
    # Dummy valid key: 'duytan-secret-2024'
    if x_api_key != "duytan-secret-2024":
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return {"user_id": 1, "username": "mock_user"}

# 3. Dependency to get the chatbot
def get_chatbot_service(chatbot: AdmissionChatbot = Depends(get_chatbot_instance)):
    """Provides the chatbot instance to routes."""
    return chatbot
