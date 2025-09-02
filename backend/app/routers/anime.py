from fastapi import APIRouter,Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Anime
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
   description: Optional[str] = None
   release_year: Optional[date] = None
   status: Optional[str] = None
   episodes_chapters: Optional[int] = None
   image_url: Optional[str] = None
   popularity: Optional[int] = None
   rating: Optional[float] = None


class AnimeResponse(BaseModel):
   id: int
   title: str
   alt_titles: Optional[str] = None
   type: Optional[str] = None
   description: Optional[str] = None
   release_year: Optional[date] = None
   status: Optional[str] = None
   episodes_chapters: Optional[int] = None
   image_url: Optional[str] = None
   popularity: Optional[int] = None
   rating: Optional[float] = None
    
   class Config:
        from_attributes = True

class AnimeUpdate(BaseModel):
    title: str
    alt_titles: Optional[str] = None
    type: Optional[str] = None 
    description: Optional[str] = None
    release_year: Optional[date] = None
    status: Optional[str] = None
    episodes_chapters: Optional[int] = None
    image_url: Optional[str] = None
    popularity: Optional[int] = None
    rating: Optional[float] = None

# Retrieve all anime
@router.get("/", response_model = List[AnimeResponse])
async def get_all_anime(db: Session = Depends(get_db)):
    anime_list = db.query(Anime).all()

    return anime_list

# Retreive anime by id
@router.get("/{id}", response_model=AnimeResponse)
async def get_animebyid(id: int, db: Session = Depends(get_db)):
    anime = db.query(Anime).filter(Anime.id == id).first()
    if not anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Anime not found")
    return anime

# Update anime
@router.put("/{id}", response_model=AnimeResponse)
async def update_animebyid(id: int, anime_update: AnimeUpdate, db: Session = Depends(get_db)):
    rows_affected = db.query(Anime).filter(Anime.id == id).update(
        anime_update.model_dump(exclude_unset=True)
    )
    if rows_affected == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Anime not found")
    db.commit()
    updated_animebyid = db.query(Anime).filter(Anime.id == id).first()
    return updated_animebyid

# Delete anime
@router.delete("/{id}")
async def delete_anime(id: int, db: Session = Depends(get_db)):
    rows_deleted = db.query(Anime).filter(Anime.id == id).delete()

    if rows_deleted == 0:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    db.commit()
    return {"message": f"Anime {id} deleted"}

# Add Anime to Database
@router.post("/", response_model=AnimeResponse, status_code=status.HTTP_201_CREATED)
async def create_anime(anime: AnimeCreate, db: Session = Depends(get_db)):
    try:
        db_anime = Anime(
            title=anime.title,
            alt_titles=anime.alt_titles,
            type=anime.type,
            description=anime.description,
            release_year=anime.release_year,
            status=anime.status,
            episodes_chapters=anime.episodes_chapters,
            image_url=anime.image_url,
            popularity=anime.popularity,
            rating=anime.rating
        )
        db.add(db_anime) 
        db.commit()
        db.refresh(db_anime)
        return db_anime
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Anime already exists")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create anime due to server error")