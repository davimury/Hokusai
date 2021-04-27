from fastapi import APIRouter, Request, HTTPException, Depends
from starlette.responses import Response
from db.db_main import Session, USERS
from sqlalchemy import exc
from models import Registro
from routers.login import manager

router = APIRouter()

@router.get("/v1/feed/{username}")
def auth_register(username: str = None, user=Depends(manager)):
    print(username)