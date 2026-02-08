import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.services import ai_roadmap
import json

def test_generation():
    role = "Python Backend Developer"
    print(f"Testing generation for: {role}")
    
    try:
        data = ai_roadmap.generate_roadmap_content(role)
        print("\nGenerated Data:")
        print(json.dumps(data, indent=2))
        
        # Verify structure
        if "roadmap" in data and isinstance(data["roadmap"], list):
            print("\n✅ Structure is valid (contains 'roadmap' list)")
            if len(data["roadmap"]) == 6:
                 print("✅ Structure is valid (contains 6 weeks)")
            else:
                 print(f"❌ Warning: Expected 6 weeks, got {len(data['roadmap'])}")
        else:
            print("\n❌ Invalid structure")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_generation()
