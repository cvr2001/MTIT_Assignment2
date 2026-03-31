from fastapi import FastAPI, HTTPException, status
from models import Theater, TheaterCreate, TheaterUpdate
from service import TheaterService
from typing import List

app = FastAPI(title="Theater Microservice", version="1.0.0")

theater_service = TheaterService()

@app.get("/")
def read_root():
    return {"message": "Theater Microservice is running"}

# Get all theaters
@app.get("/api/theaters", response_model=List[Theater])
def get_all_theaters():
    return theater_service.get_all()

# Get theater by ID
@app.get("/api/theaters/{theater_id}", response_model=Theater)
def get_theater(theater_id: int):
    theater = theater_service.get_by_id(theater_id)
    if not theater:
        raise HTTPException(status_code=404, detail="Theater not found")
    return theater

# Create theater
@app.post("/api/theaters", response_model=Theater, status_code=status.HTTP_201_CREATED)
def create_theater(theater: TheaterCreate):
    return theater_service.create(theater)

# Update theater
@app.put("/api/theaters/{theater_id}", response_model=Theater)
def update_theater(theater_id: int, theater: TheaterUpdate):
    updated_theater = theater_service.update(theater_id, theater)
    if not updated_theater:
        raise HTTPException(status_code=404, detail="Theater not found")
    return updated_theater

# Delete theater
@app.delete("/api/theaters/{theater_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_theater(theater_id: int):
    success = theater_service.delete(theater_id)
    if not success:
        raise HTTPException(status_code=404, detail="Theater not found")
    return None