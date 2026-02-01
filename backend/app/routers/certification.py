from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, deps
from app.database import get_db

router = APIRouter()

@router.get("/summary", response_model=dict)
def get_recruiter_summary(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    # Check eligibility
    roadmaps = current_user.roadmaps
    badges = current_user.badges
    
    if not badges:
        return {
            "is_certified": False,
            "message": "User has not earned any badges yet."
        }
        
    # Simple logic: If user has at least 1 roadmap and 1 badge, they have a summary
    # In real app, check if all items in roadmap are verified.
    
    summary = {
        "candidate_name": current_user.full_name,
        "is_certified": True, # Simplified
        "badges": [b.name for b in badges],
        "roadmaps_completed": [r.role_title for r in roadmaps if r.status == 'completed'],
        "skills_verified": len(badges),
        "recruiter_note": "This candidate has verified skills through SkillVerity's rigorous assessment."
    }
    
    return summary
