from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import index, landing_page, login, portfolio, registro

app = FastAPI()

app.include_router(index.router)
app.include_router(landing_page.router)
app.include_router(login.router)
app.include_router(portfolio.router)
app.include_router(registro.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
