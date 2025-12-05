from fastapi import APIRouter,Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Anime, Genre
from .genre import GenreResponse
from datetime import date
from typing import List, Optional

router = APIRouter(
    prefix="/anime",
    tags=["anime"]
)

class AnimeCreate(BaseModel):
   title: str
   alt_titles: Optional[str] = None
   type: Optional[str] = None
   original_format: Optional[str] = None
   source_material: Optional[str] = None
   description: Optional[str] = None
   release_year: Optional[date] = None
   aired_from: Optional[date] = None
   aired_to: Optional[date] = None
   status: Optional[str] = None
   episodes: Optional[int] = None
   chapters: Optional[int] = None
   volumes: Optional[int] = None
   duration_minutes: Optional[int] = None
   image_url: Optional[str] = None
   popularity: Optional[int] = None
   rating: Optional[float] = None
   author: Optional[str] = None
   studio: Optional[str] = None
   serialization: Optional[str] = None

   genres: list[int] = []


class AnimeResponse(BaseModel):
   id: int
   title: str
   alt_titles: Optional[str] = None
   type: Optional[str] = None
   original_format: Optional[str] = None
   source_material: Optional[str] = None
   description: Optional[str] = None
   release_year: Optional[date] = None
   aired_from: Optional[date] = None
   aired_to: Optional[date] = None
   status: Optional[str] = None
   episodes: Optional[int] = None
   chapters: Optional[int] = None
   volumes: Optional[int] = None
   duration_minutes: Optional[int] = None
   image_url: Optional[str] = None
   popularity: Optional[int] = None
   rating: Optional[float] = None
   author: Optional[str] = None
   studio: Optional[str] = None
   serialization: Optional[str] = None

   
   genres: List[GenreResponse] = []
   
   class Config:
        from_attributes = True


class AnimeUpdate(BaseModel):
    title: Optional[str] = None
    alt_titles: Optional[str] = None
    type: Optional[str] = None
    original_format: Optional[str] = None
    source_material: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[date] = None
    aired_from: Optional[date] = None
    aired_to: Optional[date] = None
    status: Optional[str] = None
    episodes: Optional[int] = None
    chapters: Optional[int] = None
    volumes: Optional[int] = None
    duration_minutes: Optional[int] = None
    image_url: Optional[str] = None
    popularity: Optional[int] = None
    rating: Optional[float] = None
    author: Optional[str] = None
    studio: Optional[str] = None
    serialization: Optional[str] = None
    
    genres: Optional[List[int]] = []

# Retrieve all anime
@router.get("/", response_model = List[AnimeResponse])
async def get_all_anime(db: Session = Depends(get_db)):
    anime_list = db.query(Anime).all()

    return anime_list

# Retreive anime by id
@router.get("/{id}", response_model=AnimeResponse)
async def get_anime_by_id(id: int, db: Session = Depends(get_db)):
    anime = db.query(Anime).filter(Anime.id == id).first()
    if not anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Anime not found")
    return anime

# Update anime
@router.put("/{id}", response_model=AnimeResponse)
async def update_anime_by_id(id: int, anime_update: AnimeUpdate, db: Session = Depends(get_db)):
    updated_anime_by_id = db.query(Anime).filter(Anime.id == id).first()

    if not updated_anime_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Anime not found")

    for key, value in anime_update.model_dump(exclude_unset=True).items():
        if key != "genres":
            setattr(updated_anime_by_id, key, value)
    
    if anime_update.genres is not None:
        updated_anime_by_id.genres = db.query(Genre).filter(Genre.id.in_(anime_update.genres)).all()
    
    db.commit()
    db.refresh(updated_anime_by_id)
    return updated_anime_by_id

# Delete anime
@router.delete("/{id}")
async def delete_anime(id: int, db: Session = Depends(get_db)):
    try: 
        anime = db.query(Anime).filter(Anime.id == id).first()

        if not anime: 
            raise HTTPException(status_code=404, detail="Anime not found")
        anime.genres = []
        db.flush()

        db.delete(anime)
        db.commit()
        
        return {"message": f"Anime {id} deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete anime: {str(e)}"
        )

# Add Anime to Database
@router.post("/", response_model=AnimeResponse, status_code=status.HTTP_201_CREATED)
async def create_anime(anime: AnimeCreate, db: Session = Depends(get_db)):
    try:
        db_anime = Anime(
           title=anime.title,
            alt_titles=anime.alt_titles,
            type=anime.type,
            original_format=anime.original_format,
            source_material=anime.source_material,
            description=anime.description,
            release_year=anime.release_year,
            aired_from=anime.aired_from,
            aired_to=anime.aired_to,
            status=anime.status,
            episodes=anime.episodes,
            chapters=anime.chapters,
            volumes=anime.volumes,
            duration_minutes=anime.duration_minutes,
            image_url=anime.image_url,
            popularity=anime.popularity,
            rating=anime.rating,
            author=anime.author,
            studio=anime.studio,
            serialization=anime.serialization
        )
        # Look up genres by IDs
        if anime.genres:
            db_anime.genres = db.query(Genre).filter(Genre.id.in_(anime.genres)).all()

        db.add(db_anime) 
        db.commit()
        db.refresh(db_anime)
        return db_anime
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Anime already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail= f"Failed to create anime: {str(e)}"
        )