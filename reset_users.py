from sqlalchemy import create_engine, text
from app.database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("DELETE FROM users"))
    conn.commit()
    print("All users deleted. You can register again.")
