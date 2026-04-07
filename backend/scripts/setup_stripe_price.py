"""
Helper script to create or retrieve Stripe Price ID for subscription setup.

This script will:
1. Check if a price already exists for the product
2. Create a new $15/month recurring price if none exists
3. Display the Price ID to use in STRIPE_PRICE_ID environment variable
"""

import os
import sys
import stripe

# Add parent directory to path to import from backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY') or os.environ.get('STRIPE_SECRET_KEY_TEST')

if not stripe.api_key:
    print("ERROR: Stripe API key not found!")
    print("Please set STRIPE_SECRET_KEY or STRIPE_SECRET_KEY_TEST environment variable")
    print("\nExample:")
    print("  export STRIPE_SECRET_KEY_TEST=sk_test_...")
    sys.exit(1)

# Product ID from user
PRODUCT_ID = "prod_TbjNIPCwvMGBX6"  # Update this if needed

def find_or_create_price():
    """Find existing price or create a new one"""
    
    print(f"Looking for prices for product: {PRODUCT_ID}")
    print("-" * 60)
    
    try:
        # List all prices for this product
        prices = stripe.Price.list(product=PRODUCT_ID, active=True, limit=100)
        
        # Look for a monthly recurring price at $15
        monthly_price = None
        for price in prices.data:
            if price.recurring and price.recurring.interval == 'month':
                amount = price.unit_amount / 100  # Convert cents to dollars
                if amount == 15.00:
                    monthly_price = price
                    break
        
        if monthly_price:
            print("[SUCCESS] Found existing price!")
            print(f"   Price ID: {monthly_price.id}")
            print(f"   Amount: ${monthly_price.unit_amount / 100}/month")
            print(f"   Status: {'Active' if monthly_price.active else 'Inactive'}")
            return monthly_price.id
        
        # No matching price found, create one
        print("No matching $15/month price found. Creating new price...")
        
        new_price = stripe.Price.create(
            product=PRODUCT_ID,
            unit_amount=1500,  # $15.00 in cents
            currency='usd',
            recurring={
                'interval': 'month',
            },
            nickname='Monthly Subscription - $15',
        )
        
        print("[SUCCESS] Created new price!")
        print(f"   Price ID: {new_price.id}")
        print(f"   Amount: ${new_price.unit_amount / 100}/month")
        return new_price.id
        
    except stripe.error.InvalidRequestError as e:
        if 'No such product' in str(e):
            print(f"[ERROR] Product {PRODUCT_ID} not found!")
            print("Please verify the product ID is correct.")
            print("\nTrying to create product and price...")
            
            # Try to create product first, then price
            try:
                product = stripe.Product.create(
                    name="CoffeeChat AI Monthly Subscription",
                    description="Monthly subscription to CoffeeChat AI",
                )
                print(f"[SUCCESS] Created product: {product.id}")
                
                new_price = stripe.Price.create(
                    product=product.id,
                    unit_amount=1500,
                    currency='usd',
                    recurring={'interval': 'month'},
                    nickname='Monthly Subscription - $15',
                )
                print(f"[SUCCESS] Created price: {new_price.id}")
                return new_price.id
            except Exception as create_error:
                print(f"[ERROR] Failed to create product/price: {create_error}")
                sys.exit(1)
        else:
            print(f"[ERROR] {str(e)}")
            sys.exit(1)
    except stripe.error.StripeError as e:
        print(f"[ERROR] Stripe API Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    print("=" * 60)
    print("Stripe Price Setup Script")
    print("=" * 60)
    print()
    
    price_id = find_or_create_price()
    
    print()
    print("=" * 60)
    print("[SUCCESS] Setup Complete!")
    print("=" * 60)
    print()
    print("Add this to your environment variables:")
    print(f"  export STRIPE_PRICE_ID={price_id}")
    print()
    print("Or add to your .env file:")
    print(f"  STRIPE_PRICE_ID={price_id}")
    print()
    print("Also make sure you have:")
    print("  export STRIPE_SECRET_KEY_TEST=sk_test_...")
    print("  (or STRIPE_SECRET_KEY=sk_live_... for production)")
    print()

