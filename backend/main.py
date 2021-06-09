from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, posts, tags, users, connections

app = FastAPI()

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(tags.router)
app.include_router(users.router)
app.include_router(connections.router)

auth.manager.useRequest(app)

origins = [
    "http://localhost:8080", # frontend
    "http://localhost:8081", # frontend
    "https://localhost:8080", # frontend
    "https://localhost:8081", # frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

