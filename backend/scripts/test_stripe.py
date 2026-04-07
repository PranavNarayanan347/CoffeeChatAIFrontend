"""
Test script to verify Stripe configuration
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import stripe
from services.stripe_service import is_stripe_configured, create_checkout_session, get_subscription_status

def test_stripe_config():
    """Test Stripe configuration"""
    print("=" * 60)
    print("Stripe Configuration Test")
    print("=" * 60)
    print()
    
    # Check environment variables
    secret_key = os.environ.get('STRIPE_SECRET_KEY') or os.environ.get('STRIPE_SECRET_KEY_TEST')
    price_id = os.environ.get('STRIPE_PRICE_ID')
    
    print("Environment Variables:")
    print(f"  STRIPE_SECRET_KEY_TEST: {'Set' if secret_key else 'NOT SET'}")
    if secret_key:
        print(f"    Value: {secret_key[:20]}...{secret_key[-10:]}")
    print(f"  STRIPE_PRICE_ID: {'Set' if price_id else 'NOT SET'}")
    if price_id:
        print(f"    Value: {price_id}")
    print()
    
    # Test Stripe configuration
    if not is_stripe_configured():
        print("[ERROR] Stripe is not configured!")
        print("Please set STRIPE_SECRET_KEY or STRIPE_SECRET_KEY_TEST")
        return False
    
    print("[SUCCESS] Stripe API key is configured")
    print()
    
    # Test Stripe API connection
    try:
        stripe.api_key = secret_key
        account = stripe.Account.retrieve()
        print(f"[SUCCESS] Connected to Stripe account: {account.id}")
        print(f"  Account type: {account.type}")
        print(f"  Country: {account.country}")
        print()
    except Exception as e:
        print(f"[ERROR] Failed to connect to Stripe: {str(e)}")
        return False
    
    # Test Price ID
    if not price_id:
        print("[WARNING] STRIPE_PRICE_ID not set!")
        print("Subscription checkout will not work without a Price ID")
        return False
    
    try:
        price = stripe.Price.retrieve(price_id)
        print(f"[SUCCESS] Price ID is valid!")
        print(f"  Price ID: {price.id}")
        print(f"  Amount: ${price.unit_amount / 100} {price.currency.upper()}")
        print(f"  Interval: {price.recurring.interval if price.recurring else 'one-time'}")
        print(f"  Active: {price.active}")
        print()
    except stripe.error.InvalidRequestError as e:
        print(f"[ERROR] Invalid Price ID: {str(e)}")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to retrieve price: {str(e)}")
        return False
    
    print("=" * 60)
    print("[SUCCESS] All Stripe configuration tests passed!")
    print("=" * 60)
    print()
    print("You can now:")
    print("  1. Start your backend server")
    print("  2. Test the checkout flow on the frontend")
    print("  3. Use test card: 4242 4242 4242 4242")
    print()
    
    return True

if __name__ == '__main__':
    success = test_stripe_config()
    sys.exit(0 if success else 1)



