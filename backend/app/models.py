from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, JSON, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    roadmaps = relationship("Roadmap", back_populates="user")
    badges = relationship("Badge", back_populates="user")

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_title = Column(String)
    content = Column(JSON)  # Stores the full generated roadmap structure if needed
    status = Column(String, default="active") # active, completed
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="roadmaps")
    items = relationship("RoadmapItem", back_populates="roadmap", cascade="all, delete-orphan")

class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"))
    title = Column(String)
    description = Column(String)
    resource_url = Column(String)
    status = Column(String, default="pending")  # pending, in_progress, verified
    
    roadmap = relationship("Roadmap", back_populates="items")
    quiz = relationship("Quiz", uselist=False, back_populates="roadmap_item")

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_item_id = Column(Integer, ForeignKey("roadmap_items.id"))
    questions = Column(JSON) # List of question objects
    score = Column(Float, nullable=True)
    passed = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)

    roadmap_item = relationship("RoadmapItem", back_populates="quiz")

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String)
    icon_url = Column(String, nullable=True)
    awarded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="badges")
