import asyncio
import os
import json
from dotenv import load_dotenv

# Load môi trường
load_dotenv()

from src.agent.chatbot import AdmissionChatbot
from src.services.chat_service import ChatService
from src.schemas.chat import ChatRequest

async def test_service_stream():
    agent = AdmissionChatbot()
    service = ChatService(agent)
    request = ChatRequest(query="Chào bạn")
    
    print("--- Testing Service Stream Output ---")
    async for chunk in service.get_streaming_response(request):
        print(f"RAW CHUNK: {repr(chunk)}")
    print("--- End of Stream ---")

if __name__ == "__main__":
    asyncio.run(test_service_stream())
