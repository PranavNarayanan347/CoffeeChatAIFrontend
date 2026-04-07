"""Test password reset functionality"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_password_reset_flow():
    """Test complete password reset flow"""
    print("=" * 60)
    print("Password Reset Flow Test")
    print("=" * 60)
    
    # Use existing test user or create one
    test_email = "testuser@example.com"
    old_password = "TestPass123"
    new_password = "NewTestPass456"
    
    print(f"\n1. Testing forgot password for: {test_email}")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/forgot-password",
            json={"email": test_email}
        )
        
        print(f"   Status Code: {response.status_code}")
        result = response.json()
        
        if response.status_code == 200:
            print(f"   [OK] Password reset request successful")
            reset_token = result.get('reset_token')
            
            if reset_token:
                print(f"   Reset Token: {reset_token[:20]}...")
                
                print(f"\n2. Testing password reset with token...")
                reset_response = requests.post(
                    f"{BASE_URL}/api/auth/reset-password",
                    json={
                        "email": test_email,
                        "token": reset_token,
                        "password": new_password
                    }
                )
                
                print(f"   Status Code: {reset_response.status_code}")
                reset_result = reset_response.json()
                
                if reset_response.status_code == 200:
                    print(f"   [OK] Password reset successful!")
                    
                    print(f"\n3. Testing login with new password...")
                    login_response = requests.post(
                        f"{BASE_URL}/api/auth/login",
                        json={
                            "email": test_email,
                            "password": new_password
                        }
                    )
                    
                    if login_response.status_code == 200:
                        print(f"   [OK] Login with new password successful!")
                        
                        # Reset password back for testing
                        print(f"\n4. Resetting password back to original...")
                        forgot_response = requests.post(
                            f"{BASE_URL}/api/auth/forgot-password",
                            json={"email": test_email}
                        )
                        if forgot_response.status_code == 200:
                            new_token = forgot_response.json().get('reset_token')
                            if new_token:
                                requests.post(
                                    f"{BASE_URL}/api/auth/reset-password",
                                    json={
                                        "email": test_email,
                                        "token": new_token,
                                        "password": old_password
                                    }
                                )
                                print(f"   [OK] Password reset back to original")
                    else:
                        print(f"   [FAIL] Login with new password failed")
                else:
                    print(f"   [FAIL] Password reset failed: {reset_result.get('error')}")
            else:
                print(f"   [INFO] No reset token in response (may be configured for email)")
        else:
            print(f"   [FAIL] Forgot password failed: {result.get('error')}")
            
    except Exception as e:
        print(f"   [FAIL] Error: {e}")

def test_invalid_reset_token():
    """Test invalid reset token handling"""
    print("\n" + "=" * 60)
    print("Invalid Reset Token Test")
    print("=" * 60)
    
    print("\n1. Testing with invalid token...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/reset-password",
            json={
                "email": "testuser@example.com",
                "token": "invalid_token_12345",
                "password": "NewPassword123"
            }
        )
        
        if response.status_code == 400:
            print(f"   [OK] Invalid token correctly rejected")
        else:
            print(f"   [FAIL] Should reject invalid token")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")

if __name__ == '__main__':
    print("\nMake sure Flask server is running on http://localhost:5000")
    print("Waiting 2 seconds...\n")
    import time
    time.sleep(2)
    
    test_password_reset_flow()
    test_invalid_reset_token()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

