from fastapi import FastAPI, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import Errorhandler
from middlewares.jwt_bearer import JWTBearer

app = FastAPI()
app.title = "La mera API RE educativa"
app.version = "0.0.1"

app.add_middleware(Errorhandler)

Base.metadata.create_all(bind=engine)



class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_lenth=5, max_length=15)
    overview: str = Field(min_lenth=15, max_length=50)
    year: int = Field(default=1996, le=2024)
    rating: float = Field(le=10, ge=1)
    category: str = Field(min_lenth=1, max_length=15)

    class Config:
        json_schema_extra = {
            "examples": [
                {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Jaaaaaa te voy ganando!",
                "year": 1996,
                "rating": 7.8,
                "category": "Drama",
            }
            ]
        }

@app.get("/", tags=["home"])
def message():
    return HTMLResponse(content="<h1>¡Hola, FastAPI!</h1>", status_code=200)

@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == '123456':
        token = create_token(user.dict())
        return JSONResponse(content={"token": token}, status_code=200)
    return JSONResponse(content={"message": "Unauthorized"}, status_code=401)

@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    results = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(results), status_code=200)

@app.get("/movies/{movie_id}", tags=["movies"], response_model=Movie)
def get_movie(movie_id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result))

@app.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    results = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not results:
        return JSONResponse(content={"message": "Category not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(results))

@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)

@app.put("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(movie_id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()

    return JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)

@app.delete("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)