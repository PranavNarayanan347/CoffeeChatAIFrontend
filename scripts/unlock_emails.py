import requests

# Apollo API configuration
url = "https://api.apollo.io/v1/people/email_unlock"
headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "5uiGUTUamjs0z8vMhFSqdw"
}

# Test with first person (Bill Gates)
person_id = "6867cec58eea26000153fa61"

data = {
    "person_id": person_id
}

print("Attempting to unlock email for Bill Gates...")
print(f"Person ID: {person_id}")

response = requests.post(url, headers=headers, json=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    result = response.json()
    print(f"Unlocked Email: {result.get('email', 'N/A')}")
else:
    print(f"Error: {response.status_code} - {response.text}")

