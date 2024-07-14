from config.database import Session
from models.movie import Movie as MovieModel
from sqlalchemy import func

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