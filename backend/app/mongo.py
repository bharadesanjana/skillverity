from pymongo import MongoClient
from app.config import settings
import sys

# Initialize MongoDB Client
MONGO_URL = settings.MONGODB_URL if hasattr(settings, "MONGODB_URL") else None

# Fallback if settings doesn't have it yet (during dev reload)
if not MONGO_URL:
    import os
    from dotenv import load_dotenv
    load_dotenv()
    MONGO_URL = os.getenv("MONGODB_URL")

try:
    if not MONGO_URL:
        print("WARNING: MONGODB_URL not found in settings or .env", file=sys.stderr)
        client = None
        db = None
        users_collection = None
    else:
        client = MongoClient(MONGO_URL)
        # Select Database (Parsing from URL or default)
        # The URL provided is: mongodb+srv://.../cluster0?appName=Cluster0
        # The default db is usually 'test' if not specified. Let's use 'skillverity_db' explicitly.
        db = client["skillverity_db"]
        users_collection = db["users"]
        roadmaps_collection = db["roadmaps"]
        
        # Verify connection
        client.admin.command('ping')
        print("MongoDB Connected Successfully")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}", file=sys.stderr)
    client = None
    db = None
    users_collection = None
    roadmaps_collection = None
