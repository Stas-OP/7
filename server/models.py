from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    password_hash: str
    token: str 