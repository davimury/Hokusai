from fastapi import APIRouter, Request
#from starlette.responses import HTMLResponse

router = APIRouter()

@router.get("/", tags=["Index"]) # Precisa ter o atributo: response_class=HTMLResponse para retornar um pagina html
async def index(request: Request): 
    return {"message": "Index"} # Por enquanto retornando um json com o retorno da rota acessada