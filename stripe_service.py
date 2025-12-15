"""Stripe service for customer and subscription management"""
import stripe
import os
from typing import Optional, Dict, Any

# Initialize Stripe API key
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY') or os.environ.get('STRIPE_SECRET_KEY_TEST')

def create_stripe_customer(email: str, name: Optional[str] = None, metadata: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Create a Stripe customer
    
    Args:
        email: Customer email address
        name: Customer name (optional)
        metadata: Additional metadata to attach to customer (optional)
    
    Returns:
        Dictionary containing customer data or error information
    
    Example:
        result = create_stripe_customer("user@example.com", "John Doe")
        if result.get('success'):
            customer_id = result['customer']['id']
    """
    try:
        if not stripe.api_key:
            return {
                'success': False,
                'error': 'Stripe API key not configured. Set STRIPE_SECRET_KEY environment variable.'
            }
        
        customer_data = {
            'email': email,
        }
        
        if name:
            customer_data['name'] = name
        
        if metadata:
            customer_data['metadata'] = metadata
        
        customer = stripe.Customer.create(**customer_data)
        
        return {
            'success': True,
            'customer': {
                'id': customer.id,
                'email': customer.email,
                'name': customer.name,
                'created': customer.created
            }
        }
    
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': f'Stripe API error: {str(e)}',
            'error_type': type(e).__name__
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

def get_stripe_customer(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve a Stripe customer by ID
    
    Args:
        customer_id: Stripe customer ID
    
    Returns:
        Dictionary containing customer data or error information
    """
    try:
        if not stripe.api_key:
            return {
                'success': False,
                'error': 'Stripe API key not configured'
            }
        
        customer = stripe.Customer.retrieve(customer_id)
        
        return {
            'success': True,
            'customer': {
                'id': customer.id,
                'email': customer.email,
                'name': customer.name,
                'created': customer.created
            }
        }
    
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': f'Stripe API error: {str(e)}',
            'error_type': type(e).__name__
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

def get_customer_subscription(customer_id: str) -> Dict[str, Any]:
    """
    Get active subscription for a customer
    
    Args:
        customer_id: Stripe customer ID
    
    Returns:
        Dictionary containing subscription data or None if no active subscription
    """
    try:
        if not stripe.api_key:
            return {
                'success': False,
                'error': 'Stripe API key not configured'
            }
        
        subscriptions = stripe.Subscription.list(
            customer=customer_id,
            status='active',
            limit=1
        )
        
        if subscriptions.data:
            subscription = subscriptions.data[0]
            return {
                'success': True,
                'subscription': {
                    'id': subscription.id,
                    'status': subscription.status,
                    'current_period_end': subscription.current_period_end,
                    'plan': subscription.items.data[0].price.id if subscription.items.data else None
                }
            }
        else:
            return {
                'success': True,
                'subscription': None,
                'message': 'No active subscription found'
            }
    
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': f'Stripe API error: {str(e)}',
            'error_type': type(e).__name__
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

def cancel_subscription(subscription_id: str) -> Dict[str, Any]:
    """
    Cancel a Stripe subscription
    
    Args:
        subscription_id: Stripe subscription ID
    
    Returns:
        Dictionary containing cancellation result
    """
    try:
        if not stripe.api_key:
            return {
                'success': False,
                'error': 'Stripe API key not configured'
            }
        
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
        )
        
        return {
            'success': True,
            'message': 'Subscription will be canceled at period end',
            'subscription': {
                'id': subscription.id,
                'status': subscription.status,
                'cancel_at_period_end': subscription.cancel_at_period_end
            }
        }
    
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': f'Stripe API error: {str(e)}',
            'error_type': type(e).__name__
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

def is_stripe_configured() -> bool:
    """
    Check if Stripe is properly configured
    
    Returns:
        True if Stripe API key is set, False otherwise
    """
    return bool(stripe.api_key)

