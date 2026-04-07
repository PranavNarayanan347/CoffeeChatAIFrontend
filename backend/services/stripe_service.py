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

def create_checkout_session(customer_id: str, price_id: str, success_url: str, cancel_url: str, trial_period_days: int = 7) -> Dict[str, Any]:
    """
    Create a Stripe Checkout Session with trial period
    
    Args:
        customer_id: Stripe customer ID
        price_id: Stripe Price ID for the subscription
        success_url: URL to redirect to after successful checkout
        cancel_url: URL to redirect to if checkout is canceled
        trial_period_days: Number of days for trial period (default: 7)
    
    Returns:
        Dictionary containing checkout session data or error information
    """
    try:
        if not stripe.api_key:
            return {
                'success': False,
                'error': 'Stripe API key not configured'
            }
        
        checkout_session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            subscription_data={
                'trial_period_days': trial_period_days,
            },
            success_url=success_url,
            cancel_url=cancel_url,
            allow_promotion_codes=True,
        )
        
        return {
            'success': True,
            'checkout_session': {
                'id': checkout_session.id,
                'url': checkout_session.url
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

def create_subscription_with_trial(customer_id: str, price_id: str, trial_period_days: int = 7) -> Dict[str, Any]:
    """
    Create a subscription directly with trial period
    
    Args:
        customer_id: Stripe customer ID
        price_id: Stripe Price ID for the subscription
        trial_period_days: Number of days for trial period (default: 7)
    
    Returns:
        Dictionary containing subscription data or error information
    """
    try:
        if not stripe.api_key:
            return {
                'success': False,
                'error': 'Stripe API key not configured'
            }
        
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            trial_period_days=trial_period_days,
        )
        
        return {
            'success': True,
            'subscription': {
                'id': subscription.id,
                'status': subscription.status,
                'trial_start': subscription.trial_start,
                'trial_end': subscription.trial_end,
                'current_period_end': subscription.current_period_end,
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

def get_subscription_status(customer_id: str) -> Dict[str, Any]:
    """
    Get subscription status for a customer, including trial information
    
    Args:
        customer_id: Stripe customer ID
    
    Returns:
        Dictionary containing subscription status (active, trial, expired, none)
    """
    try:
        if not stripe.api_key:
            return {
                'success': False,
                'error': 'Stripe API key not configured'
            }
        
        # Get all subscriptions (including trialing)
        subscriptions = stripe.Subscription.list(
            customer=customer_id,
            status='all',
            limit=10
        )
        
        if not subscriptions.data:
            return {
                'success': True,
                'status': 'none',
                'has_subscription': False,
                'subscription': None
            }
        
        # Find active or trialing subscription
        active_subscription = None
        for sub in subscriptions.data:
            if sub.status in ['active', 'trialing']:
                active_subscription = sub
                break
        
        if not active_subscription:
            return {
                'success': True,
                'status': 'expired',
                'has_subscription': False,
                'subscription': None
            }
        
        # Determine if in trial
        is_trial = active_subscription.status == 'trialing'
        trial_end = None
        if active_subscription.trial_end:
            from datetime import datetime
            trial_end = datetime.fromtimestamp(active_subscription.trial_end)
        
        return {
            'success': True,
            'status': 'trial' if is_trial else 'active',
            'has_subscription': True,
            'subscription': {
                'id': active_subscription.id,
                'status': active_subscription.status,
                'trial_end': active_subscription.trial_end,
                'current_period_end': active_subscription.current_period_end,
            },
            'is_trial': is_trial,
            'trial_end': trial_end.isoformat() if trial_end else None
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

def create_portal_session(customer_id: str, return_url: str) -> Dict[str, Any]:
    """
    Create a Stripe Customer Portal session for subscription management
    
    Args:
        customer_id: Stripe customer ID
        return_url: URL to return to after portal session
    
    Returns:
        Dictionary containing portal session URL or error information
    """
    try:
        if not stripe.api_key:
            return {
                'success': False,
                'error': 'Stripe API key not configured'
            }
        
        portal_session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )
        
        return {
            'success': True,
            'url': portal_session.url
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

