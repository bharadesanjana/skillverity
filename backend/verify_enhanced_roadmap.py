import requests
import json
import time

BASE_URL = "http://localhost:8000"
EMAIL = "enhanced_test@example.com"
PASSWORD = "password123"

def run_verification():
    print("--- Verifying Enhanced Roadmap & Assessment ---")
    session = requests.Session()

    # 1. Login/Register
    print("1. Authenticating...")
    login_resp = session.post(f"{BASE_URL}/token", data={"username": EMAIL, "password": PASSWORD})
    if login_resp.status_code != 200:
        session.post(f"{BASE_URL}/register", json={"email": EMAIL, "password": PASSWORD, "full_name": "Enhanced Tester"})
        login_resp = session.post(f"{BASE_URL}/token", data={"username": EMAIL, "password": PASSWORD})
    
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Authenticated.")

    # 2. Create Roadmap
    print("2. Creating Enhanced Roadmap...")
    # Using 1 week to save tokens/time, but prompt should respect it.
    resp = session.post(f"{BASE_URL}/roadmaps/", json={"role_title": "Python Developer", "duration_weeks": 1}, headers=headers)
    if resp.status_code != 200:
        print(f"❌ Creation failed: {resp.text}")
        return
    
    roadmap = resp.json()
    roadmap_id = roadmap["id"]
    print(f"✅ Created Roadmap ID: {roadmap_id}")

    # 3. Check Structure (Tasks field)
    content = roadmap["content"]
    weeks = content.get("weeks", [])
    if weeks and ("tasks" in weeks[0]):
        tasks = weeks[0].get('tasks')
        print(f"✅ Roadmap has tasks: {len(tasks)} tasks found.")
        if len(tasks) > 0 and isinstance(tasks[0], dict):
             print(f"   Task 1: {tasks[0].get('task')} (Diff: {tasks[0].get('difficulty')})")
    else:
        print("❌ 'tasks' field missing in JSON content.")

    # 4. Check Items & Final Assessment
    print("4. Checking Roadmap Items & Quizzes...")
    # Fetch again to get items just in case (though create returns them usually empty in some schemas? No, it should be there)
    # The `create_roadmap` returns `db_roadmap` which has items but might not be eager loaded in the return object if not refreshed/configured.
    # Let's fetch explicitly.
    get_resp = session.get(f"{BASE_URL}/roadmaps/{roadmap_id}", headers=headers)
    items = get_resp.json()["items"]
    
    final_assessment_found = False
    week_quiz_found = False
    
    for item in items:
        print(f"   Item: {item['title']} (ID: {item['id']})")
        
        # Check if quiz exists for this item
        # We need to hit the generate endpoint to see if it returns existing? 
        # Or checking the DB directly?
        # The `generate` endpoint returns the quiz.
        quiz_resp = session.post(f"{BASE_URL}/quizzes/generate/{item['id']}", headers=headers)
        if quiz_resp.status_code == 200:
            q_data = quiz_resp.json()
            print(f"      ✅ Quiz found: {len(q_data['questions'])} questions")
            if item['title'] == "Final Assessment":
                final_assessment_found = True
            else:
                week_quiz_found = True
        else:
            print(f"      ❌ Quiz missing for item {item['id']}")

    if final_assessment_found:
        print("✅ Final Assessment created and has quiz.")
    else:
        print("❌ Final Assessment NOT found.")

    if week_quiz_found:
        print("✅ Weekly Quiz created.")
    else:
        print("❌ Weekly Quiz NOT found.")

if __name__ == "__main__":
    run_verification()
