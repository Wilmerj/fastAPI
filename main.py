from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from config.database import  engine, Base
from middlewares.error_handler import Errorhandler
from routers.movie import movie_router
from routers.auth import auth_router

app = FastAPI()
app.title = "La mera API RE educativa"
app.version = "0.0.1"

app.add_middleware(Errorhandler)
app.include_router(movie_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["home"])
def message():
    return HTMLResponse(content="<h1>¡Hola, FastAPI!</h1>", status_code=200)
