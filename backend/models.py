from pydantic import BaseModel

class Login(BaseModel):
    email: str
    password: str

class Registro(BaseModel):
    name: str
    username: str
    email: str
    password: str
