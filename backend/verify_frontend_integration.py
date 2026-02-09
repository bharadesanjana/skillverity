import requests
import json

BASE_URL = "http://localhost:8000"

def verify_frontend_flow():
    # 0. Authenticate
    email = "frontend_test@example.com"
    password = "password123"
    print("0. Authenticating...")
    
    # We can try to login directly, if fails, register (but user likely exists from create_test_roadmap.py)
    resp = requests.post(f"{BASE_URL}/token", data={"username": email, "password": password})
    if resp.status_code != 200:
        # Try register if login fails (unlikely if ran sequential)
        requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})
        resp = requests.post(f"{BASE_URL}/token", data={"username": email, "password": password})
        
    if resp.status_code != 200:
        print(f"❌ Login failed: {resp.text}")
        return

    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Fetch Roadmap (simulate frontend load)
    # We need a roadmap ID. Use the one we created.
    roadmap_id = 21 
    
    print(f"\n1. Fetching Roadmap {roadmap_id}...")
    try:
        resp = requests.get(f"{BASE_URL}/roadmaps/{roadmap_id}", headers=headers)
        if resp.status_code == 200:
            roadmap = resp.json()
            print("✅ Roadmap Fetched")
            # Verify structure
            weeks = roadmap.get("content", {}).get("weeks", [])
            print(f"   Found {len(weeks)} weeks")
            if len(weeks) > 0 and isinstance(weeks[0].get("tasks"), list):
                 print("   ✅ Tasks structure confirmed (New Format)")
            else:
                 print("   ⚠️ Tasks structure mismatch or legacy format")
        else:
             print(f"❌ Failed to fetch roadmap: {resp.status_code}")
             return
    except Exception as e:
        print(f"❌ Error fetching roadmap: {e}")
        return

    # 2. Verify Verification Endpoints (simulate Modal interactions)
    print("\n2. Testing Verification Endpoints (Modal Flow)...")
    
    # Generate
    gen_payload = {
        "role": "Frontend Developer",
        "week": 1,
        "title": "Test Week",
        "skills": ["React"],
        "tasks": ["Build Button"]
    }
    print("   -> Generating Assessment...")
    resp = requests.post(f"{BASE_URL}/verification/generate", json=gen_payload)
    if resp.status_code == 200:
        print("   ✅ Assessment API working")
        q = resp.json().get("questions", [])[0]
        question_text = q.get("question")
        print(f"      Question: {question_text[:50]}...")
    else:
        print(f"   ❌ Generation failed: {resp.text}")
        return

    # Evaluate
    print("   -> Evaluating Answer...")
    eval_payload = {
        "role": "Frontend Developer",
        "week": 1,
        "skill_focus": "React",
        "question": question_text,
        "answer": "React components use props."
    }
    resp = requests.post(f"{BASE_URL}/verification/evaluate", json=eval_payload)
    if resp.status_code == 200:
         print("   ✅ Evaluation API working")
    else:
         print(f"   ❌ Evaluation failed: {resp.text}")

if __name__ == "__main__":
    verify_frontend_flow()
