#!/usr/bin/env python3
"""
Test script to verify OpenAI and PDL API keys are working
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_people_search import PDL_API_KEY, OPENAI_API_KEY, client
import requests
import json

def test_openai_key():
    """Test OpenAI API key"""
    print("=" * 60)
    print("Testing OpenAI API Key...")
    print("=" * 60)
    
    try:
        # Simple test request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'API key is working' if you can read this."}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        print(f"[OK] OpenAI API Key: WORKING")
        print(f"   Response: {result}")
        print(f"   Key (first 20 chars): {OPENAI_API_KEY[:20]}...")
        return True
        
    except Exception as e:
        print(f"[FAIL] OpenAI API Key: FAILED")
        print(f"   Error: {str(e)}")
        return False

def test_pdl_key():
    """Test People Data Labs API key"""
    print("\n" + "=" * 60)
    print("Testing People Data Labs (PDL) API Key...")
    print("=" * 60)
    
    try:
        # Simple test query - search for a common job title
        url = "https://api.peopledatalabs.com/v5/person/search"
        headers = {"X-Api-Key": PDL_API_KEY}
        
        # Test query - search for software engineers
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"job_title": "software engineer"}}
                    ]
                }
            }
        }
        
        params = {
            "query": json.dumps(query),
            "size": 1,  # Just get 1 result for testing
            "pretty": True
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                print(f"[OK] PDL API Key: WORKING")
                print(f"   Found {len(data['data'])} test result(s)")
                print(f"   Key (first 20 chars): {PDL_API_KEY[:20]}...")
                return True
            else:
                print(f"[WARN] PDL API Key: WORKING (but no results found)")
                print(f"   This might be normal - API key is valid but query returned no results")
                return True
        elif response.status_code == 401:
            print(f"[FAIL] PDL API Key: INVALID (401 Unauthorized)")
            print(f"   The API key is not valid or has been revoked")
            return False
        elif response.status_code == 403:
            print(f"[FAIL] PDL API Key: FORBIDDEN (403)")
            print(f"   The API key doesn't have permission for this endpoint")
            return False
        else:
            print(f"[FAIL] PDL API Key: ERROR")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"[FAIL] PDL API Key: TIMEOUT")
        print(f"   Request timed out - check your internet connection")
        return False
    except Exception as e:
        print(f"[FAIL] PDL API Key: FAILED")
        print(f"   Error: {str(e)}")
        return False

def main():
    print("\n" + "=" * 60)
    print("API Key Verification Test")
    print("=" * 60)
    print("\nThis script will test both API keys to verify they're working.\n")
    
    openai_ok = test_openai_key()
    pdl_ok = test_pdl_key()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"OpenAI API Key: {'[OK] WORKING' if openai_ok else '[FAIL] NOT WORKING'}")
    print(f"PDL API Key:    {'[OK] WORKING' if pdl_ok else '[FAIL] NOT WORKING'}")
    
    if openai_ok and pdl_ok:
        print("\n[SUCCESS] Both API keys are working correctly!")
        return 0
    else:
        print("\n[WARNING] One or more API keys are not working.")
        print("   Please check the errors above and update the keys if needed.")
        return 1

if __name__ == "__main__":
    exit(main())

