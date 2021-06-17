from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, posts, tags, users, chat, connections
from db.db_main import db_engine
app = FastAPI()

app.include_router(auth.router)
app.include_router(tags.router)
app.include_router(chat.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(connections.router)

auth.manager.useRequest(app)

origins = [
    "http://app.hokusai.codes", # frontend
    "https://app.hokusai.codes", # frontend
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
def shutdown_session():
    db_engine.dispose()