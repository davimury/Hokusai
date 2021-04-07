from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Login

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/login")
def auth_teste(user: Login):
    print(user)
    return {"user": user}

