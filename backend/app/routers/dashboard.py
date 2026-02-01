from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, deps
from app.schemas_dashboard import DashboardSummary, NextAction, DashboardBadge

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Roadmaps Count
    roadmaps = db.query(models.Roadmap).filter(models.Roadmap.user_id == current_user.id).all()
    active_roadmaps = len([r for r in roadmaps if r.status == "active"])
    
    # 2. Skills Progress
    total_skills = 0
    verified_skills = 0
    next_item = None
    
    for r in roadmaps:
        for item in r.items:
            total_skills += 1
            if item.status == "verified":
                verified_skills += 1
            elif item.status == "pending" and next_item is None:
                # Naively pick the first pending item as next action
                next_item = item
                # Also store roadmap info for it
                next_roadmap = r
    
    overall_progress = (verified_skills / total_skills * 100) if total_skills > 0 else 0
    readiness_score = (verified_skills / (total_skills or 1) * 100) * 1.2 # Make it a bit more optimistic for demo
    if readiness_score > 100: readiness_score = 100

    # 3. Next Action
    action = None
    if next_item and next_roadmap:
        action = NextAction(
            item_title=next_item.title,
            roadmap_id=next_roadmap.id,
            roadmap_title=next_roadmap.role_title,
            estimated_time="45 mins"
        )
    elif not next_item and len(roadmaps) > 0:
         # Everything completed
         pass 

    # 4. Badges
    db_badges = current_user.badges
    badges_response = [
        DashboardBadge(
            name=b.name, 
            description=b.description, 
            awarded_at=b.awarded_at.strftime("%Y-%m-%d")
        ) for b in db_badges[-5:] # Last 5
    ]

    return DashboardSummary(
        active_roadmaps=active_roadmaps,
        skills_completed=verified_skills,
        total_skills=total_skills,
        overall_progress=round(overall_progress, 1),
        streak=3, # Mock streak for demo
        readiness_score=round(readiness_score, 1),
        next_action=action,
        badges=badges_response
    )
