from fastapi import FastAPI
from app.routers import anime,genre
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(anime.router)
app.include_router(genre.router)

@app.get("/")
def root():
    return {"message": "Welcome to the OtakuSearch API"}
