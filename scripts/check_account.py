import requests

# Check account status
url = "https://api.apollo.io/v1/auth/health"
headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "5uiGUTUamjs0z8vMhFSqdw"
}

print("Checking Apollo API account status...")
response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

# Also try to get account info
url2 = "https://api.apollo.io/v1/auth/account"
response2 = requests.get(url2, headers=headers)

print(f"\nAccount Info Status: {response2.status_code}")
print(f"Account Info: {response2.text}")

