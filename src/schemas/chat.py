from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str = Field(..., example="Ngành Kỹ thuật Phần mềm học gì?")

class ContextItem(BaseModel):
    page_content: str
    metadata: dict

class ChatResponse(BaseModel):
    answer: str
    context: Optional[List[ContextItem]] = None
    status: str = "success"
