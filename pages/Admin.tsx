import { useState, useEffect } from "react";
import { Card } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { 
  Mail, 
  Users, 
  TrendingUp, 
  Calendar, 
  User, 
  Building2,
  RefreshCw,
  AlertCircle,
  CheckCircle,
  Clock,
  FileText
} from "lucide-react";
import { adminService, EmailRecord, EmailStats, UserRecord } from "../services/admin";
import { authService } from "../services/auth";

export function Admin() {
  const [activeTab, setActiveTab] = useState<"emails" | "stats" | "users">("stats");
  const [emails, setEmails] = useState<EmailRecord[]>([]);
  const [stats, setStats] = useState<EmailStats | null>(null);
  const [users, setUsers] = useState<UserRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [emailPage, setEmailPage] = useState(1);
  const [userPage, setUserPage] = useState(1);
  const [filters, setFilters] = useState({
    status: "",
    email_type: "",
  });

  useEffect(() => {
    loadData();
  }, [activeTab, emailPage, userPage, filters]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      if (activeTab === "emails") {
        const result = await adminService.getEmails({
          page: emailPage,
          per_page: 20,
          ...(filters.status && { status: filters.status }),
          ...(filters.email_type && { email_type: filters.email_type }),
        });
        setEmails(result.emails);
      } else if (activeTab === "stats") {
        const result = await adminService.getEmailStats();
        setStats(result.stats);
      } else if (activeTab === "users") {
        const result = await adminService.getUsers({
          page: userPage,
          per_page: 20,
        });
        setUsers(result.users);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load data");
      if (err.message.includes("Admin access required")) {
        // Redirect to profile or show message
      }
    } finally {
      setLoading(false);
    }
  };

  const handleMakeAdmin = async (userId: number) => {
    try {
      await adminService.makeUserAdmin(userId);
      await loadData(); // Reload users
    } catch (err: any) {
      setError(err.message || "Failed to make user admin");
    }
  };

  const getStatusBadge = (status: string) => {
    const variants: { [key: string]: { color: string; icon: any } } = {
      generated: { color: "bg-blue-100 text-blue-800", icon: FileText },
      draft_created: { color: "bg-amber-100 text-amber-800", icon: CheckCircle },
      sent: { color: "bg-green-100 text-green-800", icon: Mail },
      failed: { color: "bg-red-100 text-red-800", icon: AlertCircle },
    };
    
    const variant = variants[status] || { color: "bg-gray-100 text-gray-800", icon: Clock };
    const Icon = variant.icon;
    
    return (
      <Badge className={variant.color}>
        <Icon className="w-3 h-3 mr-1" />
        {status.replace("_", " ").toUpperCase()}
      </Badge>
    );
  };

  if (loading && !stats && !emails.length && !users.length) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white via-amber-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-amber-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-stone-600">Loading admin dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-amber-50 to-orange-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-white to-amber-50 border-b border-amber-200">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-amber-700 via-orange-600 to-amber-600 bg-clip-text text-transparent mb-2">
                Admin Dashboard
              </h1>
              <p className="text-amber-700">Email tracking and user management</p>
            </div>
            <Button
              onClick={loadData}
              variant="outline"
              className="border-amber-300"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Tabs */}
        <div className="flex gap-4 mb-6 border-b border-amber-200">
          <button
            onClick={() => setActiveTab("stats")}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === "stats"
                ? "text-amber-700 border-b-2 border-amber-600"
                : "text-stone-600 hover:text-amber-600"
            }`}
          >
            <TrendingUp className="w-4 h-4 inline mr-2" />
            Statistics
          </button>
          <button
            onClick={() => setActiveTab("emails")}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === "emails"
                ? "text-amber-700 border-b-2 border-amber-600"
                : "text-stone-600 hover:text-amber-600"
            }`}
          >
            <Mail className="w-4 h-4 inline mr-2" />
            Emails ({stats?.total_emails || 0})
          </button>
          <button
            onClick={() => setActiveTab("users")}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === "users"
                ? "text-amber-700 border-b-2 border-amber-600"
                : "text-stone-600 hover:text-amber-600"
            }`}
          >
            <Users className="w-4 h-4 inline mr-2" />
            Users
          </button>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700">
            <AlertCircle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        )}

        {/* Stats Tab */}
        {activeTab === "stats" && stats && (
          <div className="space-y-6">
            {/* Overview Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card className="p-6 bg-gradient-to-br from-white to-amber-50">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-stone-600 mb-1">Total Emails</p>
                    <p className="text-3xl font-bold text-amber-900">{stats.total_emails}</p>
                  </div>
                  <Mail className="w-8 h-8 text-amber-600" />
                </div>
              </Card>

              <Card className="p-6 bg-gradient-to-br from-white to-orange-50">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-stone-600 mb-1">Generated</p>
                    <p className="text-3xl font-bold text-orange-900">
                      {stats.by_status.generated || 0}
                    </p>
                  </div>
                  <FileText className="w-8 h-8 text-orange-600" />
                </div>
              </Card>

              <Card className="p-6 bg-gradient-to-br from-white to-green-50">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-stone-600 mb-1">Drafts Created</p>
                    <p className="text-3xl font-bold text-green-900">
                      {stats.by_status.draft_created || 0}
                    </p>
                  </div>
                  <CheckCircle className="w-8 h-8 text-green-600" />
                </div>
              </Card>

              <Card className="p-6 bg-gradient-to-br from-white to-blue-50">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-stone-600 mb-1">Top Users</p>
                    <p className="text-3xl font-bold text-blue-900">
                      {stats.top_users.length}
                    </p>
                  </div>
                  <Users className="w-8 h-8 text-blue-600" />
                </div>
              </Card>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Top Users */}
              <Card className="p-6 bg-white">
                <h3 className="text-lg font-semibold text-stone-900 mb-4">Top Users</h3>
                <div className="space-y-3">
                  {stats.top_users.map((user, idx) => (
                    <div
                      key={user.user_id}
                      className="flex items-center justify-between p-3 bg-amber-50 rounded-lg"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-amber-600 text-white flex items-center justify-center font-bold">
                          {idx + 1}
                        </div>
                        <div>
                          <p className="font-medium text-stone-900">{user.name || user.email}</p>
                          <p className="text-sm text-stone-600">{user.email}</p>
                        </div>
                      </div>
                      <Badge className="bg-amber-600 text-white">{user.email_count}</Badge>
                    </div>
                  ))}
                </div>
              </Card>

              {/* Top Recipients */}
              <Card className="p-6 bg-white">
                <h3 className="text-lg font-semibold text-stone-900 mb-4">Top Recipients</h3>
                <div className="space-y-3">
                  {stats.top_recipients.map((recipient, idx) => (
                    <div
                      key={recipient.recipient_email}
                      className="flex items-center justify-between p-3 bg-orange-50 rounded-lg"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-orange-600 text-white flex items-center justify-center font-bold">
                          {idx + 1}
                        </div>
                        <div>
                          <p className="font-medium text-stone-900">
                            {recipient.recipient_name || recipient.recipient_email}
                          </p>
                          <p className="text-sm text-stone-600">{recipient.recipient_email}</p>
                        </div>
                      </div>
                      <Badge className="bg-orange-600 text-white">{recipient.email_count}</Badge>
                    </div>
                  ))}
                </div>
              </Card>
            </div>

            {/* Email Types */}
            <Card className="p-6 bg-white">
              <h3 className="text-lg font-semibold text-stone-900 mb-4">Emails by Type</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(stats.by_type).map(([type, count]) => (
                  <div
                    key={type}
                    className="p-4 bg-gradient-to-br from-amber-50 to-orange-50 rounded-lg text-center"
                  >
                    <p className="text-2xl font-bold text-amber-900">{count}</p>
                    <p className="text-sm text-stone-600 mt-1">
                      {type.replace("_", " ").toUpperCase()}
                    </p>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}

        {/* Emails Tab */}
        {activeTab === "emails" && (
          <div className="space-y-6">
            {/* Filters */}
            <Card className="p-4 bg-white">
              <div className="flex gap-4">
                <select
                  value={filters.status}
                  onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                  className="px-4 py-2 border border-amber-300 rounded-lg"
                >
                  <option value="">All Statuses</option>
                  <option value="generated">Generated</option>
                  <option value="draft_created">Draft Created</option>
                  <option value="sent">Sent</option>
                  <option value="failed">Failed</option>
                </select>
                <select
                  value={filters.email_type}
                  onChange={(e) => setFilters({ ...filters, email_type: e.target.value })}
                  className="px-4 py-2 border border-amber-300 rounded-lg"
                >
                  <option value="">All Types</option>
                  <option value="cold_outreach">Cold Outreach</option>
                  <option value="job_inquiry">Job Inquiry</option>
                  <option value="collaboration">Collaboration</option>
                  <option value="informational_interview">Informational Interview</option>
                </select>
              </div>
            </Card>

            {/* Email List */}
            <div className="space-y-4">
              {emails.map((email) => (
                <Card key={email.id} className="p-6 bg-white hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        {getStatusBadge(email.status)}
                        <span className="text-sm text-stone-600">
                          {new Date(email.created_at).toLocaleString()}
                        </span>
                      </div>
                      <h4 className="font-semibold text-stone-900 mb-1">
                        To: {email.recipient_name || email.recipient_email}
                      </h4>
                      <p className="text-sm text-stone-600 mb-2">
                        From: {email.user_name || email.user_email}
                      </p>
                      {email.subject && (
                        <p className="text-stone-700 mb-2">
                          <strong>Subject:</strong> {email.subject}
                        </p>
                      )}
                      {email.person_company && (
                        <div className="flex items-center gap-4 text-sm text-stone-600">
                          <span className="flex items-center gap-1">
                            <Building2 className="w-4 h-4" />
                            {email.person_company}
                          </span>
                          {email.person_role && (
                            <span className="flex items-center gap-1">
                              <User className="w-4 h-4" />
                              {email.person_role}
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </Card>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex justify-center gap-2">
              <Button
                onClick={() => setEmailPage((p) => Math.max(1, p - 1))}
                disabled={emailPage === 1}
                variant="outline"
              >
                Previous
              </Button>
              <span className="px-4 py-2">Page {emailPage}</span>
              <Button
                onClick={() => setEmailPage((p) => p + 1)}
                variant="outline"
              >
                Next
              </Button>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === "users" && (
          <div className="space-y-4">
            {users.map((user) => (
              <Card key={user.id} className="p-6 bg-white">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="font-semibold text-stone-900">{user.name || user.email}</h4>
                      {user.is_admin && (
                        <Badge className="bg-purple-600 text-white">Admin</Badge>
                      )}
                    </div>
                    <p className="text-sm text-stone-600">{user.email}</p>
                    {user.last_login && (
                      <p className="text-xs text-stone-500 mt-1">
                        Last login: {new Date(user.last_login).toLocaleString()}
                      </p>
                    )}
                  </div>
                  {!user.is_admin && (
                    <Button
                      onClick={() => handleMakeAdmin(user.id)}
                      size="sm"
                      className="bg-purple-600 hover:bg-purple-700"
                    >
                      Make Admin
                    </Button>
                  )}
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}



