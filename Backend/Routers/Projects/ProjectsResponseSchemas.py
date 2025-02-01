from pydantic import BaseModel, Extra
from typing import Optional, List, Tuple, Union
from datetime import datetime


class Project(BaseModel):
    """
    This is the schema for user login to send specific information, Not all.
    """
    project_id: int
    user_id: int
    name: str

    class Config:
        """
        This is required by FastAPI to be able to transfer json to dict
        """
        from_attributes = True


class ClarifyProject(BaseModel):
    query: str
    chat_history: str

    class Config:
        """
        This is required by FastAPI to be able to transfer json to dict
        """
        from_attributes = True

