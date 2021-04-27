from fastapi import APIRouter, FastAPI, Request, HTTPException, Depends
from fastapi_login import LoginManager
from starlette.responses import Response, RedirectResponse, JSONResponse, HTMLResponse
from db.db_main import Session, USERS
from datetime import timedelta
from models import Login

SECRET = "434d502035aa8243868e3e5767afb5943c75fb5f0a18e013"

router = APIRouter()

manager = LoginManager(SECRET, "/", use_cookie=True)
manager.cookie_name = "rsa_cookie"

@manager.user_loader
async def load_user(email: str):
    """
        Procura o usuario do banco e retorna o objeto se o encontrar
    """
    try:
        session = Session()
        user = session.query(USERS).filter_by(email=email).first()

        if not user:
            return None
        else:
            return user

    except Exception as e:
        raise e
    
    finally:
        session.close()

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
        
        response = JSONResponse(content='Sucesso')
        access_token = manager.create_access_token(data={"sub": formData.email}, expires=timedelta(hours=6))
        manager.set_cookie(response, access_token)
        
    except HTTPException as e:
        raise e
    
    if flag:
        return response

@router.get("/v1/is_loged", response_class=HTMLResponse)
async def auth_is_loged(user=Depends(manager)):
    return JSONResponse(content=True)

@router.delete("/v1/logout", response_class=HTMLResponse)
async def auth_logout(res: Response, user=Depends(manager)):
    try:
        res.delete_cookie("rsa_cookie")

    except Exception as e:
        print(f'Error: Impossivel deletar cookie do cliente:\n{e}')
