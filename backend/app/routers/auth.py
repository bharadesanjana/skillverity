from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_db
from app import models, schemas
from app import auth as auth_utils # Import the utilities we kept
from datetime import timedelta

router = APIRouter()

from app.mongo import users_collection

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(f"DEBUG: Registering user {user.email}")
    
    # 1. Check for existing email (SQL)
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 1b. Check for existing email (MongoDB)
    if users_collection is not None:
        mongo_user = users_collection.find_one({"email": user.email})
        if mongo_user:
             raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash password
    hashed_password = auth_utils.get_password_hash(user.password)

    # 3. Create User object (SQL)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )

    # 4. Add to DB and Commit (SQL)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    # 5. Add to MongoDB (Dual Write)
    if users_collection is not None:
        try:
            mongo_user_doc = {
                "sql_id": new_user.id, # Link to SQL ID
                "email": user.email,
                "hashed_password": hashed_password,
                "full_name": user.full_name,
                "created_at": new_user.created_at
            }
            users_collection.insert_one(mongo_user_doc)
            print(f"DEBUG: User {user.email} saved to MongoDB")
        except Exception as e:
            print(f"ERROR: Failed to save to MongoDB: {e}")
            # Optional: Decide if we rollback SQL? For now, we log error but keep SQL.

    return new_user

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate against MongoDB if available, otherwise fallback to SQL
    
    user_email = form_data.username
    password = form_data.password
    
    user = None # This will be an object with .email and .hashed_password
    
    # Try MongoDB First
    if users_collection is not None:
        mongo_user = users_collection.find_one({"email": user_email})
        if mongo_user:
            print(f"DEBUG: Found user {user_email} in MongoDB")
            # Create a simple object-like wrapper or dict access
            class MongoUser:
                email = mongo_user["email"]
                hashed_password = mongo_user["hashed_password"]
            user = MongoUser()
    
    # Fallback to SQL if not found in Mongo (for legacy users)
    if not user:
        print(f"DEBUG: User {user_email} not in Mongo, checking SQL")
        user = db.query(models.User).filter(models.User.email == user_email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not auth_utils.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate Token
    access_token_expires = timedelta(minutes=30)
    access_token = auth_utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
