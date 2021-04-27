from fastapi import FastAPI, Request, HTTPException
from starlette.responses import Response, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import login, register, feed

app = FastAPI()

app.include_router(login.router)
app.include_router(register.router)
app.include_router(feed.router)

login.manager.useRequest(app)

origins = [
    "http://localhost:8080", # frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

