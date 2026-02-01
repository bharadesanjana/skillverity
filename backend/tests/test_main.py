import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from main import app
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to SkillVerity API"}

def test_create_user():
    response = client.post(
        "/register",
        json={"email": "test@example.com", "password": "password123", "full_name": "Test User"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login_user():
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert "access_token" in data
    assert data["token_type"] == "bearer"

if __name__ == "__main__":
    try:
        test_read_main()
        print("test_read_main PASSED")
        test_create_user()
        print("test_create_user PASSED")
        test_login_user()
        print("test_login_user PASSED")
    except Exception as e:
        import traceback
        traceback.print_exc()
