from fastapi import FastAPI, HTTPException, status
from models import Show, ShowCreate, ShowUpdate
from service import ShowService
from typing import List

app = FastAPI(title="Show Microservice", version="1.0.0")

show_service = ShowService()

@app.get("/")
def read_root():
    return {"message": "Show Microservice is running"}

# Get all shows
@app.get("/api/shows", response_model=List[Show])
def get_all_shows():
    return show_service.get_all()

# Get show by ID
@app.get("/api/shows/{show_id}", response_model=Show)
def get_show(show_id: int):
    show = show_service.get_by_id(show_id)
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return show

# Create show
@app.post("/api/shows", response_model=Show, status_code=status.HTTP_201_CREATED)
def create_show(show: ShowCreate):
    return show_service.create(show)

# Update show
@app.put("/api/shows/{show_id}", response_model=Show)
def update_show(show_id: int, show: ShowUpdate):
    updated_show = show_service.update(show_id, show)
    if not updated_show:
        raise HTTPException(status_code=404, detail="Show not found")
    return updated_show

# Delete show
@app.delete("/api/shows/{show_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_show(show_id: int):
    success = show_service.delete(show_id)
    if not success:
        raise HTTPException(status_code=404, detail="Show not found")
    return None