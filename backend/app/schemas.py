from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Quiz Schemas ---
# Based on quiz.py usage
class Question(BaseModel):
    id: int
    text: str
    options: List[str]
    correct_option: Optional[int] = None # Hidden in client response ideally, but defined here

class QuizBase(BaseModel):
    pass

class QuizCreate(QuizBase):
    roadmap_item_id: int

class QuizSubmission(BaseModel):
    answers: List[int]

class QuizResponse(BaseModel):
    id: int
    roadmap_item_id: int
    questions: List[Dict[str, Any]] # Or List[Question]
    score: Optional[float] = None
    passed: bool
    attempts: int
    
    model_config = ConfigDict(from_attributes=True)

# --- Roadmap AI Schemas ---
class RoadmapWeek(BaseModel):
    week: int
    focus: str
    topics: List[str]
    practice: List[str]
    outcome: str

class RoadmapItemBase(BaseModel):
    id: int
    title: str
    status: str
    model_config = ConfigDict(from_attributes=True)

class RoadmapCreate(BaseModel):
    role_title: str
    duration_weeks: int = 6

class RoadmapResponse(BaseModel):
    id: int
    role_title: str
    content: dict
    status: str
    items: List[RoadmapItemBase] = []
    model_config = ConfigDict(from_attributes=True)
