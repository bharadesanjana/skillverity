from app.mongo import roadmaps_collection
import sys
import os

# Ensure we can import app
sys.path.append(os.getcwd())

def verify_mongo():
    if roadmaps_collection is None:
        print("❌ MongoDB collection not available (connection failed?)")
        return

    print("Checking MongoDB 'roadmaps' collection...")
    try:
        # Get the most recent roadmap
        recent_roadmap = roadmaps_collection.find_one(sort=[("created_at", -1)])
        
        if recent_roadmap:
            print("✅ Found a roadmap in MongoDB!")
            print(f"   ID: {recent_roadmap.get('_id')}")
            print(f"   Role: {recent_roadmap.get('role_title')}")
            print(f"   Duration: {recent_roadmap.get('duration_weeks')} weeks")
            
            if recent_roadmap.get('duration_weeks') == 2:
                print("   ✅ Duration matches request (2 weeks)")
            else:
                print(f"   ❌ Duration mismatch! Expected 2, got {recent_roadmap.get('duration_weeks')}")
                
            content = recent_roadmap.get('content', {})
            roadmap_list = content.get('roadmap', [])
            print(f"   Weeks in Content: {len(roadmap_list)}")
        else:
            print("❌ No roadmaps found in MongoDB.")
            
    except Exception as e:
        print(f"❌ Error querying MongoDB: {e}")

if __name__ == "__main__":
    verify_mongo()
