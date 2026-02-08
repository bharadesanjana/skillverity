import sys
import os

# MANUAL ENV LOADING
print("Loading environment...")
env_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                if not os.environ.get(key):
                    os.environ[key] = value
else:
    print("WARNING: .env not found!")

if not os.environ.get('GEMINI_API_KEY'):
    print("CRITICAL: GEMINI_API_KEY not found in env!")

# Add backend to path
sys.path.append(os.getcwd())

from app.services import ai_roadmap

print("Calling generate_weekly_quiz()...")

try:
    questions = ai_roadmap.generate_weekly_quiz(
        role="React Developer", 
        week_number=1, 
        focus="React Basics", 
        topics="Components, Props, State", 
        tasks="Build a counter app"
    )
    
    print(f"Generated {len(questions)} questions.")
    if len(questions) >= 8:
        print("SUCCESS: High Quality constraints met.")
    else:
        print(f"WARNING: Count {len(questions)} < 8 (Fallback used?).")
    
    if questions:
        print(f"Sample: {questions[0].get('text')}")
        
except Exception as e:
    print(f"Script Error: {e}")
