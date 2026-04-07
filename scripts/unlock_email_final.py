import requests

# Try the correct Apollo email unlock endpoint
url = "https://api.apollo.io/v1/people/email_unlock"

headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "5uiGUTUamjs0z8vMhFSqdw"
}

# Test with Bill Gates' person ID
data = {
    "person_id": "6867cec58eea26000153fa61"
}

print("Attempting to unlock email using Apollo API...")
print(f"Person ID: {data['person_id']}")

response = requests.post(url, headers=headers, json=data)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Response Body: {response.text}")

# Also try to check account/credits if possible
print("\n" + "="*50)
print("Checking account status...")

account_url = "https://api.apollo.io/v1/auth/account"
account_response = requests.get(account_url, headers=headers)

print(f"Account Status: {account_response.status_code}")
print(f"Account Response: {account_response.text}")





