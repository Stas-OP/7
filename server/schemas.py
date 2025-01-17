from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    id: int
    token: str
    message: str

class RequestHistory(BaseModel):
    timestamp: datetime
    request_type: str
    endpoint: str

class CipherRequest(BaseModel):
    text: str
    key: str

class CipherResponse(BaseModel):
    result: str

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    id: int
    text: str
    timestamp: datetime 