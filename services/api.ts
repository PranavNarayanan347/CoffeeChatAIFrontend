// API service for communicating with the backend
import { authService } from './auth';

const API_BASE_URL = 'http://localhost:5000';

export interface Person {
  name: string;
  title: string;
  company: string;
  work_email: string;
  personal_email: string;
  linkedin: string;
  education: Array<{
    school_name: string;
    school_type: string;
    degrees: string[];
    majors: string[];
    start_date: string;
    end_date: string;
    gpa: string;
  }>;
}

export interface EmailData {
  recipient: string;
  subject: string;
  body: string;
  matchedContact: {
    name: string;
    role: string;
    company: string;
  };
}

export interface ChatResponse {
  success: boolean;
  message: string;
  search_results: Person[];
  count: number;
  error?: string;
}

export interface GmailDraftResponse {
  success: boolean;
  draft_id?: string;
  message?: string;
  error?: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async healthCheck(): Promise<{ status: string; message: string }> {
    const response = await fetch(`${this.baseUrl}/api/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return response.json();
  }

  async searchPeople(query: string): Promise<{ success: boolean; results: Person[]; error?: string }> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/search-people`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token expired, clear auth
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      throw new Error(`Search failed: ${response.statusText}`);
    }

    return response.json();
  }

  async generateEmail(personInfo: Person, emailType: string = 'cold_outreach', customMessage: string = ''): Promise<{ success: boolean; email_content: string; error?: string }> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/generate-email`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        person_info: personInfo,
        email_type: emailType,
        custom_message: customMessage,
      }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      throw new Error(`Email generation failed: ${response.statusText}`);
    }

    return response.json();
  }

  async createGmailDraft(toEmail: string, subject: string, body: string): Promise<GmailDraftResponse> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/create-gmail-draft`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        to_email: toEmail,
        subject: subject,
        body: body,
      }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      throw new Error(`Gmail draft creation failed: ${response.statusText}`);
    }

    return response.json();
  }

  async chat(message: string): Promise<ChatResponse> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      throw new Error(`Chat failed: ${response.statusText}`);
    }

    return response.json();
  }

  async updateEmail(originalEmail: string, personInfo: Person, updateInstructions: string, emailType: string = 'cold_outreach'): Promise<{ success: boolean; updated_email: string; error?: string }> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/update-email`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        original_email: originalEmail,
        person_info: personInfo,
        update_instructions: updateInstructions,
        email_type: emailType,
      }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      throw new Error(`Email update failed: ${response.statusText}`);
    }

    return response.json();
  }

  async parseResume(file: File): Promise<{ success: boolean; profile_data: any; talking_points: string[]; user: any; error?: string }> {
    const token = authService.getToken();
    if (!token) {
      throw new Error('Authentication required');
    }

    // Convert file to base64
    const fileData = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        // Remove data URL prefix
        const base64 = result.split(',')[1];
        resolve(base64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/resume/parse`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        file_data: fileData,
        filename: file.name,
      }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      const errorData = await response.json();
      throw new Error(errorData.error || 'Resume parsing failed');
    }

    return response.json();
  }

  async updateProfile(profileData: {
    name?: string;
    bio?: string;
    company?: string;
    role?: string;
    linkedin_profile?: string;
    profile_picture_url?: string;
    preferences?: any;
  }): Promise<{ success: boolean; user: any; error?: string }> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/auth/update-profile`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(profileData),
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      const errorData = await response.json();
      throw new Error(errorData.error || 'Profile update failed');
    }

    return response.json();
  }

  async getUserStats(): Promise<{ success: boolean; stats: { emails_generated: number; conversations: number }; error?: string }> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const response = await fetch(`${this.baseUrl}/api/user/stats`, {
      method: 'GET',
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to get user stats');
    }

    return response.json();
  }

  async getUserEmails(params?: {
    limit?: number;
    status?: string;
  }): Promise<{
    success: boolean;
    emails: Array<{
      id: number;
      recipient_email: string;
      recipient_name: string | null;
      subject: string | null;
      status: string;
      person_company: string | null;
      person_role: string | null;
      created_at: string;
    }>;
    count: number;
    error?: string;
  }> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...authService.getAuthHeader(),
    };

    const queryParams = new URLSearchParams();
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.status) queryParams.append('status', params.status);

    const response = await fetch(
      `${this.baseUrl}/api/user/emails?${queryParams.toString()}`,
      {
        method: 'GET',
        headers,
      }
    );

    if (!response.ok) {
      if (response.status === 401) {
        authService.clearAuth();
        throw new Error('Session expired. Please login again.');
      }
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to get user emails');
    }

    return response.json();
  }
}

export const apiService = new ApiService();
