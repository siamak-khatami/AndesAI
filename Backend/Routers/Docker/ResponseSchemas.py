from pydantic import BaseModel, Extra
from typing import Optional, List
from datetime import datetime


class ChatGPTCallResponse(BaseModel):
    Thread_id: str
    Run_id: str
    CollectionName: str

    class Config:
        from_attributes = True