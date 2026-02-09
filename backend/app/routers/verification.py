from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app import schemas
from app.services import ai_verification

router = APIRouter()

@router.post("/generate", response_model=schemas.VerificationResponse)
def generate_assessment(request: schemas.VerificationGenerateRequest):
    try:
        data = ai_verification.generate_verification_assessment(
            role=request.role,
            week_number=request.week,
            week_title=request.title,
            skills=request.skills,
            tasks=request.tasks
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate", response_model=schemas.EvaluationResponse)
def evaluate_response(request: schemas.EvaluationRequest):
    try:
        data = ai_verification.evaluate_response(
            role=request.role,
            week_number=request.week,
            skill_focus=request.skill_focus,
            question=request.question,
            user_answer=request.answer
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/followup")
def generate_followup(request: schemas.FollowupRequest):
    try:
        data = ai_verification.generate_followup(request.summary)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
