from pydantic import BaseModel
from typing import Union

class V_USERS(BaseModel):
    name: str
    username: str
    email: str
    password: str
    
class V_TAGS(BaseModel):
    tag_name: str

class V_POSTS(BaseModel):
    post_body: str