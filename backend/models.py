from pydantic import BaseModel
from typing import List

class Login(BaseModel):
    email: str
    password: str

class Registro(BaseModel):
    name: str
    username: str
    email: str
    password: str

class Tags(BaseModel):
    id: int = None
    name: str
    
class Posts(BaseModel):
    body: str
    type: int
    images: List[str]
    tags: List[Tags]

class Profile(BaseModel):
    image: str
    tags: List[int] = []

class Base64(BaseModel):
    base: str