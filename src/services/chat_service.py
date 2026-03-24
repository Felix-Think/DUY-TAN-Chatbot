import json
from src.agent.chatbot import AdmissionChatbot
from src.schemas.chat import ChatRequest, ChatResponse, ContextItem

class ChatService:
    def __init__(self, agent: AdmissionChatbot):
        self.agent = agent

    async def get_response(self, request: ChatRequest) -> ChatResponse:
        """Processes a chat request using the agent."""
        result = self.agent.ask(request.query)
        
        # Transform context if present
        context = []
        if result.get("context"):
            context = [
                ContextItem(page_content=doc.page_content, metadata=doc.metadata) 
                for doc in result["context"]
            ]
        
        return ChatResponse(
            answer=result["answer"],
            context=context
        )

    async def get_streaming_response(self, request: ChatRequest):
        """Processes a chat request and yields SSE data chunks."""
        async for chunk in self.agent.astream(request.query):
            data = {}
            
            # 1. Handle Context (only sent once at the beginning)
            if "context" in chunk:
                context = [
                    ContextItem(page_content=doc.page_content, metadata=doc.metadata).model_dump()
                    for doc in chunk["context"]
                ]
                data = {"context": context}
            
            # 2. Handle Answer Tokens
            elif "token" in chunk:
                data = {"token": chunk["token"]}
            
            if data:
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        
        # 3. Final signal
        yield "data: [DONE]\n\n"
