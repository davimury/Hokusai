from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List

class Tag(BaseModel):
    tag_id      : int           = None
    name        : str           = None
    
class Post(BaseModel):
    post_id     : int           = None
    body        : str           = None
    description : str           = None
    slides      : List[str]     = None
    tags        : List[Tag]     = None
    username    : str           = None
    author_id   : int           = None
    postType    : int           = None
    likes       : int           = None
    created_at  : datetime      = None
    like        : bool          = None
    dislike     : bool          = None

class User(BaseModel):
    user_id     : int           = None
    name        : str           = None
    username    : str           = None
    email       : EmailStr      = None
    password    : str           = None
    tags        : List[Tag]     = None
    posts       : List[Post]    = None


class Connection(BaseModel):
    con_id      : int           = None
    con_status  : bool          = None
    user_1_id   : int           = None
    user_2_id   : int           = None
