import urllib.request
import json

url = "http://127.0.0.1:8000/register"
payload = {
    "email": "test_urllib_client@test.com",
    "password": "mysecretpassword",
    "full_name": "Python Client"
}
data = json.dumps(payload).encode('utf-8')
headers = {"Content-Type": "application/json"}

req = urllib.request.Request(url, data=data, headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.status}")
        print(f"Response: {response.read().decode()}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(f"Response: {e.read().decode()}")
except Exception as e:
    print(f"Request Error: {e}")
