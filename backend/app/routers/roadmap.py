from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app import models, schemas, deps
from app.database import get_db
# Import our new service
from app.services import ai_roadmap

router = APIRouter()

class RoadmapCreate(schemas.BaseModel):
    role_title: str
    
class RoadmapResponse(schemas.BaseModel):
    id: int
    role_title: str
    content: dict # We store full structure here
    status: str
    class Config:
        from_attributes = True

@router.post("/", response_model=RoadmapResponse)
def create_roadmap(
    roadmap_in: RoadmapCreate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Check if user already has an active roadmap for this role?
    # User requirement: "No Create Roadmap... Selecting a role automatically generates..."
    # We allow multiple roadmaps but maybe one active per role.
    
    # 2. Call Gemini Service
    ai_data = ai_roadmap.generate_roadmap_content(roadmap_in.role_title)
    
    # 3. Create Roadmap Record
    db_roadmap = models.Roadmap(
        user_id=current_user.id,
        role_title=ai_data.get("role_title", roadmap_in.role_title),
        content=ai_data,
        status="active"
    )
    db.add(db_roadmap)
    db.commit()
    db.refresh(db_roadmap)
    
    # 4. Flatten Phases into RoadmapItems for tracking
    # We want to track individual skills in the relational DB for the dashboard
    phases = ai_data.get("phases", [])
    for phase in phases:
        for item in phase.get("items", []):
            db_item = models.RoadmapItem(
                roadmap_id=db_roadmap.id,
                title=item.get("title"),
                description=item.get("description"),
                resource_url=item.get("resource_url"),
                status="pending"
            )
            db.add(db_item)
    
    db.commit()
    
    return db_roadmap

@router.get("/", response_model=List[RoadmapResponse])
def get_roadmaps(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    return current_user.roadmaps

@router.get("/{id}", response_model=RoadmapResponse)
def get_roadmap(
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    roadmap = db.query(models.Roadmap).filter(models.Roadmap.id == id, models.Roadmap.user_id == current_user.id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return roadmap
