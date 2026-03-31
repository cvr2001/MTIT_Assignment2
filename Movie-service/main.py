from fastapi import FastAPI, HTTPException, status
from models import Movie, MovieCreate, MovieUpdate
from service import MovieService
from typing import List

app = FastAPI(title="Movie Microservice", version="1.0.0")

movie_service = MovieService()

@app.get("/")
def read_root():
    return {"message": "Movie Microservice is running"}

# Get all movies
@app.get("/api/movies", response_model=List[Movie])
def get_all_movies():
    return movie_service.get_all()

# Get movie by ID
@app.get("/api/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    movie = movie_service.get_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# Create movie
@app.post("/api/movies", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate):
    return movie_service.create(movie)

# Update movie
@app.put("/api/movies/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie: MovieUpdate):
    updated_movie = movie_service.update(movie_id, movie)
    if not updated_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie

# Delete movie
@app.delete("/api/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):
    success = movie_service.delete(movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return None