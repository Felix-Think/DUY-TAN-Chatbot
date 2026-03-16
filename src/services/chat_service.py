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
