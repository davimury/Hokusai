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

class Posts(BaseModel):
    body: str
    images: List[str]
    reactions: List[int]


class Tags(BaseModel):
    tag_name: str