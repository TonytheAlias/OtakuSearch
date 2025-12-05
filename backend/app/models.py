from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Table,Date
from sqlalchemy.orm import relationship
from .database import Base

anime_genres = Table(
	'anime_genres',
	Base.metadata,
	Column('anime_id', Integer, ForeignKey('anime.id'), primary_key=True),
	Column('genre_id', Integer, ForeignKey('genre.id'), primary_key=True)
)
media_relations = Table(
    'media_relations',
    Base.metadata,
    Column('source_media_id', Integer, ForeignKey('anime.id'),primary_key=True),
    Column('related_media_id', Integer, ForeignKey('anime.id'), primary_key=True),
    Column('relation_type', String(50), nullable=False)
)
class Anime(Base):
    __tablename__ = "anime"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    alt_titles = Column(Text)
    description = Column(Text)
    image_url = Column(Text)
    type = Column(String(50))
    original_format = Column(String(50))
    source_material = Column(String(200))
    release_year = Column(Date)
    aired_from = Column(Date)
    aired_to = Column(Date)
    status = Column(String(30))
    episodes = Column(Integer)
    chapters = Column(Integer)
    volumes = Column(Integer)
    duration_minutes = Column(Integer)
    popularity = Column(Integer)
    rating = Column(Float)
    author = Column(String(200))
    studio = Column(String(200))
    serialization = Column(String(100))

    genres = relationship("Genre", secondary=anime_genres, back_populates="anime")
    related_media = relationship(
        "Anime",
        secondary=media_relations,
        primaryjoin=id == media_relations.c.source_media_id,
        secondaryjoin=id == media_relations.c.related_media_id,
        backref="sources"
    )

class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    anime = relationship("Anime", secondary=anime_genres, back_populates="genres")