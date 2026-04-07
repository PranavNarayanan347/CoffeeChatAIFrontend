import { useState, useEffect } from "react";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { Label } from "../components/ui/label";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Upload, FileText, Sparkles, User, Mail, Briefcase, GraduationCap, Award, AlertCircle, CheckCircle, ArrowRight, CreditCard, ExternalLink } from "lucide-react";
import { Badge } from "../components/ui/badge";
import { authService } from "../services/auth";
import { apiService } from "../services/api";
import { subscriptionService, SubscriptionStatus } from "../services/subscription";

interface ProfileProps {
  userEmail: string;
  initialTalkingPoints?: string[];
  initialResumeFileName?: string;
}

export function Profile({ userEmail, initialTalkingPoints = [], initialResumeFileName = "" }: ProfileProps) {
  const [uploading, setUploading] = useState(false);
  const [hasResume, setHasResume] = useState(initialTalkingPoints.length > 0);
  const [talkingPoints, setTalkingPoints] = useState<string[]>(initialTalkingPoints);
  const [resumeFileName, setResumeFileName] = useState(initialResumeFileName || "");
  
  // Profile fields
  const [name, setName] = useState("");
  const [bio, setBio] = useState("");
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");
  const [linkedinProfile, setLinkedinProfile] = useState("");
  
  // UI state
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [loading, setLoading] = useState(true);
  
  // Stats state
  const [emailsGenerated, setEmailsGenerated] = useState(0);
  const [conversations, setConversations] = useState(0);
  
  // Subscription state
  const [subscriptionStatus, setSubscriptionStatus] = useState<SubscriptionStatus | null>(null);
  const [loadingSubscription, setLoadingSubscription] = useState(true);
  const [managingSubscription, setManagingSubscription] = useState(false);

  // Load user data on mount
  useEffect(() => {
    const loadUserData = async () => {
      try {
        const user = await authService.getCurrentUser();
        if (user) {
          setName(user.name || "");
          setBio(user.bio || "");
          setCompany(user.company || "");
          setRole(user.role || "");
          setLinkedinProfile(user.linkedin_profile || "");
        } else {
          // Fallback to stored user
          const storedUser = authService.getUser();
          if (storedUser) {
            setName(storedUser.name || "");
            setBio(storedUser.bio || "");
            setCompany(storedUser.company || "");
            setRole(storedUser.role || "");
            setLinkedinProfile(storedUser.linkedin_profile || "");
          }
        }
        
        // Load user stats
        try {
          const statsResult = await apiService.getUserStats();
          if (statsResult.success && statsResult.stats) {
            setEmailsGenerated(statsResult.stats.emails_generated || 0);
            setConversations(statsResult.stats.conversations || 0);
          }
        } catch (statsError) {
          console.error("Failed to load user stats:", statsError);
          // Don't fail the whole page if stats fail
        }
        
        // Load subscription status
        try {
          const subStatus = await subscriptionService.getSubscriptionStatus();
          if (subStatus && subStatus.success !== false) {
            setSubscriptionStatus(subStatus);
          } else {
            // If API returns error, set default 'none' status
            setSubscriptionStatus({
              success: true,
              status: 'none',
              is_trial: false
            } as SubscriptionStatus);
          }
        } catch (subError) {
          console.error("Failed to load subscription status:", subError);
          // Set default status on error so UI still shows
          setSubscriptionStatus({
            success: true,
            status: 'none',
            is_trial: false
          } as SubscriptionStatus);
        } finally {
          setLoadingSubscription(false);
        }
      } catch (error) {
        console.error("Failed to load user data:", error);
      } finally {
        setLoading(false);
      }
    };

    loadUserData();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    const validTypes = ['.pdf', '.doc', '.docx'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!validTypes.includes(fileExtension)) {
      setSaveMessage({ type: 'error', text: 'Please upload a PDF, DOC, or DOCX file' });
      return;
    }

    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      setSaveMessage({ type: 'error', text: 'File size must be less than 5MB' });
      return;
    }

    setUploading(true);
    setSaveMessage(null);
    
    try {
      const result = await apiService.parseResume(file);
      
      if (result.success) {
        setResumeFileName(file.name);
        setHasResume(true);
        setTalkingPoints(result.talking_points || []);
        
        // Update profile fields from parsed resume
        if (result.profile_data) {
          if (result.profile_data.bio) setBio(result.profile_data.bio);
          if (result.profile_data.company) setCompany(result.profile_data.company);
          if (result.profile_data.role) setRole(result.profile_data.role);
          if (result.profile_data.linkedin_profile) setLinkedinProfile(result.profile_data.linkedin_profile);
        }
        
        // Update auth service with new user data
        if (result.user) {
          authService.setUser(result.user);
        }
        
        setSaveMessage({ type: 'success', text: 'Resume parsed successfully!' });
      } else {
        throw new Error(result.error || 'Failed to parse resume');
      }
    } catch (error) {
      setSaveMessage({ 
        type: 'error', 
        text: error instanceof Error ? error.message : 'Failed to upload resume. Please try again.' 
      });
    } finally {
      setUploading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setSaveMessage(null);

    try {
      const result = await apiService.updateProfile({
        name: name.trim() || undefined,
        bio: bio.trim() || undefined,
        company: company.trim() || undefined,
        role: role.trim() || undefined,
        linkedin_profile: linkedinProfile.trim() || undefined,
      });

      if (result.success) {
        // Update auth service with new user data
        if (result.user) {
          authService.setUser(result.user);
        }
        
        setSaveMessage({ type: 'success', text: 'Profile updated successfully!' });
        
        // Clear message after 3 seconds
        setTimeout(() => setSaveMessage(null), 3000);
      }
    } catch (error) {
      setSaveMessage({ 
        type: 'error', 
        text: error instanceof Error ? error.message : 'Failed to save profile. Please try again.' 
      });
    } finally {
      setSaving(false);
    }
  };

  const generateMorePoints = () => {
    const newPoints = [
      "Conducted user interviews with 50+ participants for product validation",
      "Experience with A/B testing and conversion rate optimization",
      "Skilled in creating product roadmaps and prioritization frameworks",
    ];
    setTalkingPoints([...talkingPoints, ...newPoints]);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white via-amber-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-amber-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-stone-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-amber-50 to-orange-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-white to-amber-50 border-b border-amber-200">
        <div className="max-w-5xl mx-auto px-6 py-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-amber-700 via-orange-600 to-amber-600 bg-clip-text text-transparent mb-2">Your Profile</h1>
          <p className="text-amber-700">
            Manage your information and resume talking points
          </p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Profile Info */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="p-8 border-amber-200 bg-gradient-to-br from-white to-amber-50 hover:shadow-xl transition-all duration-300">
              <div className="flex flex-col items-center text-center">
                <div className="w-28 h-28 rounded-full bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center mb-6 shadow-lg">
                  <User className="w-14 h-14 text-white" />
                </div>
                <h2 className="text-xl font-semibold text-amber-900 mb-2">
                  {name || userEmail.split('@')[0] || 'User'}
                </h2>
                <p className="text-sm text-amber-700 mb-6">{userEmail}</p>
                {company && role && (
                  <p className="text-sm text-amber-600 mb-2">{role} at {company}</p>
                )}
                {company && !role && (
                  <p className="text-sm text-amber-600 mb-2">{company}</p>
                )}
                {role && !company && (
                  <p className="text-sm text-amber-600 mb-2">{role}</p>
                )}
                {loadingSubscription ? (
                  <Badge className="bg-gradient-to-r from-amber-500 to-orange-500 text-white border-0 shadow-lg">
                    Loading...
                  </Badge>
                ) : subscriptionStatus?.status === 'trial' ? (
                  <Badge className="bg-gradient-to-r from-green-500 to-emerald-600 text-white border-0 shadow-lg">
                    Free Trial
                  </Badge>
                ) : subscriptionStatus?.status === 'active' ? (
                  <Badge className="bg-gradient-to-r from-amber-500 to-orange-500 text-white border-0 shadow-lg">
                    Premium
                  </Badge>
                ) : (
                  <Badge className="bg-gradient-to-r from-amber-500 to-orange-500 text-white border-0 shadow-lg">
                    Free Plan
                  </Badge>
                )}
              </div>
            </Card>

            <Card className="p-8 border-orange-200 bg-gradient-to-br from-white to-orange-50 hover:shadow-xl transition-all duration-300">
              <h3 className="text-orange-900 font-semibold mb-6 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-orange-600" />
                Quick Stats
              </h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg">
                  <span className="text-sm text-orange-700 font-medium">Emails Generated</span>
                  <span className="text-orange-900 font-bold text-lg">{emailsGenerated}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-gradient-to-r from-amber-50 to-orange-50 rounded-lg">
                  <span className="text-sm text-amber-700 font-medium">Conversations</span>
                  <span className="text-amber-900 font-bold text-lg">{conversations}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg">
                  <span className="text-sm text-orange-700 font-medium">Talking Points</span>
                  <span className="text-orange-900 font-bold text-lg">{talkingPoints.length}</span>
                </div>
              </div>
            </Card>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Basic Info */}
            <Card className="p-8 border-amber-200 bg-gradient-to-br from-white to-amber-50 hover:shadow-xl transition-all duration-300">
              <h3 className="text-amber-900 font-semibold mb-6 flex items-center gap-3">
                <div className="w-8 h-8 bg-gradient-to-br from-amber-500 to-orange-500 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-white" />
                </div>
                Basic Information
              </h3>
              <div className="space-y-6">
                <div>
                  <Label htmlFor="name" className="text-amber-700 font-medium">Full Name</Label>
                  <Input
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="border-amber-300 focus:border-amber-500 focus:ring-amber-500 mt-2"
                  />
                </div>
                <div>
                  <Label htmlFor="email" className="text-amber-700 font-medium">Email</Label>
                  <div className="relative mt-2">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-amber-500" />
                    <Input
                      id="email"
                      value={userEmail}
                      disabled
                      className="pl-10 border-amber-300 bg-gradient-to-r from-amber-50 to-orange-50 text-amber-700"
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="bio" className="text-amber-700 font-medium">Professional Bio</Label>
                  <Textarea
                    id="bio"
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                    rows={3}
                    placeholder="Tell us about yourself..."
                    className="border-amber-300 focus:border-amber-500 focus:ring-amber-500 resize-none mt-2"
                  />
                </div>
                <div>
                  <Label htmlFor="company" className="text-amber-700 font-medium">Company</Label>
                  <Input
                    id="company"
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    placeholder="Your current company"
                    className="border-amber-300 focus:border-amber-500 focus:ring-amber-500 mt-2"
                  />
                </div>
                <div>
                  <Label htmlFor="role" className="text-amber-700 font-medium">Role/Title</Label>
                  <Input
                    id="role"
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    placeholder="Your current role"
                    className="border-amber-300 focus:border-amber-500 focus:ring-amber-500 mt-2"
                  />
                </div>
                <div>
                  <Label htmlFor="linkedin" className="text-amber-700 font-medium">LinkedIn Profile</Label>
                  <Input
                    id="linkedin"
                    value={linkedinProfile}
                    onChange={(e) => setLinkedinProfile(e.target.value)}
                    placeholder="https://linkedin.com/in/yourprofile"
                    className="border-amber-300 focus:border-amber-500 focus:ring-amber-500 mt-2"
                  />
                </div>
              </div>
            </Card>

            {/* Resume Upload */}
            <Card className="p-8 border-orange-200 bg-gradient-to-br from-white to-orange-50 hover:shadow-xl transition-all duration-300">
              <h3 className="text-orange-900 font-semibold mb-6 flex items-center gap-3">
                <div className="w-8 h-8 bg-gradient-to-br from-orange-500 to-amber-600 rounded-full flex items-center justify-center">
                  <FileText className="w-4 h-4 text-white" />
                </div>
                Resume
              </h3>
              
              {!hasResume ? (
                <div className="border-2 border-dashed border-orange-300 rounded-xl p-8 text-center bg-gradient-to-br from-orange-50 to-amber-50">
                  <div className="w-20 h-20 rounded-full bg-gradient-to-br from-orange-500 to-amber-500 flex items-center justify-center mx-auto mb-6 shadow-lg">
                    <Upload className="w-10 h-10 text-white" />
                  </div>
                  <h4 className="text-orange-900 font-semibold mb-3 text-lg">
                    Upload your resume
                  </h4>
                  <p className="text-sm text-orange-700 mb-6 leading-relaxed">
                    We'll extract key talking points to help you in conversations
                  </p>
                  <label htmlFor="resume-upload">
                    <Button
                      className="bg-gradient-to-r from-orange-500 to-amber-600 hover:from-orange-600 hover:to-amber-700 text-white shadow-lg"
                      disabled={uploading}
                      asChild
                    >
                      <span>
                        {uploading ? "Processing..." : "Choose File"}
                      </span>
                    </Button>
                  </label>
                  <input
                    id="resume-upload"
                    type="file"
                    accept=".pdf,.doc,.docx"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                  <p className="text-xs text-orange-600 mt-3">
                    PDF, DOC, or DOCX (Max 5MB)
                  </p>
                </div>
              ) : (
                <div>
                  <div className="flex items-center gap-4 p-6 bg-gradient-to-r from-orange-50 to-amber-50 rounded-xl border border-orange-200 mb-6">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-orange-500 to-amber-500 flex items-center justify-center">
                      <FileText className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm text-orange-900 font-medium">{resumeFileName}</p>
                      <p className="text-xs text-orange-700">Uploaded successfully</p>
                    </div>
                    <label htmlFor="resume-reupload">
                      <Button variant="ghost" size="sm" className="text-orange-700 hover:text-orange-900 hover:bg-orange-100" asChild>
                        <span>Replace</span>
                      </Button>
                    </label>
                    <input
                      id="resume-reupload"
                      type="file"
                      accept=".pdf,.doc,.docx"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                  </div>
                </div>
              )}
            </Card>

            {/* Talking Points */}
            {hasResume && talkingPoints.length > 0 && (
              <Card className="p-8 border-amber-200 bg-gradient-to-br from-white to-amber-50 hover:shadow-xl transition-all duration-300">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-amber-900 font-semibold flex items-center gap-3">
                    <div className="w-8 h-8 bg-gradient-to-br from-amber-500 to-orange-500 rounded-full flex items-center justify-center">
                      <Sparkles className="w-4 h-4 text-white" />
                    </div>
                    AI-Generated Talking Points
                  </h3>
                  <Button
                    onClick={generateMorePoints}
                    variant="outline"
                    size="sm"
                    className="border-amber-300 text-amber-700 hover:bg-amber-50 hover:border-amber-400"
                  >
                    Generate More
                  </Button>
                </div>
                
                <p className="text-sm text-amber-700 mb-6 leading-relaxed">
                  Use these points to strengthen your networking conversations and emails
                </p>

                <div className="space-y-4">
                  {talkingPoints.map((point, index) => {
                    const icon = index % 4 === 0 ? Briefcase : 
                                 index % 4 === 1 ? GraduationCap :
                                 index % 4 === 2 ? Award : Sparkles;
                    const IconComponent = icon;
                    
                    return (
                      <div
                        key={index}
                        className="flex items-start gap-4 p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl hover:from-amber-100 hover:to-orange-100 transition-all duration-300 group border border-amber-200"
                      >
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center flex-shrink-0 shadow-lg group-hover:shadow-xl transition-all duration-300">
                          <IconComponent className="w-5 h-5 text-white" />
                        </div>
                        <p className="text-sm text-amber-800 pt-2 leading-relaxed">{point}</p>
                      </div>
                    );
                  })}
                </div>

                <div className="mt-6 p-6 bg-gradient-to-r from-orange-50 to-amber-50 rounded-xl border border-orange-200">
                  <p className="text-sm text-orange-900 leading-relaxed">
                    💡 <strong>Pro tip:</strong> Reference these points when crafting your networking emails to make your outreach more compelling and specific.
                  </p>
                </div>
              </Card>
            )}

            {/* Subscription Management */}
            <Card className="p-8 border-amber-200 bg-gradient-to-br from-white to-amber-50 hover:shadow-xl transition-all duration-300">
              <h3 className="text-amber-900 font-semibold mb-6 flex items-center gap-3">
                <div className="w-8 h-8 bg-gradient-to-br from-amber-500 to-orange-500 rounded-full flex items-center justify-center">
                  <CreditCard className="w-4 h-4 text-white" />
                </div>
                Subscription
              </h3>
              
              {loadingSubscription ? (
                <div className="text-center py-8">
                  <div className="w-8 h-8 border-4 border-amber-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-stone-600">Loading subscription...</p>
                </div>
              ) : !subscriptionStatus || subscriptionStatus?.status === 'none' || subscriptionStatus?.status === 'expired' || subscriptionStatus?.status === 'canceled' ? (
                <div className="space-y-4">
                  <div className="p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-lg border border-amber-200">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertCircle className="w-5 h-5 text-amber-600" />
                      <span className="font-semibold text-amber-900">No Active Subscription</span>
                    </div>
                    <p className="text-sm text-amber-700 mb-4">
                      Start your 7-day free trial to unlock all features
                    </p>
                  </div>
                  <Button
                    onClick={async () => {
                      setManagingSubscription(true);
                      try {
                        const checkoutResult = await subscriptionService.createCheckoutSession(
                          `${window.location.origin}/?subscription=success`,
                          `${window.location.origin}/?subscription=canceled`
                        );
                        if (checkoutResult.success && checkoutResult.checkout_url) {
                          window.location.href = checkoutResult.checkout_url;
                        }
                      } catch (error) {
                        setSaveMessage({
                          type: 'error',
                          text: error instanceof Error ? error.message : 'Failed to start checkout'
                        });
                      } finally {
                        setManagingSubscription(false);
                      }
                    }}
                    disabled={managingSubscription}
                    className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white"
                  >
                    {managingSubscription ? "Loading..." : "Start Free Trial"}
                    <ArrowRight className="w-5 h-5 ml-2" />
                  </Button>
                </div>
              ) : subscriptionStatus?.status === 'trial' ? (
                <div className="space-y-4">
                  <div className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200">
                    <div className="flex items-center gap-2 mb-2">
                      <CheckCircle className="w-5 h-5 text-green-600" />
                      <span className="font-semibold text-green-900">You're on a free trial</span>
                    </div>
                    {subscriptionStatus.trial_end && (
                      <p className="text-sm text-green-700">
                        Trial ends: {new Date(subscriptionStatus.trial_end).toLocaleDateString()}
                      </p>
                    )}
                  </div>
                  <Button
                    onClick={async () => {
                      setManagingSubscription(true);
                      try {
                        const portalResult = await subscriptionService.createPortalSession(window.location.href);
                        if (portalResult.success && portalResult.url) {
                          window.location.href = portalResult.url;
                        }
                      } catch (error) {
                        setSaveMessage({
                          type: 'error',
                          text: error instanceof Error ? error.message : 'Failed to open subscription management'
                        });
                      } finally {
                        setManagingSubscription(false);
                      }
                    }}
                    disabled={managingSubscription}
                    className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white"
                  >
                    {managingSubscription ? "Loading..." : "Manage Subscription"}
                    <ExternalLink className="w-4 h-4 ml-2" />
                  </Button>
                </div>
              ) : subscriptionStatus?.status === 'active' ? (
                <div className="space-y-4">
                  <div className="p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-lg border border-amber-200">
                    <div className="flex items-center gap-2 mb-2">
                      <CheckCircle className="w-5 h-5 text-amber-600" />
                      <span className="font-semibold text-amber-900">Active Subscription</span>
                    </div>
                    {subscriptionStatus.current_period_end && (
                      <p className="text-sm text-amber-700">
                        Renews: {new Date(subscriptionStatus.current_period_end).toLocaleDateString()}
                      </p>
                    )}
                  </div>
                  <Button
                    onClick={async () => {
                      setManagingSubscription(true);
                      try {
                        const portalResult = await subscriptionService.createPortalSession(window.location.href);
                        if (portalResult.success && portalResult.url) {
                          window.location.href = portalResult.url;
                        }
                      } catch (error) {
                        setSaveMessage({
                          type: 'error',
                          text: error instanceof Error ? error.message : 'Failed to open subscription management'
                        });
                      } finally {
                        setManagingSubscription(false);
                      }
                    }}
                    disabled={managingSubscription}
                    className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white"
                  >
                    {managingSubscription ? "Loading..." : "Manage Subscription"}
                    <ExternalLink className="w-4 h-4 ml-2" />
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-lg border border-amber-200">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertCircle className="w-5 h-5 text-amber-600" />
                      <span className="font-semibold text-amber-900">No Active Subscription</span>
                    </div>
                    <p className="text-sm text-amber-700 mb-4">
                      Start your 7-day free trial to unlock all features
                    </p>
                  </div>
                  <Button
                    onClick={async () => {
                      setManagingSubscription(true);
                      try {
                        const checkoutResult = await subscriptionService.createCheckoutSession(
                          `${window.location.origin}/?subscription=success`,
                          `${window.location.origin}/?subscription=canceled`
                        );
                        if (checkoutResult.success && checkoutResult.checkout_url) {
                          window.location.href = checkoutResult.checkout_url;
                        }
                      } catch (error) {
                        setSaveMessage({
                          type: 'error',
                          text: error instanceof Error ? error.message : 'Failed to start checkout'
                        });
                      } finally {
                        setManagingSubscription(false);
                      }
                    }}
                    disabled={managingSubscription}
                    className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white"
                  >
                    {managingSubscription ? "Loading..." : "Start Free Trial"}
                    <ArrowRight className="w-5 h-5 ml-2" />
                  </Button>
                </div>
              )}
            </Card>

            {/* Save Button */}
            <div className="flex justify-end gap-4 items-center">
              {saveMessage && (
                <div className={`flex items-center gap-2 px-4 py-2 rounded-md ${
                  saveMessage.type === 'success' 
                    ? 'bg-green-50 text-green-700 border border-green-200' 
                    : 'bg-red-50 text-red-700 border border-red-200'
                }`}>
                  {saveMessage.type === 'success' ? (
                    <CheckCircle className="w-4 h-4" />
                  ) : (
                    <AlertCircle className="w-4 h-4" />
                  )}
                  <span className="text-sm">{saveMessage.text}</span>
                </div>
              )}
              <Button 
                onClick={handleSave}
                disabled={saving || loading}
                className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white shadow-lg px-8 py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {saving ? "Saving..." : "Save Changes"}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
