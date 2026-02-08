import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"

# 1. Login to get token
def login(email, password):
    # Route is /token, not /auth/token
    response = requests.post(f"{BASE_URL}/token", data={"username": email, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    print(f"Login failed: {response.text}")
    return None

# 2. Create Roadmap
def create_roadmap(token, role):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"role_title": role}
    response = requests.post(f"{BASE_URL}/roadmaps/", json=data, headers=headers)
    
    if response.status_code == 200:
        print("\n✅ Roadmap created successfully!")
        print(json.dumps(response.json(), indent=2))
        return response.json()["id"]
    else:
        print(f"\n❌ Failed to create roadmap: {response.text}")
        return None

if __name__ == "__main__":
    # Assuming test user from previous sessions or seeds
    # If not, I might need to register one. Let's try test@example.com / password123
    email = "test@example.com"
    password = "password123"
    
    # Or I can just check the db first to see a valid user? 
    # Whatever, let's try to register first just in case.
    try:
        register_resp = requests.post(f"{BASE_URL}/register", json={"email": email, "password": password, "full_name": "Test User"})
        if register_resp.status_code == 200:
            print("Registered new test user.")
        else:
            print(f"User probably exists (or error: {register_resp.status_code}), proceeding to login.")
    except:
        pass

    token = login(email, password)
    if token:
        create_roadmap(token, "Frontend Developer")
