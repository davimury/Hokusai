from fastapi import APIRouter, HTTPException, Depends
from fastapi_login import LoginManager
from starlette.responses import Response, JSONResponse, HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import exc
from db.db_main import Session, USERS
from datetime import timedelta
from models import Login, Registro

SECRET = "434d502035aa8243868e3e5767afb5943c75fb5f0a18e013"

router = APIRouter()
manager = LoginManager(SECRET, "/token", use_cookie=True)
manager.cookie_name = "hokusai_cookie"


@manager.user_loader
async def load_user(email: str):
    try: 
        session = Session()
        user = session.query(USERS).filter_by(email=email).first()
        session.close()

        if not user:
            return None
        else:
            return user

    except Exception as e:
        raise e


@router.post("/v1/register")
def auth_register(formData: Registro):
    try:
        flag = True
        session = Session()

        new_user = USERS(name=formData.name, username=formData.username, email=formData.email, password=formData.password)
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


@router.post("/v1/login")
async def auth_login(formData: Login):
    """
    EndPoint para envio de form com dados de login e senha do usuário
    """
    try:
        flag = True
        user = await load_user(formData.email)

        if not user:
            raise HTTPException(status_code=401, detail="email não cadastrado")
        elif not user.verify_password(formData.password):
            raise HTTPException(status_code=401, detail="senha incorreta")

        response = JSONResponse(content={
                                'id': user.user_id, 'user': user.username, 'email': user.email, 'name': user.name})
        access_token = manager.create_access_token(
            data={"sub": formData.email}, expires=timedelta(hours=6))
        manager.set_cookie(response, access_token)

    except HTTPException as e:
        raise e

    if flag:
        return response

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    session = Session()
    user_obj = session.query(USERS).filter_by(username = form_data.username).first()
    user = await load_user(user_obj.email)

    if not user:
        raise HTTPException(status_code=401, detail="email não cadastrado")
    elif not user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="senha incorreta")

    token = manager.create_access_token(
        data=dict(sub=user.username)
    )

    return {"access_token": token, "token_type": "bearer"}


@router.delete("/v1/logout", response_class=HTMLResponse)
async def auth_logout(res: Response):
    try:
        res.delete_cookie("hokusai_cookie")

    except Exception as e:
        print(f'Error: Impossivel deletar cookie do cliente:\n{e}')