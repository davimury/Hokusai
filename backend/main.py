from fastapi import FastAPI, Request, HTTPException
from starlette.responses import Response, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import login, register, feed, posts, tags, profile

app = FastAPI()

app.include_router(login.router)
app.include_router(register.router)
app.include_router(feed.router)
app.include_router(posts.router)
app.include_router(tags.router)
app.include_router(profile.router)

login.manager.useRequest(app)

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

