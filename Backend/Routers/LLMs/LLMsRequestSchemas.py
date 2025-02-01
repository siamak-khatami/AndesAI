from pydantic import BaseModel, EmailStr, validator, Field  # this will be used to create request schemas
from typing import Optional, List


class ChatLLM(BaseModel):
    prompt: str
    llm_model: str
    chat_history: Optional[List[str]] = []
