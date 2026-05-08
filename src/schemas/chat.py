from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str = Field(..., example="Ngành Kỹ thuật Phần mềm học gì?")
    session_id: Optional[str] = Field(
        default=None,
        example="web-1700000000000-abc123",
        description="Stable chat session id used for short-term conversation memory.",
    )

class ContextItem(BaseModel):
    page_content: str
    metadata: dict

class ChatResponse(BaseModel):
    answer: str
    context: Optional[List[ContextItem]] = None
    status: str = "success"
