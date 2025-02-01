from numpy.f2py.symbolic import Op
from pydantic import BaseModel, EmailStr, validator, Field  # this will be used to create request schemas
from typing import Optional, List
from datetime import datetime
from fastapi import HTTPException
from fastapi import status as st


class ChatGPTCall(BaseModel):
    prompt: str
    Instructions: Optional[str]
    Aim: Optional[str]
    UploadFile: Optional[bool] = False
    # Model: Optional[List[str]] = ["Poverty"]
    Model: Optional[str] = "Poverty"
    CollectionName: Optional[str] = "Tests"
    QAModel: Optional[str] = "gpt-4-0125-preview"


class ChatGPTRetrieveAnswers(BaseModel):
    Thread_id: str
    Run_id: str
    CollectionName: str
