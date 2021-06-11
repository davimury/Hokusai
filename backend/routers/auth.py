from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
from fastapi_login import LoginManager
from starlette.responses import Response, JSONResponse, HTMLResponse
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from db.db_main import Session, USERS
from datetime import timedelta
from sqlalchemy import exc
from models import User
from datetime import datetime, timedelta
import jwt

SECRET = "434d502035aa8243868e3e5767afb5943c75fb5f0a18e013"

router = APIRouter()
manager = LoginManager(SECRET, "/login", use_cookie=True)
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


@router.post("/register")
def auth_register(formData: User):
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


@router.post("/login")
async def auth_login(formData: User):
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


@router.post("/send_recover")
async def send_email_token(formData: User):
    """
    EndPoint para envio de form com dados de login e senha do usuário
    """
    flag = True

    print(formData)
    try:
        conf = ConnectionConfig(
            MAIL_USERNAME = "app.hokusai@gmail.com",
            MAIL_PASSWORD = "Pr0t3g1d0@",
            MAIL_FROM = "app.hokusai@gmail.com",
            MAIL_PORT = 587,
            MAIL_SERVER = "smtp.gmail.com",
            MAIL_TLS = True,
            MAIL_SSL = False,
            USE_CREDENTIALS = True,
            TEMPLATE_FOLDER='./email'
        )

        encoded_jwt = jwt.encode({'email': formData.email, "exp": datetime.now() + timedelta(hours=1)}, SECRET, algorithm='HS256')

        message = MessageSchema(
            subject="Hokusai - Recuperar senha",
            recipients=[formData.email],
            body={'url': f'http://localhost:8080/login?recover={encoded_jwt}'},
            subtype="html"
        )

    except Exception as e:
        flag = False
        print(e)

    if flag:
        try:
            fm = FastMail(conf)
            await fm.send_message(message, template_name="recover.html") 
        except Exception as e:
            print(e)
    else:
        print('er')


@router.post("/recover_password/")
async def get_email_token(recover: Dict[str, str]):
    """
    EndPoint para envio de form com dados de login e senha do usuário
    """
    try:
        decode_jwt = jwt.decode(recover['token'], SECRET, algorithms='HS256')

        session = Session()
        user = session.query(USERS).filter_by(email=decode_jwt['email']).first()

        user.password = recover['password']

        session.merge(user)
        
    except Exception as e:
        print(e)

    finally:
        session.commit()


@router.delete("/logout", response_class=HTMLResponse)
async def auth_logout(res: Response):
    try:
        res.delete_cookie("hokusai_cookie")

    except Exception as e:
        print(f'Error: Impossivel deletar cookie do cliente:\n{e}')