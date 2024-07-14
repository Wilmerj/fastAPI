from pydantic import BaseModel, Field
from typing import Optional

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