import requests

# Apollo Email Verifier API
url = "https://api.apollo.io/v1/email_verifier"

headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "5uiGUTUamjs0z8vMhFSqdw"
}

# Test with Bill Gates' person ID
data = {
    "person_id": "6867cec58eea26000153fa61"
}

print("Attempting to verify and unlock email using Apollo Email Verifier...")
print(f"Person ID: {data['person_id']}")

response = requests.post(url, headers=headers, json=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    result = response.json()
    print(f"\nEmail Verification Result:")
    print(f"Email: {result.get('email', 'N/A')}")
    print(f"Status: {result.get('status', 'N/A')}")
    print(f"Verification: {result.get('verification', 'N/A')}")
else:
    print(f"Error: {response.status_code} - {response.text}")
    
    # Try alternative endpoint
    print("\nTrying alternative email verification endpoint...")
    alt_url = "https://api.apollo.io/v1/people/email_verification"
    alt_response = requests.post(alt_url, headers=headers, json=data)
    print(f"Alternative Status: {alt_response.status_code}")
    print(f"Alternative Response: {alt_response.text}")





