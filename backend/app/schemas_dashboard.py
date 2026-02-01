from pydantic import BaseModel
from typing import List, Optional

class NextAction(BaseModel):
    item_title: str
    roadmap_id: int
    roadmap_title: str
    estimated_time: str = "45 mins" # Hardcoded for MVP or can be calculated

class DashboardBadge(BaseModel):
    name: str
    description: str
    awarded_at: str

class DashboardSummary(BaseModel):
    active_roadmaps: int
    skills_completed: int
    total_skills: int
    overall_progress: float
    streak: int
    readiness_score: float
    next_action: Optional[NextAction] = None
    badges: List[DashboardBadge] = []
