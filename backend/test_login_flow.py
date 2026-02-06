import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    email = "testlogin@example.com"
    password = "password123"
    
    # 1. Register
    print(f"Registering {email}...")
    reg_data = {
        "email": email,
        "password": password,
        "full_name": "Test User"
    }
    
    # Check if user exists first or handle 400
    reg_res = requests.post(f"{BASE_URL}/register", json=reg_data)
    if reg_res.status_code == 200:
        print("Registration successful")
    elif reg_res.status_code == 400 and "already registered" in reg_res.text:
        print("User already registered, proceeding to login")
    else:
        print(f"Registration failed: {reg_res.status_code} {reg_res.text}")
        return

    # 2. Login
    print("Logging in...")
    login_data = {
        "username": email,
        "password": password
    }
    login_res = requests.post(f"{BASE_URL}/token", data=login_data)
    
    if login_res.status_code == 200:
        print("Login successful!")
        print(login_res.json())
    else:
        print(f"Login failed: {login_res.status_code} {login_res.text}")

if __name__ == "__main__":
    test_flow()
