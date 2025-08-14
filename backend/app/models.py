from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from .database import Base

anime_genres = Table(
	'anime_genres',
	Base.metadata,
	Column('anime_id', Integer, ForeignKey('anime.id'), primary_key=True),
	Column('genre_id', Integer, ForeignKey('genre.id'), primary_key=True)
)

class Anime(Base):
    __tablename__ = "anime"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    alt_titles = Column(Text)  # Could store JSON or comma-separated
    type = Column(String(20))
    description = Column(Text)
    release_year = Column(Integer)
    status = Column(String(20))
    episodes_chapters = Column(Integer)
    image_url = Column(Text)
    popularity = Column(Integer)
    rating = Column(Float)

    genres = relationship("Genre", secondary=anime_genres, back_populates="anime")

class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    anime = relationship("Anime", secondary=anime_genres, back_populates="genres")