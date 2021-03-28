from fastapi import APIRouter, Request
#from starlette.responses import HTMLResponse

router = APIRouter()

@router.get("/portfolio", tags=["Portfólio"]) # Precisa ter o atributo: response_class=HTMLResponse para retornar um pagina html
async def login(request: Request): 
    return {"message": "Portfólio"} # Por enquanto retornando um json com o retorno da rota acessada