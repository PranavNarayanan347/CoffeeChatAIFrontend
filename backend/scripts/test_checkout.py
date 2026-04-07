"""
Test script to verify checkout session creation
This simulates what happens when a user clicks "Start Free Trial"
"""

import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import stripe
from services.stripe_service import create_checkout_session, is_stripe_configured

def test_checkout_session():
    """Test creating a checkout session"""
    print("=" * 60)
    print("Checkout Session Test")
    print("=" * 60)
    print()
    
    if not is_stripe_configured():
        print("[ERROR] Stripe is not configured!")
        return False
    
    price_id = os.environ.get('STRIPE_PRICE_ID')
    if not price_id:
        print("[ERROR] STRIPE_PRICE_ID not set!")
        return False
    
    # Create a test customer
    print("Creating test customer...")
    try:
        test_customer = stripe.Customer.create(
            email="test@example.com",
            name="Test User"
        )
        print(f"[SUCCESS] Created test customer: {test_customer.id}")
        print()
    except Exception as e:
        print(f"[ERROR] Failed to create customer: {str(e)}")
        return False
    
    # Test checkout session creation
    print("Creating checkout session...")
    try:
        result = create_checkout_session(
            customer_id=test_customer.id,
            price_id=price_id,
            success_url="http://localhost:5173/?subscription=success",
            cancel_url="http://localhost:5173/?subscription=canceled",
            trial_period_days=7
        )
        
        if result.get('success'):
            checkout_session = result['checkout_session']
            print("[SUCCESS] Checkout session created!")
            print(f"  Session ID: {checkout_session['id']}")
            print(f"  Checkout URL: {checkout_session['url']}")
            print()
            print("You can test the checkout by visiting:")
            print(f"  {checkout_session['url']}")
            print()
            print("Use test card: 4242 4242 4242 4242")
            print("Any future expiry date, any CVC, any ZIP")
            return True
        else:
            print(f"[ERROR] Failed to create checkout session: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception: {str(e)}")
        return False
    finally:
        # Clean up test customer
        try:
            stripe.Customer.delete(test_customer.id)
            print("Cleaned up test customer")
        except:
            pass

if __name__ == '__main__':
    success = test_checkout_session()
    sys.exit(0 if success else 1)



