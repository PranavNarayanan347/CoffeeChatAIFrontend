import requests

# Try to get person details by ID
person_id = "6867cec58eea26000153fa61"  # Bill Gates
url = f"https://api.apollo.io/v1/people/{person_id}"

headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "5uiGUTUamjs0z8vMhFSqdw"
}

print(f"Getting person details for ID: {person_id}")
response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    data = response.json()
    person = data.get('person', {})
    print(f"\nName: {person.get('name', 'N/A')}")
    print(f"Email: {person.get('email', 'N/A')}")
    print(f"Title: {person.get('title', 'N/A')}")
    print(f"Organization: {person.get('organization', {}).get('name', 'N/A')}")

