from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import random

from app import models, schemas, deps
from app.database import get_db

router = APIRouter()

@router.post("/generate/{roadmap_item_id}", response_model=schemas.QuizResponse)
def generate_quiz(
    roadmap_item_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    # Verify roadmap item belongs to user
    roadmap_item = db.query(models.RoadmapItem).join(models.Roadmap).filter(
        models.RoadmapItem.id == roadmap_item_id,
        models.Roadmap.user_id == current_user.id
    ).first()
    
    if not roadmap_item:
        raise HTTPException(status_code=404, detail="Roadmap item not found")

    # Check if quiz exists
    if roadmap_item.quiz:
        return roadmap_item.quiz

    # Dummy Question Generation (In real app, this comes from AI/VectorStore)
    questions = [
        {
            "id": 1,
            "text": "What is the capital of Python?",
            "options": ["Snake City", "Guido's House", "None (It's a language)", "C++"],
            "correct_option": 2
        },
        {
            "id": 2,
            "text": "Which method is used to add an item to a list?",
            "options": [".push()", ".add()", ".append()", ".insert()"],
            "correct_option": 2
        },
        {
             "id": 3,
            "text": "What is 2 + 2 in Python?",
            "options": ["4", "22", "Error", "None"],
            "correct_option": 0
        }
    ]
    
    db_quiz = models.Quiz(
        roadmap_item_id=roadmap_item_id,
        questions=questions,
        score=None,
        passed=False,
        attempts=0
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@router.post("/{id}/submit", response_model=schemas.QuizResponse)
def submit_quiz(
    id: int,
    submission: schemas.QuizSubmission,
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    quiz = db.query(models.Quiz).join(models.RoadmapItem).join(models.Roadmap).filter(
        models.Quiz.id == id,
        models.Roadmap.user_id == current_user.id
    ).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    if quiz.passed:
        raise HTTPException(status_code=400, detail="Quiz already passed")

    # Evaluation
    correct_count = 0
    questions = quiz.questions
    
    if len(submission.answers) != len(questions):
        raise HTTPException(status_code=400, detail="Invalid number of answers")
        
    for i, q in enumerate(questions):
        if submission.answers[i] == q["correct_option"]:
            correct_count += 1
            
    score = (correct_count / len(questions)) * 100
    quiz.score = score
    quiz.attempts += 1
    
    if score >= 70:
        quiz.passed = True
        # Award Badge
        badge_name = f"Mastery: {quiz.roadmap_item.title}"
        existing_badge = db.query(models.Badge).filter(models.Badge.user_id == current_user.id, models.Badge.name == badge_name).first()
        if not existing_badge:
            new_badge = models.Badge(
                user_id=current_user.id,
                name=badge_name,
                description=f"Passed quiz for {quiz.roadmap_item.title} with {score}%"
            )
            db.add(new_badge)
            
        # Update Item Status
        quiz.roadmap_item.status = "verified"
    
    db.commit()
    db.refresh(quiz)
    return quiz
