import requests
import json
import openai
import re
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration (set PDL_API_KEY and OPENAI_API_KEY in the environment)
PDL_API_KEY = os.environ.get("PDL_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Gmail API Configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# Initialize OpenAI client (uses OPENAI_API_KEY from the environment)
client = openai.OpenAI(api_key=OPENAI_API_KEY or None)

def authenticate_gmail():
    """Authenticate with Gmail API"""
    creds = None
    
    # Check if token file exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"❌ Gmail credentials file '{CREDENTIALS_FILE}' not found!")
                print("Please download your Gmail API credentials from Google Cloud Console:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project or select existing one")
                print("3. Enable Gmail API")
                print("4. Create OAuth 2.0 credentials")
                print("5. Download as 'credentials.json' and place in this directory")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def create_gmail_draft(to_email, subject, body, from_email=None):
    """Create a Gmail draft"""
    try:
        creds = authenticate_gmail()
        if not creds:
            return {"error": "Gmail authentication failed"}
        
        service = build('gmail', 'v1', credentials=creds)
        
        # Create email message
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject
        if from_email:
            message['from'] = from_email
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        # Create draft
        draft_body = {
            'message': {
                'raw': raw_message
            }
        }
        
        draft = service.users().drafts().create(userId='me', body=draft_body).execute()
        
        return {
            "success": True,
            "draft_id": draft['id'],
            "message": f"Draft created successfully! Draft ID: {draft['id']}"
        }
        
    except HttpError as error:
        return {"error": f"Gmail API error: {error}"}
    except Exception as e:
        return {"error": f"Error creating draft: {str(e)}"}

def parse_user_prompt(prompt):
    """Parse user prompt to extract search parameters using OpenAI"""
    
    system_prompt = """
    You are a helpful assistant that parses user requests for finding people. 
    Extract the following information from the user's request:
    - job_title: The job title they're looking for (e.g., "Software Engineer", "Data Scientist")
    - company: The company name (e.g., "Google", "Microsoft", "Apple")
    - count: Number of people to find (default to 5 if not specified)
    - location: Any location mentioned (optional)
    
    Return ONLY a JSON object with these fields. If a field is not mentioned, use null.
    
    Examples:
    "Find me 5 Google software engineers" -> {"job_title": "Software Engineer", "company": "Google", "count": 5, "location": null}
    "I need 3 data scientists at Microsoft" -> {"job_title": "Data Scientist", "company": "Microsoft", "count": 3, "location": null}
    "Show me software engineers" -> {"job_title": "Software Engineer", "company": null, "count": 5, "location": null}
    "Find me 5 investment banking analysts at Morgan Stanley in New York City" -> {"job_title": "Investment Banking Analyst", "company": "Morgan Stanley", "count": 5, "location": New York City}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        parsed_data = json.loads(response.choices[0].message.content)
        return parsed_data
        
    except Exception as e:
        print(f"Error parsing prompt: {e}")
        # Fallback parsing using regex
        return fallback_parse(prompt)

def fallback_parse(prompt):
    """Fallback parsing using regex if OpenAI fails"""
    prompt_lower = prompt.lower()
    
    # Extract count
    count_match = re.search(r'(\d+)', prompt)
    count = int(count_match.group(1)) if count_match else 5
    
    # Extract job title
    job_titles = ['software engineer', 'data scientist', 'product manager', 'designer', 'developer', 'engineer']
    job_title = None
    for title in job_titles:
        if title in prompt_lower:
            job_title = title.title()
            break
    
    # Extract company
    companies = ['google', 'microsoft', 'apple', 'amazon', 'meta', 'facebook', 'netflix', 'uber', 'airbnb']
    company = None
    for comp in companies:
        if comp in prompt_lower:
            company = comp
            break
    
    return {
        "job_title": job_title,
        "company": company,
        "count": count,
        "location": None
    }

def search_people_pdl(job_title, company, count=5):
    """Search for people using People Data Labs API"""
    
    # Build Elasticsearch query
    query_conditions = []
    
    if job_title:
        # Use match_phrase for better partial matching
        query_conditions.append({"match_phrase": {"job_title": job_title}})
    
    if company:
        # Use match_phrase for better partial matching
        query_conditions.append({"match_phrase": {"job_company_name": company}})
    
    if not query_conditions:
        # If no specific criteria, search for any software engineers
        query_conditions.append({"match_phrase": {"job_title": "software engineer"}})
    
    query = {
        "query": {
            "bool": {
                "must": query_conditions
            }
        }
    }
    
    url = "https://api.peopledatalabs.com/v5/person/search"
    headers = {"X-Api-Key": PDL_API_KEY}
    params = {
        "query": json.dumps(query),
        "size": count,
        "pretty": True
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

def format_results(data):
    """Format PDL results into clean JSON"""
    if 'error' in data:
        return data
    
    if 'data' not in data or not data['data']:
        return {"message": "No people found matching your criteria"}
    
    results = []
    
    for person in data['data']:
        # Extract education information
        education = []
        if 'education' in person and person['education']:
            for edu in person['education']:
                school_info = {
                    "school_name": edu.get('school', {}).get('name', 'N/A'),
                    "school_type": edu.get('school', {}).get('type', 'N/A'),
                    "degrees": edu.get('degrees', []),
                    "majors": edu.get('majors', []),
                    "start_date": edu.get('start_date', 'N/A'),
                    "end_date": edu.get('end_date', 'N/A'),
                    "gpa": edu.get('gpa', 'N/A')
                }
                education.append(school_info)
        
        # Extract personal email (handle list format)
        personal_emails = person.get('personal_emails', [])
        if isinstance(personal_emails, list) and len(personal_emails) > 0:
            personal_email = personal_emails[0]  # Get first email
        elif isinstance(personal_emails, str):
            personal_email = personal_emails
        else:
            personal_email = 'N/A'
        
        # Create person record
        person_record = {
            "name": person.get('full_name', 'N/A'),
            "title": person.get('job_title', 'N/A'),
            "company": person.get('job_company_name', 'N/A'),
            "work_email": person.get('work_email', 'N/A'),
            "personal_email": personal_email,
            "linkedin": person.get('linkedin_url', 'N/A'),
            "education": education
        }
        
        results.append(person_record)
    
    return results

def generate_email(person_info, email_type="cold_outreach", custom_message=""):
    """Generate personalized email for a person using OpenAI"""
    
    system_prompt = f"""
    You are a professional email writer specializing in {email_type} emails. 
    Generate a personalized, professional email based on the person's information.
    
    Guidelines:
    - Keep it concise (2-3 paragraphs max)
    - Be professional but friendly
    - Reference specific details from their profile
    - Include a clear call-to-action
    - Avoid being overly salesy or pushy
    
    Email types:
    - cold_outreach: Initial contact for networking or collaboration
    - job_inquiry: Asking about job opportunities
    - collaboration: Proposing a business partnership
    - informational_interview: Requesting career advice
    """
    
    user_prompt = f"""
    Generate a {email_type} email for:
    Name: {person_info.get('name', 'N/A')}
    Title: {person_info.get('title', 'N/A')}
    Company: {person_info.get('company', 'N/A')}
    Education: {person_info.get('education', [])}
    
    Custom message/context: {custom_message if custom_message else 'No specific context provided'}
    
    Return ONLY the email content, no subject line or additional formatting.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Error generating email: {e}"

def update_email_content(original_email, person_info, update_instructions, email_type="cold_outreach"):
    """Update an existing email based on user instructions"""
    
    system_prompt = f"""
    You are a professional email editor. You will be given an original email and specific instructions for how to modify it.
    
    Guidelines:
    - Keep the professional tone and structure
    - Incorporate the requested changes naturally
    - Maintain the email's purpose and call-to-action
    - Keep it concise (2-3 paragraphs max)
    - Ensure the updated email flows well
    
    Email type: {email_type}
    Person: {person_info.get('name', 'N/A')} - {person_info.get('title', 'N/A')} at {person_info.get('company', 'N/A')}
    """
    
    user_prompt = f"""
    Original email:
    {original_email}
    
    Update instructions: {update_instructions}
    
    Please update the email according to the instructions while maintaining its professional quality and purpose.
    Return ONLY the updated email content, no subject line or additional formatting.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Error updating email: {e}"

def process_user_request(user_prompt):
    """Main function to process user request"""
    print(f"Processing request: '{user_prompt}'")
    
    # Parse the user prompt
    search_params = parse_user_prompt(user_prompt)
    print(f"Parsed parameters: {search_params}")
    
    # Search for people
    search_results = search_people_pdl(
        job_title=search_params.get('job_title'),
        company=search_params.get('company'),
        count=search_params.get('count', 5)
    )
    
    # Format and return results
    formatted_results = format_results(search_results)
    
    return formatted_results

# Interactive mode
def main():
    print("=" * 60)
    print("AI-Powered People Search & Email Generator")
    print("=" * 60)
    print("Search Examples:")
    print("- 'Find me 5 Google software engineers'")
    print("- 'I need 3 data scientists at Microsoft'")
    print("- 'Show me software engineers'")
    print("- 'Find 10 product managers at Apple'")
    print("\nAfter finding people, you can generate personalized emails!")
    print("Email types: Cold outreach, Job inquiry, Collaboration, Informational interview")
    print("\n📧 Gmail Integration: Create drafts directly in your Gmail!")
    print("   (Requires Gmail API setup - see instructions if needed)")
    print("=" * 60)
    
    if not OPENAI_API_KEY:
        print("⚠️  WARNING: Please set your OpenAI API key!")
        print("   Get your API key from: https://platform.openai.com/api-keys")
        print("\nContinuing with fallback parsing...")
    
    while True:
        try:
            user_input = input("\nEnter your search request (or 'quit' to exit): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process the request
            results = process_user_request(user_input)
            
            # Display results
            print("\n" + "=" * 60)
            print("RESULTS:")
            print("=" * 60)
            print(json.dumps(results, indent=2))
            
            # Check if we have valid results for email generation
            if isinstance(results, list) and len(results) > 0:
                print("\n" + "=" * 60)
                print("EMAIL GENERATION:")
                print("=" * 60)
                
                while True:
                    try:
                        email_choice = input("\nWould you like to generate an email for someone? (y/n): ").strip().lower()
                        
                        if email_choice in ['n', 'no']:
                            break
                        elif email_choice in ['y', 'yes']:
                            # Show numbered list of people
                            print("\nSelect a person to generate an email for:")
                            for i, person in enumerate(results, 1):
                                print(f"{i}. {person.get('name', 'N/A')} - {person.get('title', 'N/A')} at {person.get('company', 'N/A')}")
                            
                            try:
                                person_choice = int(input("\nEnter the number (1-{}): ".format(len(results))))
                                if 1 <= person_choice <= len(results):
                                    selected_person = results[person_choice - 1]
                                    
                                    # Email type selection
                                    print("\nEmail types:")
                                    print("1. Cold outreach (networking)")
                                    print("2. Job inquiry")
                                    print("3. Collaboration proposal")
                                    print("4. Informational interview")
                                    
                                    email_type_choice = input("Select email type (1-4): ").strip()
                                    email_types = {
                                        "1": "cold_outreach",
                                        "2": "job_inquiry", 
                                        "3": "collaboration",
                                        "4": "informational_interview"
                                    }
                                    
                                    email_type = email_types.get(email_type_choice, "cold_outreach")
                                    
                                    # Optional custom message
                                    custom_message = input("\nAny specific context or message to include? (press Enter to skip): ").strip()
                                    
                                    # Generate email
                                    print("\nGenerating email...")
                                    email_content = generate_email(selected_person, email_type, custom_message)
                                    
                                    print("\n" + "=" * 60)
                                    print("GENERATED EMAIL:")
                                    print("=" * 60)
                                    recipient_email = selected_person.get('work_email', selected_person.get('personal_email', 'N/A'))
                                    subject_line = email_type.replace('_', ' ').title()
                                    print(f"To: {recipient_email}")
                                    print(f"Subject: {subject_line}")
                                    print("-" * 40)
                                    print(email_content)
                                    print("=" * 60)
                                    
                                    # Ask if user wants to create Gmail draft
                                    if recipient_email != 'N/A':
                                        draft_choice = input("\nWould you like to create this as a Gmail draft? (y/n): ").strip().lower()
                                        
                                        if draft_choice in ['y', 'yes']:
                                            print("\nCreating Gmail draft...")
                                            draft_result = create_gmail_draft(
                                                to_email=recipient_email,
                                                subject=subject_line,
                                                body=email_content
                                            )
                                            
                                            if draft_result.get('success'):
                                                print(f"✅ {draft_result['message']}")
                                                print("📧 Check your Gmail drafts folder!")
                                            else:
                                                print(f"❌ {draft_result.get('error', 'Unknown error')}")
                                    else:
                                        print("\n⚠️  No valid email address found for this person.")
                                    
                                else:
                                    print("Invalid selection. Please try again.")
                            except ValueError:
                                print("Please enter a valid number.")
                        else:
                            print("Please enter 'y' for yes or 'n' for no.")
                            
                    except KeyboardInterrupt:
                        print("\nReturning to main menu...")
                        break
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
