from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    id: int
    token: str
    message: str 