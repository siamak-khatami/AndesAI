from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserInfo(BaseModel):
    _id: str
    first_name: str
    last_name: str
    email: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserInfo
    status: int


class AdminInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
    roles: List[int]


class AdminToken(BaseModel):
    access_token: str
    token_type: str
    data: AdminInfo


class TokenDecodedData(BaseModel):
    """
    This contains information in which we embed with our tokens. For now, it is time and email.
    """
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class ActivationTokenDecode(BaseModel):
    email: Optional[EmailStr] = None


class AdminTokenDecodedData(BaseModel):
    """
    This contains information in which we embed with our tokens. For now, it is time and email.
    """
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: Optional[list] = None