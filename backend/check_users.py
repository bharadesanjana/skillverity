from app.database import SessionLocal
from app.models import User

db = SessionLocal()
users = db.query(User).all()

print(f"Found {len(users)} users:")
for user in users:
    print(f"ID: {user.id}, Email: {user.email}, Hashed Password: {user.hashed_password}")

db.close()
