import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def create_roadmap():
    print("--- Creating Test Roadmap ---")
    
    # 1. Login/Register (to get token)
    email = "frontend_test@example.com"
    password = "password123"
    
    # Register
    requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})
    
    # Login
    resp = requests.post(f"{BASE_URL}/token", data={"username": email, "password": password})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return None
        
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create Roadmap
    payload = {"role_title": "Frontend Developer", "duration_weeks": 4}
    resp = requests.post(f"{BASE_URL}/roadmaps/", json=payload, headers=headers)
    
    if resp.status_code == 200:
        roadmap = resp.json()
        print(f"✅ Created Roadmap ID: {roadmap['id']}")
        return roadmap['id']
    else:
        print(f"❌ Failed to create roadmap: {resp.text}")
        return None

if __name__ == "__main__":
    rid = create_roadmap()
    if rid:
        with open("test_roadmap_id.txt", "w") as f:
            f.write(str(rid))
