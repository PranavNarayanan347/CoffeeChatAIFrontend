"""Test email delivery service"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.email_service import send_password_reset_email, send_welcome_email, is_email_configured

def test_email_configuration():
    """Test if email is configured"""
    print("=" * 60)
    print("Email Configuration Test")
    print("=" * 60)
    
    if is_email_configured():
        print("[OK] Email service is configured")
        print(f"  SMTP Server: {os.environ.get('SMTP_SERVER', 'Not set')}")
        print(f"  SMTP Port: {os.environ.get('SMTP_PORT', 'Not set')}")
        print(f"  SMTP Username: {os.environ.get('SMTP_USERNAME', 'Not set')}")
        print(f"  Email From: {os.environ.get('EMAIL_FROM', 'Not set')}")
        print(f"  Frontend URL: {os.environ.get('FRONTEND_URL', 'Not set')}")
        return True
    else:
        print("[FAIL] Email service is NOT configured")
        print("\nPlease set the following environment variables:")
        print("  - SMTP_SERVER")
        print("  - SMTP_PORT")
        print("  - SMTP_USERNAME")
        print("  - SMTP_PASSWORD")
        print("  - EMAIL_FROM")
        print("  - FRONTEND_URL")
        return False

def test_password_reset_email():
    """Test password reset email"""
    print("\n" + "=" * 60)
    print("Testing Password Reset Email")
    print("=" * 60)
    
    test_email = input("Enter test email address: ").strip()
    if not test_email:
        print("[SKIP] No email provided")
        return False
    
    reset_token = "test_token_12345"
    result = send_password_reset_email(test_email, reset_token, "Test User")
    
    if result.get('success'):
        print(f"[OK] Password reset email sent successfully to {test_email}")
        print(f"  Check your inbox for the reset link")
        return True
    else:
        print(f"[FAIL] Failed to send email: {result.get('error')}")
        return False

def test_welcome_email():
    """Test welcome email"""
    print("\n" + "=" * 60)
    print("Testing Welcome Email")
    print("=" * 60)
    
    test_email = input("Enter test email address: ").strip()
    if not test_email:
        print("[SKIP] No email provided")
        return False
    
    result = send_welcome_email(test_email, "Test User")
    
    if result.get('success'):
        print(f"[OK] Welcome email sent successfully to {test_email}")
        return True
    else:
        print(f"[FAIL] Failed to send email: {result.get('error')}")
        return False

def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("Email Delivery Test Suite")
    print("=" * 60)
    
    # Check configuration
    if not test_email_configuration():
        print("\n[INFO] Please configure email settings before testing")
        return
    
    # Run tests
    print("\nSelect test to run:")
    print("1. Password Reset Email")
    print("2. Welcome Email")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    results = []
    
    if choice == '1':
        results.append(test_password_reset_email())
    elif choice == '2':
        results.append(test_welcome_email())
    elif choice == '3':
        results.append(test_password_reset_email())
        results.append(test_welcome_email())
    else:
        print("[SKIP] Invalid choice")
        return
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if all(results):
        print("[OK] All tests passed!")
    else:
        print("[FAIL] Some tests failed")
        print("\nTroubleshooting:")
        print("1. Check SMTP credentials are correct")
        print("2. Verify firewall allows SMTP connections")
        print("3. For Gmail, ensure 'Less secure app access' is enabled or use App Password")
        print("4. Check spam folder if email not received")

if __name__ == '__main__':
    main()



