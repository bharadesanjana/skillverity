from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Input CORS settings
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import auth, roadmap, quiz, certification, dashboard

app.include_router(auth.router, tags=["auth"])
app.include_router(roadmap.router, prefix="/roadmaps", tags=["roadmaps"])
app.include_router(quiz.router, prefix="/quizzes", tags=["quizzes"])
app.include_router(certification.router, prefix="/certification", tags=["certification"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

from app.routers import verification
app.include_router(verification.router, prefix="/verification", tags=["verification"])

@app.get("/")
def read_root():
    return {"message": "SkillVerity API Running"}
