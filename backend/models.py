from datetime import datetime
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
    name: str = None
    
class Posts(BaseModel):
    post_id: int
    description: str
    slides: List[str]
    username: str
    author_id: int
    postType: int
    likes: int
    created_at: datetime = None
    like: bool = False
    dislike: bool = False

class Add_Posts(BaseModel):
    body: str
    type: int
    images: List[str]
    tags: List[Tags]
