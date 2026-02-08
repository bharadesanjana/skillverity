import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
# Use the demo user credentials or create one
EMAIL = "test_quiz@example.com"
PASSWORD = "password123"

def run_verification():
    print("--- Verifying AI Quiz and Verification Flow ---")
    session = requests.Session()

    # 1. Login
    print(f"1. Logging in as {EMAIL}...")
    try:
        login_resp = session.post(f"{BASE_URL}/token", data={"username": EMAIL, "password": PASSWORD})
        if login_resp.status_code != 200:
            # Register if login fails
            print("   Login failed, trying registration...")
            reg_resp = session.post(f"{BASE_URL}/register", json={"email": EMAIL, "password": PASSWORD, "full_name": "Quiz Tester"})
            if reg_resp.status_code != 200:
                print(f"❌ Registration failed: {reg_resp.text}")
                return
            login_resp = session.post(f"{BASE_URL}/token", data={"username": EMAIL, "password": PASSWORD})
        
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Logged in.")
    except Exception as e:
        print(f"❌ Auth failed: {e}")
        return

    # 2. Create Roadmap (if needed)
    print("2. Creating/Fetching Roadmap...")
    roadmap_id = None
    roadmap_resp = session.post(f"{BASE_URL}/roadmaps/", json={"role_title": "Quiz Tester Role", "duration_weeks": 2}, headers=headers)
    if roadmap_resp.status_code == 200:
        roadmap_data = roadmap_resp.json()
        roadmap_id = roadmap_data["id"]
        print(f"✅ Created Roadmap ID: {roadmap_id}")
    else:
        print(f"❌ Roadmap creation failed: {roadmap_resp.text}")
        return

    # 3. Get Roadmap Items to find ID for Week 1
    print("3. Fetching Roadmap Items...")
    # The /roadmaps/{id} endpoint now returns items!
    get_roadmap_resp = session.get(f"{BASE_URL}/roadmaps/{roadmap_id}", headers=headers)
    if get_roadmap_resp.status_code != 200:
        print(f"❌ Fetch roadmap failed: {get_roadmap_resp.text}")
        return
    
    data = get_roadmap_resp.json()
    items = data.get("items", [])
    if not items:
        print("❌ No items found in roadmap response. Eager loading might have failed?")
        return
        
    target_item = items[0]
    target_item_id = target_item["id"]
    print(f"✅ Found Item: {target_item['title']} (ID: {target_item_id})")

    # 4. Generate Quiz
    print(f"4. Generating Quiz for Item {target_item_id}...")
    quiz_resp = session.post(f"{BASE_URL}/quizzes/generate/{target_item_id}", headers=headers)
    if quiz_resp.status_code != 200:
        print(f"❌ Quiz generation failed: {quiz_resp.text}")
        return
    
    quiz_data = quiz_resp.json()
    quiz_id = quiz_data["id"]
    questions = quiz_data["questions"]
    print(f"✅ Generated Quiz ID: {quiz_id} with {len(questions)} questions")
    print(f"   Example Q: {questions[0]['text']}")

    # 5. Submit Quiz (Pass)
    print("5. Submitting Passing Answers...")
    # Since we can't see the correct option index usually, but in our mocked schema/AI response debugging we might.
    # But wait, our schemas in backend define `correct_option` in `Question` model.
    # The API returns it? Let's check `QuizResponse`. 
    # Yes, `questions` is `List[Dict[str, Any]]`.
    
    # Cheat: Look at `correct_option` from the response (it might be leaking, which is good for testing, bad for prod)
    # The `QuizResponse` just dumps the JSON column. Pydantic `dict` might hide it if we used strict models, 
    # but `questions` column is JSON, so it likely passes through everything.
    
    answers = []
    for q in questions:
        # In a real app we would hide this. Here we check if it's present.
        if "correct_option" in q:
            answers.append(q["correct_option"])
        else:
            print("   ⚠️ correct_option hidden. Guessing 0.")
            answers.append(0)
            
    submit_resp = session.post(f"{BASE_URL}/quizzes/{quiz_id}/submit", json={"answers": answers}, headers=headers)
    if submit_resp.status_code == 200:
        result = submit_resp.json()
        print(f"✅ Quiz Submitted. Score: {result['score']}% Passed: {result['passed']}")
        
        if result['passed']:
            print("   ✅ PASSED as expected.")
        else:
            print("   ⚠️ FAILED (Did AI give bad questions/options?)")
    else:
        print(f"❌ Submission failed: {submit_resp.text}")

if __name__ == "__main__":
    run_verification()
