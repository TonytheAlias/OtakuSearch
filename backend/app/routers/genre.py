from fastapi import APIRouter,Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from app.database import get_db
from app.models import Genre
from typing import List

router = APIRouter(
    prefix="/genre",
    tags=["genre"]
)

class GenreCreate(BaseModel):
    name: str

class GenreResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class GenreUpdate(BaseModel):
    name: str

# Retrieve all genres
@router.get("/", response_model = List[GenreResponse])
async def get_all_genres(db: Session = Depends(get_db)):
    genre_list = db.query(Genre).all()

    return genre_list

# Retrieve Genre by id
@router.get("/{id}", response_model = GenreResponse)
async def get_genre_by_id(id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == id).first()
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return genre

# Update Genre 
@router.put("/{id}", response_model=GenreResponse)
async def update_genre_by_id(id: int, genre_update: GenreUpdate, db: Session = Depends(get_db)):
    rows_affected = db.query(Genre).filter(Genre.id == id).update(
        genre_update.model_dump(exclude_unset=True)
    )
    if rows_affected == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    db.commit()
    updated_genre = db.query(Genre).filter(Genre.id == id).first()
    return updated_genre

# Delete Genre
@router.delete("/{id}")
async def delete_genre(id: int, db: Session = Depends(get_db)):
    rows_deleted = db.query(Genre).filter(Genre.id == id).delete()

    if rows_deleted == 0:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    db.commit()
    return {"message": f"Genre {id} deleted"}

# Add Genre to Database
@router.post("/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
async def add_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    try:
        db_genre = Genre(name=genre.name)
        db.add(db_genre) 
        db.commit()
        db.refresh(db_genre)
        return db_genre
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Genre already exists")
    except Exception as e:
        db.rollback()
        # More specific error for debugging
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create genre: {str(e)}")
    
@router.get("/health-check")
async def database_health_check(db: Session = Depends(get_db)):
    try:
        # Fixed: Use text() wrapper for raw SQL
        result = db.execute(text("SELECT 1 as test")).fetchone()
        
        # Count existing genres - this uses ORM so no text() needed
        genre_count = db.query(Genre).count()
        
        # Try to fetch one genre (if any exist)
        sample_genre = db.query(Genre).first()
        
        return {
            "status": "healthy",
            "connection_test": result[0] if result else None,
            "total_genres": genre_count,
            "sample_genre": sample_genre.name if sample_genre else "No genres found"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "error_type": type(e).__name__
        }