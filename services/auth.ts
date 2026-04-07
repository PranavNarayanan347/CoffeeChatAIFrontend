// Authentication service for user login, registration, and token management
const API_BASE_URL = 'http://localhost:5000';

export interface User {
  id: number;
  email: string;
  name: string | null;
  stripe_customer_id: string | null;
  bio: string | null;
  company: string | null;
  role: string | null;
  linkedin_profile: string | null;
  profile_picture_url: string | null;
  email_verified: boolean;
  is_admin: boolean;
  preferences: any;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  success: boolean;
  message?: string;
  user: User;
  access_token: string;
  stripe_customer_created?: boolean;
  stripe_warning?: string;
}

export interface ErrorResponse {
  error: string;
  message?: string;
}

const TOKEN_KEY = 'coffeechat_access_token';
const USER_KEY = 'coffeechat_user';

class AuthService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Register a new user
   */
  async register(email: string, password: string, name?: string): Promise<AuthResponse> {
    const response = await fetch(`${this.baseUrl}/api/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.trim().toLowerCase(),
        password,
        name: name?.trim() || undefined,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Registration failed');
    }

    // Store token and user info
    if (data.access_token) {
      this.setToken(data.access_token);
      this.setUser(data.user);
    }

    return data;
  }

  /**
   * Login with email and password
   */
  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await fetch(`${this.baseUrl}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.trim().toLowerCase(),
        password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }

    // Store token and user info
    if (data.access_token) {
      this.setToken(data.access_token);
      this.setUser(data.user);
    }

    return data;
  }

  /**
   * Logout the current user
   */
  async logout(): Promise<void> {
    const token = this.getToken();
    
    if (token) {
      try {
        // Call logout endpoint (optional, token is stateless)
        await fetch(`${this.baseUrl}/api/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
      } catch (error) {
        // Ignore errors on logout - we'll clear local storage anyway
        console.warn('Logout API call failed:', error);
      }
    }

    // Clear local storage
    this.clearAuth();
  }

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<User | null> {
    const token = this.getToken();
    
    if (!token) {
      return null;
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        // Token might be invalid, clear it
        if (response.status === 401) {
          this.clearAuth();
        }
        return null;
      }

      const data = await response.json();
      
      if (data.success && data.user) {
        this.setUser(data.user);
        return data.user;
      }

      return null;
    } catch (error) {
      console.error('Failed to get current user:', error);
      return null;
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  /**
   * Get stored authentication token
   */
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  /**
   * Set authentication token
   */
  private setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token);
  }

  /**
   * Get stored user info
   */
  getUser(): User | null {
    const userStr = localStorage.getItem(USER_KEY);
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  }

  /**
   * Set user info in storage
   */
  private setUser(user: User): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  /**
   * Clear all authentication data
   */
  clearAuth(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  /**
   * Get authorization header for API requests
   */
  getAuthHeader(): { Authorization: string } | {} {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }
}

export const authService = new AuthService();

