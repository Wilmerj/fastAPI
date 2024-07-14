from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

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
    MovieService().create_movie(movie)
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)

@movie_router.put("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(movie_id: int, movie: Movie) -> dict:
    result = MovieService().update_movie(movie_id, movie)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)

@movie_router.delete("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
    result = MovieService().delete_movie(movie_id)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)