from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
import json

from app import models, schemas, deps
from app.database import get_db
# Import our new service
from app.services import ai_roadmap

router = APIRouter()

class RoadmapResponse(schemas.BaseModel):
    id: int
    role_title: str
    content: dict # We store full structure here
    status: str
    items: List[schemas.RoadmapItemBase] = []
    model_config = schemas.ConfigDict(from_attributes=True)

from app.mongo import roadmaps_collection
from datetime import datetime
import traceback

@router.post("/", response_model=RoadmapResponse)
def create_roadmap(
    roadmap_in: schemas.RoadmapCreate,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # 1. Generate Content
        # print(f"DEBUG: Generating roadmap for {roadmap_in.role_title} ({roadmap_in.duration_weeks} weeks)")
        ai_data = ai_roadmap.generate_roadmap_content(roadmap_in.role_title, roadmap_in.duration_weeks)
        
        # 2. Save to MongoDB (Full JSON)
        mongo_id = None
        if roadmaps_collection is not None:
            try:
                mongo_doc = {
                    "user_id": current_user.id, # Storing SQL ID for reference
                    "user_email": current_user.email,
                    "role_title": roadmap_in.role_title,
                    "duration_weeks": roadmap_in.duration_weeks,
                    "content": ai_data,
                    "created_at": datetime.utcnow()
                }
                result = roadmaps_collection.insert_one(mongo_doc)
                mongo_id = str(result.inserted_id)
                print(f"DEBUG: Saved roadmap to MongoDB with ID {mongo_id}")
            except Exception as e:
                print(f"ERROR: Failed to save roadmap to MongoDB: {e}")
                traceback.print_exc()

        # 3. Save to SQL (Relational Data for Dashboard)
        role_name = ai_data.get("role", roadmap_in.role_title)
        
        db_roadmap = models.Roadmap(
            user_id=current_user.id,
            role_title=role_name,
            content=ai_data, # SQL also keeps a copy for now, as safety
            status="active"
        )
        db.add(db_roadmap)
        db.commit()
        db.refresh(db_roadmap)

        # 4. Flatten Weeks into RoadmapItems for SQL tracking
        weeks = ai_data.get("roadmap", [])
        for week_data in weeks:
            week_num = week_data.get("week")
            focus = week_data.get("focus")
            
            # Helper to safely join lists
            def safe_join(lst):
                if isinstance(lst, list):
                    return ", ".join(lst)
                return str(lst) if lst else ""

            topics = safe_join(week_data.get("topics"))
            # 'tasks' is the new field, 'practice' is legacy. Support both.
            tasks_list = week_data.get("tasks") or week_data.get("practice")
            tasks = safe_join(tasks_list)
            outcome = week_data.get("outcome") or ""
            
            description = f"Topics: {topics}\nTasks: {tasks}\nOutcome: {outcome}"
            
            db_item = models.RoadmapItem(
                roadmap_id=db_roadmap.id,
                title=f"Week {week_num}: {focus}",
                description=description,
                resource_url="", 
                status="pending"
            )
            db.add(db_item)
            db.flush() # Flush to get db_item.id

            # 4b. Pre-populate Quiz if available
            weekly_quiz = week_data.get("weekly_quiz")
            if weekly_quiz:
                # print(f"DEBUG: Saving quiz for Item {db_item.id} with {len(weekly_quiz)} questions")
                db_quiz = models.Quiz(
                    roadmap_item_id=db_item.id,
                    questions=weekly_quiz,
                    score=None,
                    passed=False,
                    attempts=0
                )
                db.add(db_quiz)
        
        # 5. Handle Final Assessment (Create as a special RoadmapItem)
        final_assessment = ai_data.get("final_assessment")
        if final_assessment:
            # print(f"DEBUG: Saving Final Assessment")
            final_item = models.RoadmapItem(
                roadmap_id=db_roadmap.id,
                title="Final Assessment",
                description="Comprehensive evaluation of all skills.",
                resource_url="",
                status="pending"
            )
            db.add(final_item)
            db.flush()
            
            final_questions = final_assessment.get("questions", [])
            if final_questions:
                final_quiz = models.Quiz(
                    roadmap_item_id=final_item.id,
                    questions=final_questions,
                    score=None,
                    passed=False,
                    attempts=0
                )
                db.add(final_quiz)

        db.commit()
        return db_roadmap

    except Exception as e:
        print(f"CRITICAL ERROR in create_roadmap: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

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
    roadmap = db.query(models.Roadmap).options(joinedload(models.Roadmap.items)).filter(models.Roadmap.id == id, models.Roadmap.user_id == current_user.id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return roadmap
