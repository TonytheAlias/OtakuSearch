from fastapi import FastAPI
from app.routers import anime,genre
app = FastAPI()

app.include_router(anime.router)

@app.get("/")
def root():
    return {"message": "Welcome to the OtakuSearch API"}
