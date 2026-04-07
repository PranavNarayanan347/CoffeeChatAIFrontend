// Admin service for email tracking and user management
const API_BASE_URL = 'http://localhost:5000';

export interface EmailRecord {
  id: number;
  user_id: number;
  user_email: string | null;
  user_name: string | null;
  recipient_email: string;
  recipient_name: string | null;
  subject: string | null;
  email_body: string | null;
  email_type: string | null;
  status: string;
  gmail_draft_id: string | null;
  person_company: string | null;
  person_role: string | null;
  ip_address: string | null;
  created_at: string;
  updated_at: string;
}

export interface EmailStats {
  total_emails: number;
  by_status: { [key: string]: number };
  by_type: { [key: string]: number };
  daily_counts: Array<{ date: string; count: number }>;
  top_users: Array<{
    user_id: number;
    email: string;
    name: string | null;
    email_count: number;
  }>;
  top_recipients: Array<{
    recipient_email: string;
    recipient_name: string | null;
    email_count: number;
  }>;
}

export interface UserRecord {
  id: number;
  email: string;
  name: string | null;
  is_admin: boolean;
  created_at: string;
  last_login: string | null;
}

class AdminService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private getAuthHeader(): HeadersInit {
    const token = localStorage.getItem('coffeechat_access_token');
    return {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };
  }

  /**
   * Get all emails with pagination
   */
  async getEmails(params?: {
    page?: number;
    per_page?: number;
    status?: string;
    email_type?: string;
    user_id?: number;
  }): Promise<{
    success: boolean;
    emails: EmailRecord[];
    pagination: {
      page: number;
      per_page: number;
      total: number;
      pages: number;
    };
  }> {
    const queryParams = new URLSearchParams();
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    if (params?.status) queryParams.append('status', params.status);
    if (params?.email_type) queryParams.append('email_type', params.email_type);
    if (params?.user_id) queryParams.append('user_id', params.user_id.toString());

    const response = await fetch(
      `${this.baseUrl}/api/admin/emails?${queryParams.toString()}`,
      {
        method: 'GET',
        headers: this.getAuthHeader(),
      }
    );

    if (!response.ok) {
      if (response.status === 403) {
        throw new Error('Admin access required');
      }
      throw new Error(`Failed to fetch emails: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get email statistics
   */
  async getEmailStats(): Promise<{ success: boolean; stats: EmailStats }> {
    const response = await fetch(`${this.baseUrl}/api/admin/emails/stats`, {
      method: 'GET',
      headers: this.getAuthHeader(),
    });

    if (!response.ok) {
      if (response.status === 403) {
        throw new Error('Admin access required');
      }
      throw new Error(`Failed to fetch stats: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get all users
   */
  async getUsers(params?: {
    page?: number;
    per_page?: number;
  }): Promise<{
    success: boolean;
    users: UserRecord[];
    pagination: {
      page: number;
      per_page: number;
      total: number;
      pages: number;
    };
  }> {
    const queryParams = new URLSearchParams();
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());

    const response = await fetch(
      `${this.baseUrl}/api/admin/users?${queryParams.toString()}`,
      {
        method: 'GET',
        headers: this.getAuthHeader(),
      }
    );

    if (!response.ok) {
      if (response.status === 403) {
        throw new Error('Admin access required');
      }
      throw new Error(`Failed to fetch users: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Make a user an admin
   */
  async makeUserAdmin(userId: number): Promise<{ success: boolean; message: string }> {
    const response = await fetch(`${this.baseUrl}/api/admin/users/${userId}/make-admin`, {
      method: 'POST',
      headers: this.getAuthHeader(),
    });

    if (!response.ok) {
      if (response.status === 403) {
        throw new Error('Admin access required');
      }
      const error = await response.json();
      throw new Error(error.error || 'Failed to make user admin');
    }

    return response.json();
  }
}

export const adminService = new AdminService();



