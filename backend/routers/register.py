from fastapi import APIRouter, HTTPException
from starlette.responses import Response
from db.db_main import Session, USERS
from sqlalchemy import exc
from models import Registro

router = APIRouter()


@router.post("/v1/register")
def auth_register(formData: Registro):
    try:
        flag = True
        session = Session()

        new_user = USERS(name=formData.name, username=formData.username,
                         email=formData.email, password=formData.password)
        session.add(new_user)

        session.commit()

    except exc.IntegrityError:
        flag = False
        raise HTTPException(
            status_code=409, detail="email ou username já cadastrados!")

    finally:
        session.close()

    if flag:
        return Response(status_code=200)
