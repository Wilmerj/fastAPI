from config.database import Session
from models.movie import Movie as MovieModel
from sqlalchemy import func
from schemas.movie import Movie

class MovieService():
    def __init__(self) -> None:
        self.db = Session()

    def get_movies(self):
        results = self.db.query(MovieModel).all()
        return results

    def get_movie_by_id(self, movie_id: int):
        result = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        return result

    def get_movies_by_category(self, category: str):
        results = self.db.query(MovieModel).filter(func.lower(MovieModel.category) == category.lower()).all()
        return results

    def create_movie(self, movie: Movie):
        movie = MovieModel(**movie.dict())
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def update_movie(self, movie_id: int, movie: Movie):
        result = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        if not result:
            return None

        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        self.db.commit()
        return result

    def delete_movie(self, movie_id: int):
        result = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        if not result:
            return None
        self.db.delete(result)
        self.db.commit()
        return result