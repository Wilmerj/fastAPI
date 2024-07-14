from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()

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

@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    results = MovieService().get_movies()
    return JSONResponse(content=jsonable_encoder(results), status_code=200)

@movie_router.get("/movies/{movie_id}", tags=["movies"], response_model=Movie)
def get_movie(movie_id: int = Path(ge=1, le=2000)) -> Movie:
    result = MovieService().get_movie_by_id(movie_id)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    results = MovieService().get_movies_by_category(category)
    if not results:
        return JSONResponse(content={"message": "Category not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(results))

@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)

@movie_router.put("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
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

@movie_router.delete("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)