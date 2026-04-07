// Subscription service for Stripe integration
import { authService } from './auth';

const API_BASE_URL = 'http://localhost:5000';

export interface SubscriptionStatus {
  success: boolean;
  status: 'none' | 'trial' | 'active' | 'expired' | 'canceled';
  is_trial: boolean;
  trial_end?: string;
  current_period_end?: string;
  subscription?: {
    id: number;
    user_id: number;
    stripe_subscription_id: string | null;
    status: string;
    plan_type: string | null;
    current_period_end: string | null;
    trial_start: string | null;
    trial_period_end: string | null;
    created_at: string;
    updated_at: string;
  };
  error?: string;
}

export interface CheckoutSessionResponse {
  success: boolean;
  checkout_url?: string;
  session_id?: string;
  error?: string;
}

export interface PortalSessionResponse {
  success: boolean;
  url?: string;
  error?: string;
}

class SubscriptionService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async createCheckoutSession(successUrl?: string, cancelUrl?: string): Promise<CheckoutSessionResponse> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/subscription/create-checkout-session`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        success_url: successUrl,
        cancel_url: cancelUrl,
      }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to create checkout session');
    }

    return response.json();
  }

  async getSubscriptionStatus(): Promise<SubscriptionStatus> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/subscription/status`, {
      method: 'GET',
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to get subscription status');
    }

    return response.json();
  }

  async cancelSubscription(): Promise<{ success: boolean; message?: string; error?: string }> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/subscription/cancel`, {
      method: 'POST',
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to cancel subscription');
    }

    return response.json();
  }

  async createPortalSession(returnUrl?: string): Promise<PortalSessionResponse> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/subscription/portal`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        return_url: returnUrl,
      }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to create portal session');
    }

    return response.json();
  }
}

export const subscriptionService = new SubscriptionService();



