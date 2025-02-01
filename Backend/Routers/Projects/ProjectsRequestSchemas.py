from pydantic import BaseModel, EmailStr, validator, Field  # this will be used to create request schemas
from typing import Optional, List


class Project(BaseModel):
    """
    This class defines the schema for the api to get user information due to init a project.
    """
    user_id: int
    name: str


class ClarifyProject(BaseModel):
    chat_history: str

class GanttInfo(BaseModel):
    project_id: int