import requests
import json

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "demo@skillverity.com"
PASSWORD = "password123"

def verify_duration_roadmap():
    print(f"--- Verifying Custom Duration Roadmap (2 Weeks) ---")
    
    # 1. Login
    print(f"1. Logging in as {EMAIL}...")
    try:
        login_res = requests.post(f"{BASE_URL}/token", data={"username": EMAIL, "password": PASSWORD})
        if login_res.status_code != 200:
            print(f"❌ Login Failed: {login_res.text}")
            return
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("   ✅ Login Success")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    # 2. Create Roadmap (2 Weeks)
    print("\n2. Requesting 2-Week Python Roadmap...")
    payload = {
        "role_title": "Python Automation Engineer",
        "duration_weeks": 2
    }
    
    try:
        res = requests.post(f"{BASE_URL}/roadmaps/", json=payload, headers=headers)
        if res.status_code == 200:
            data = res.json()
            # print(json.dumps(data, indent=2))
            
            # Check duration in response content
            content = data.get("content", {})
            duration = content.get("duration_weeks")
            weeks = content.get("roadmap", [])
            
            print(f"   ✅ API Response Received")
            print(f"   Requested Duration: 2")
            print(f"   Received Duration: {duration}")
            print(f"   Weeks Generated: {len(weeks)}")
            
            if len(weeks) == 2:
                print("   ✅ SUCCESS: Exactly 2 weeks generated.")
                print(f"   Week 1 Focus: {weeks[0].get('focus')}")
                print(f"   Week 2 Focus: {weeks[1].get('focus')}")
            else:
                print(f"   ❌ FAILURE: Expected 2 weeks, got {len(weeks)}")
                print("   FULL RESPONSE debug:")
                print(json.dumps(data, indent=2))
                
        else:
            print(f"❌ Failed: {res.status_code} - {res.text}")
            
    except Exception as e:
        print(f"❌ Error during roadmap creation: {e}")

if __name__ == "__main__":
    verify_duration_roadmap()
