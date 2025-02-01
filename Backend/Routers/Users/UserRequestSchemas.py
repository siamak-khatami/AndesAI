from pydantic import BaseModel, EmailStr, validator, Field  # this will be used to create request schemas
from typing import Optional, List

class UserLoginInfoRequest(BaseModel):
    """
    This class defines the schema for the api to get user information due to the login purposes.
    """
    email: EmailStr
    password: str


class UserRegistrationInfoRequest(BaseModel):
    """
    This schema defines the input for new user creation.
    """
    email: EmailStr
    name: str
    family: str
    password: str


class UserPassUpdateRequest(BaseModel):
    email: EmailStr


class UserResendActivation(BaseModel):
    email: EmailStr


class ResetPass(BaseModel):
    email: EmailStr


class TourInfo(BaseModel):
    tour_name: str


class UserNewPassWord(BaseModel):
    password: str
