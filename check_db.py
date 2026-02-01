from sqlalchemy import create_engine, inspect, text
import os

DB_PATH = "backend/sql_app.db"
URL = f"sqlite:///{DB_PATH}"

print(f"Checking database at: {DB_PATH}")
if not os.path.exists(DB_PATH):
    print("ERROR: Database file not found!")
    exit(1)

engine = create_engine(URL)
inspector = inspect(engine)

print("\n--- Tables ---")
tables = inspector.get_table_names()
print(tables)

if "users" in tables:
    print("\n--- Users Table Schema ---")
    for col in inspector.get_columns("users"):
        print(f"{col['name']} ({col['type']})")

    print("\n--- User Count ---")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM users"))
        print(f"Total Users: {result.scalar()}")
else:
    print("\nERROR: 'users' table DOES NOT EXIST.")
