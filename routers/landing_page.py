from fastapi import APIRouter, Request
#from starlette.responses import HTMLResponse

router = APIRouter()

@router.get("/landing-page", tags=["Landing Page"]) # Precisa ter o atributo: response_class=HTMLResponse para retornar um pagina html
async def landing_page(request: Request): 
    return {"message": "Landing Page"} # Por enquanto retornando um json com o retorno da rota acessada