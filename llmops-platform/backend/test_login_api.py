import requests
import json

# Test login API
url = "http://localhost:8000/auth/login"

data = {
    "email": "test@example.com",
    "password": "password123"
}

print("Testing login API...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print("-" * 60)

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n✅ LOGIN SUCCESSFUL!")
    else:
        print("\n❌ LOGIN FAILED!")
        
except Exception as e:
    print(f"❌ Error: {e}")
