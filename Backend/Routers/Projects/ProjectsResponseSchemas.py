from pydantic import BaseModel, Extra
from typing import Optional, List, Tuple, Union
from datetime import datetime


class UserRegistrationInfoResponse(BaseModel):
    """
    This is the schema for user login to send specific information, Not all.
    """
    name: str
    family: str
    email: str

    class Config:
        """
        This is required by FastAPI to be able to transfer json to dict
        """
        from_attributes = True


class UserLoginInfoResponse(BaseModel):
    """
    This is the schema for user login to send specific information, Not all.
    """
    name: str
    family: str
    email: str
    country_iso: str
    mobile: str

    class Config:
        """
        This is required by FastAPI to be able to transfer json to dict
        """
        from_attributes = True


class User(BaseModel):
    """
    This is the schema for user login to send specific information, Not all.
    """
    user_id: int
    name: str
    family: str
    email: str
    country_iso: str
    mobile: str
    registration_time: datetime
    enabled: bool

    class config:
        from_attributes = True
        extra = Extra.allow



class UserExistence(BaseModel):
    user_id: int
    name: Optional[str]
    family: Optional[str]
    email: Optional[str]
    country_iso: Optional[str]
    mobile: Optional[str]
    registration_time: Optional[datetime]
    enabled: Optional[bool]

    class Config:
        from_attributes = True
