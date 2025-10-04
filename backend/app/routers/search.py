from fastapi import APIRouter,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Anime, Genre
from .anime import AnimeResponse
from datetime import date
from typing import List, Optional

class Search(BaseModel):
    title: Optional[str] = None
    alt_titles: Optional[str] = None
    type: Optional[str] = None 
    release_year: Optional[date] = None
    status: Optional[str] = None
    min_popularity: Optional[int] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None
    genres: Optional[str] = None


router = APIRouter(
    prefix='/anime/search',
    tags=['search']
)

@router.get("/", response_model=List[AnimeResponse])
async def search_anime(
    title: Optional[str] = None,
    alt_titles: Optional[str] = None,
    type: Optional[str] = None,
    release_year: Optional[date] = None,
    status: Optional[str] = None,
    min_popularity: Optional[int] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    genres: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Anime)

    if title:
        query = query.filter(Anime.title.ilike(f"%{title}%"))
    if alt_titles:
        query = query.filter(Anime.alt_titles.ilike(f"%{alt_titles}%"))
    if release_year:
        query = query.filter(Anime.release_year == release_year)
    if status:
        query = query.filter(Anime.status == status)
    if min_rating:
        query = query.filter(Anime.rating >= min_rating)
    if max_rating:
        query = query.filter(Anime.rating <= max_rating)
    if min_popularity:
        query = query.filter(Anime.popularity >= min_popularity)
    if genres:
        query = query.join(Anime.genres).filter(Genre.name.ilike(f"%{genres}%"))

    return query.all()