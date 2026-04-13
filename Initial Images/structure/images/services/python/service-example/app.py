import requests

print("App started successfully")

try:
    response = requests.get("https://devops-db.com/", timeout=2)
    print(f"Request status: {response.status_code}")
except Exception as e:
    print(f"Request failed: {e}")