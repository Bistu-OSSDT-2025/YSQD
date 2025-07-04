import requests
import json

login_url = "http://localhost:5000/api/users/login"
login_data = {
    "email": "test@example.com",
    "password": "testpass"
}

response = requests.post(login_url, json=login_data)
print("Login Response:")
print(f"Status Code: {response.status_code}")
print("Response Body:")
print(json.dumps(response.json(), indent=2))
