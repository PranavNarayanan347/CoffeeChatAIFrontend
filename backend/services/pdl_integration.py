import requests
import json

# People Data Labs API configuration
base_url = "https://api.peopledatalabs.com/v5"
headers = {
    "X-Api-Key": "YOUR_PDL_API_KEY_HERE"  # Replace with your actual PDL API key
}

def search_people_pdl():
    """Search for people using People Data Labs API"""
    url = f"{base_url}/person/search"
    
    # Search for software engineers at Google
    params = {
        "job_title": "Software Engineer",
        "company": "Google",
        "size": 5,  # Number of results
        "pretty": True  # Pretty print JSON
    }
    
    print("Searching for Software Engineers at Google using People Data Labs...")
    print(f"URL: {url}")
    print(f"Params: {params}")
    
    response = requests.get(url, headers=headers, params=params)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.text}")
        return None

def enrich_person_by_email(email):
    """Enrich person data by email using PDL"""
    url = f"{base_url}/person/enrich"
    
    params = {
        "email": email,
        "pretty": True
    }
    
    print(f"Enriching person data for email: {email}")
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Enrichment failed: {response.status_code} - {response.text}")
        return None

def display_results(data):
    """Display search results in clean format"""
    if not data or 'data' not in data:
        print("No data found")
        return
    
    people = data['data']
    print(f"\nFound {len(people)} people:")
    print("-" * 60)
    
    for i, person in enumerate(people, 1):
        name = person.get('full_name', 'N/A')
        email = person.get('email', 'N/A')
        title = person.get('job_title', 'N/A')
        company = person.get('company', 'N/A')
        
        print(f"{i}. Name: {name}")
        print(f"   Email: {email}")
        print(f"   Title: {title}")
        print(f"   Company: {company}")
        print("-" * 60)

# Main execution
print("=" * 70)
print("PEOPLE DATA LABS API INTEGRATION")
print("=" * 70)

# Check if API key is set
if headers["X-Api-Key"] == "YOUR_PDL_API_KEY_HERE":
    print("WARNING: Please replace 'YOUR_PDL_API_KEY_HERE' with your actual PDL API key")
    print("   Get your API key from: https://www.peopledatalabs.com/dashboard")
    print("\nContinuing with demo (will show API structure)...")

# Search for people
results = search_people_pdl()

if results:
    display_results(results)
    
    # If we found people with emails, try enrichment
    if 'data' in results:
        for person in results['data']:
            email = person.get('email')
            if email and email != 'N/A':
                print(f"\nTrying enrichment for: {email}")
                enriched = enrich_person_by_email(email)
                if enriched:
                    print("Enrichment successful!")
                    # You can add more detailed processing here
                break  # Just test with first email
else:
    print("No results found or API error occurred")

print("\n" + "=" * 70)
print("INTEGRATION COMPLETE")
print("=" * 70)
print("\nNext steps:")
print("1. Get your PDL API key from: https://www.peopledatalabs.com/dashboard")
print("2. Replace 'YOUR_PDL_API_KEY_HERE' with your actual API key")
print("3. Run the script again to get real data")
