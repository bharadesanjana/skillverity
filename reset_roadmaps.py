from sqlalchemy import create_engine, text
from app.database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("DELETE FROM roadmaps"))
    conn.execute(text("DELETE FROM roadmap_items"))
    conn.commit()
    print("All roadmaps deleted. Dashboard will show Role Selector.")
