import requests
import json
import openai

class AIPeopleSearch:
    def __init__(self, pdl_api_key, openai_api_key=None):
        self.pdl_api_key = pdl_api_key
        self.openai_api_key = openai_api_key
        
        if openai_api_key:
            openai.api_key = openai_api_key
    
    def parse_prompt(self, prompt):
        """Parse user prompt to extract search parameters"""
        if not self.openai_api_key:
            return self._fallback_parse(prompt)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "Extract job_title, company, and count from user requests. Return JSON only."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            return json.loads(response.choices[0].message.content)
        except:
            return self._fallback_parse(prompt)
    
    def _fallback_parse(self, prompt):
        """Simple regex-based parsing"""
        import re
        
        prompt_lower = prompt.lower()
        
        # Extract count
        count_match = re.search(r'(\d+)', prompt)
        count = int(count_match.group(1)) if count_match else 5
        
        # Extract job title
        job_titles = ['software engineer', 'data scientist', 'product manager', 'designer', 'developer']
        job_title = None
        for title in job_titles:
            if title in prompt_lower:
                job_title = title.title()
                break
        
        # Extract company - handle variations and case-insensitive matching
        company_mappings = {
            'google': 'google',
            'microsoft': 'microsoft', 
            'apple': 'apple',
            'amazon': 'amazon',
            'meta': 'meta',
            'facebook': 'facebook',
            'netflix': 'netflix',
            'morgan stanley': 'morgan stanley',
            'goldman sachs': 'goldman sachs',
            'jpmorgan': 'jp morgan',  # Map JPMorgan variations to correct PDL format
            'jp morgan': 'jp morgan',
            'j.p. morgan': 'j.p. morgan',
            'bank of america': 'bank of america',
            'wells fargo': 'wells fargo',
            'citigroup': 'citigroup',
            'uber': 'uber',
            'airbnb': 'airbnb',
            'tesla': 'tesla',
            'spacex': 'spacex',
            'salesforce': 'salesforce',
            'oracle': 'oracle',
            'ibm': 'ibm',
            'intel': 'intel',
            'nvidia': 'nvidia',
            'amd': 'amd',
            'adobe': 'adobe',
            'paypal': 'paypal',
            'stripe': 'stripe',
            'square': 'square',
            'twitter': 'twitter',
            'linkedin': 'linkedin',
            'snapchat': 'snapchat',
            'tiktok': 'tiktok',
            'zoom': 'zoom',
            'slack': 'slack',
            'dropbox': 'dropbox',
            'spotify': 'spotify',
            'disney': 'disney',
            'warner': 'warner',
            'sony': 'sony',
            'nintendo': 'nintendo',
            'ea': 'ea',
            'activision': 'activision',
            'blizzard': 'blizzard',
            'riot games': 'riot games',
            'valve': 'valve',
            'steam': 'steam',
            'epic games': 'epic games',
            'unity': 'unity',
            'autodesk': 'autodesk',
            'atlassian': 'atlassian',
            'servicenow': 'servicenow',
            'workday': 'workday',
            'snowflake': 'snowflake',
            'databricks': 'databricks',
            'palantir': 'palantir',
            'crowdstrike': 'crowdstrike',
            'okta': 'okta',
            'zendesk': 'zendesk',
            'hubspot': 'hubspot',
            'mailchimp': 'mailchimp',
            'shopify': 'shopify',
            'squarespace': 'squarespace',
            'wix': 'wix',
            'wordpress': 'wordpress',
            'github': 'github',
            'gitlab': 'gitlab',
            'bitbucket': 'bitbucket',
            'docker': 'docker',
            'kubernetes': 'kubernetes',
            'redhat': 'redhat',
            'canonical': 'canonical',
            'ubuntu': 'ubuntu',
            'debian': 'debian',
            'centos': 'centos',
            'fedora': 'fedora',
            'arch': 'arch',
            'gentoo': 'gentoo',
            'opensuse': 'opensuse',
            'freebsd': 'freebsd',
            'openbsd': 'openbsd',
            'netbsd': 'netbsd',
            'dragonfly': 'dragonfly',
            'minix': 'minix',
            'plan9': 'plan9',
            'inferno': 'inferno',
            'qnx': 'qnx',
            'vxworks': 'vxworks',
            'rtems': 'rtems',
            'freertos': 'freertos',
            'contiki': 'contiki',
            'tinyos': 'tinyos',
            'riot': 'riot',
            'zephyr': 'zephyr',
            'mbed': 'mbed',
            'arduino': 'arduino',
            'raspberry': 'raspberry',
            'beaglebone': 'beaglebone',
            'odroid': 'odroid',
            'banana': 'banana',
            'orange': 'orange',
            'pine': 'pine',
            'rock': 'rock',
            'firefly': 'firefly',
            'hardkernel': 'hardkernel',
            'friendlyarm': 'friendlyarm',
            'olimex': 'olimex',
            'libre': 'libre',
            'pcduino': 'pcduino',
            'cubieboard': 'cubieboard',
            'marsboard': 'marsboard',
            'wandboard': 'wandboard',
            'hummingboard': 'hummingboard',
            'udoo': 'udoo',
            'minnowboard': 'minnowboard',
            'galileo': 'galileo',
            'edison': 'edison',
            'joule': 'joule',
            'up': 'up',
            'up2': 'up2',
            'up3': 'up3',
            'up4': 'up4',
            'up5': 'up5',
            'up6': 'up6',
            'up7': 'up7',
            'up8': 'up8',
            'up9': 'up9',
            'up10': 'up10',
            'up11': 'up11',
            'up12': 'up12',
            'up13': 'up13',
            'up14': 'up14',
            'up15': 'up15',
            'up16': 'up16',
            'up17': 'up17',
            'up18': 'up18',
            'up19': 'up19',
            'up20': 'up20'
        }
        
        company = None
        for search_term, pdl_name in company_mappings.items():
            if search_term in prompt_lower:
                company = pdl_name
                break
        
        return {
            "job_title": job_title,
            "company": company,
            "count": count
        }
    
    def search_people(self, job_title=None, company=None, count=5):
        """Search for people using PDL API"""
        query_conditions = []
        
        if job_title:
            query_conditions.append({"term": {"job_title": job_title.lower()}})
        
        if company:
            query_conditions.append({"term": {"job_company_name": company.lower()}})
        
        if not query_conditions:
            query_conditions.append({"term": {"job_title": "software engineer"}})
        
        query = {
            "query": {
                "bool": {
                    "must": query_conditions
                }
            }
        }
        
        url = "https://api.peopledatalabs.com/v5/person/search"
        headers = {"X-Api-Key": self.pdl_api_key}
        params = {
            "query": json.dumps(query),
            "size": count,
            "pretty": True
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return self._format_results(response.json())
            else:
                return {"error": f"API Error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def _format_results(self, data):
        """Format PDL results"""
        if 'data' not in data or not data['data']:
            return {"message": "No people found"}
        
        results = []
        
        for person in data['data']:
            # Extract education
            education = []
            if 'education' in person and person['education']:
                for edu in person['education']:
                    school_info = edu.get('school') or {}
                    education.append({
                        "school_name": school_info.get('name', 'N/A'),
                        "school_type": school_info.get('type', 'N/A'),
                        "degrees": edu.get('degrees', []),
                        "majors": edu.get('majors', []),
                        "start_date": edu.get('start_date', 'N/A'),
                        "end_date": edu.get('end_date', 'N/A'),
                        "gpa": edu.get('gpa', 'N/A')
                    })
            
            # Create person record
            results.append({
                "name": person.get('full_name', 'N/A'),
                "title": person.get('job_title', 'N/A'),
                "company": person.get('job_company_name', 'N/A'),
                "work_email": person.get('work_email', 'N/A'),
                "personal_email": person.get('personal_emails', 'N/A'),
                "linkedin": person.get('linkedin_url', 'N/A'),
                "education": education
            })
        
        return results
    
    def process_request(self, user_prompt):
        """Process user request and return results"""
        # Parse the prompt
        params = self.parse_prompt(user_prompt)
        
        # Search for people
        results = self.search_people(
            job_title=params.get('job_title'),
            company=params.get('company'),
            count=params.get('count', 5)
        )
        
        return results

# Example usage
if __name__ == "__main__":
    import os

    pdl = os.environ.get("PDL_API_KEY", "")
    oai = os.environ.get("OPENAI_API_KEY", "")
    if not pdl or not oai:
        raise SystemExit("Set PDL_API_KEY and OPENAI_API_KEY in the environment before running this module.")

    searcher = AIPeopleSearch(pdl_api_key=pdl, openai_api_key=oai)
    
    # Test with different prompts
    test_prompts = [
        "Find me 5 Google software engineers",
        "I need 3 data scientists at Microsoft",
        "Show me software engineers",
        "Find 10 product managers at Apple"
    ]
    
    for prompt in test_prompts:
        print(f"\nPrompt: '{prompt}'")
        print("=" * 50)
        results = searcher.process_request(prompt)
        print(json.dumps(results, indent=2))
        print("=" * 50)
