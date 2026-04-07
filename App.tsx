import { useState, useEffect, useCallback } from "react";
import { Landing } from "./pages/Landing";
import { Login } from "./pages/Login";
import { Chat } from "./pages/Chat";
import { Profile } from "./pages/Profile";
import { Admin } from "./pages/Admin";
import { Navigation } from "./components/Navigation";
import { WelcomeOverlay } from "./components/WelcomeOverlay";
import { OnboardingResumeUpload } from "./components/OnboardingResumeUpload";
import { authService, User } from "./services/auth";

type Page = "landing" | "login" | "onboarding" | "chat" | "profile" | "admin";

// Protected routes that require authentication
const PROTECTED_ROUTES: Page[] = ["onboarding", "chat", "profile", "admin"];

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>("landing");
  const [userEmail, setUserEmail] = useState<string>("");
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [showWelcome, setShowWelcome] = useState(false);
  const [hasCompletedOnboarding, setHasCompletedOnboarding] = useState(false);
  const [userTalkingPoints, setUserTalkingPoints] = useState<string[]>([]);
  const [resumeFileName, setResumeFileName] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

  // Check authentication status and validate token
  const checkAuth = useCallback(async () => {
    try {
      // Check if token exists in storage
      const hasToken = authService.isAuthenticated();
      
      if (hasToken) {
        // Validate token by fetching current user
        const user = await authService.getCurrentUser();
        if (user) {
          setCurrentUser(user);
          setUserEmail(user.email);
          setIsAuthenticated(true);
          return true;
        } else {
          // Token is invalid, clear auth
          setIsAuthenticated(false);
          setCurrentUser(null);
          authService.clearAuth();
          return false;
        }
      } else {
        setIsAuthenticated(false);
        setCurrentUser(null);
        return false;
      }
    } catch (error) {
      console.error("Auth check failed:", error);
      setIsAuthenticated(false);
      setCurrentUser(null);
      authService.clearAuth();
      return false;
    }
  }, []);

  // Initial auth check on mount
  useEffect(() => {
    const initializeAuth = async () => {
      const wasAuthenticated = await checkAuth();
      setIsLoading(false);
      
      // Check for Stripe redirect parameters
      const urlParams = new URLSearchParams(window.location.search);
      const subscriptionStatus = urlParams.get('subscription');
      
      if (subscriptionStatus === 'success') {
        // User completed Stripe checkout, redirect to onboarding
        if (wasAuthenticated) {
          setCurrentPage("onboarding");
          // Clean up URL
          window.history.replaceState({}, '', window.location.pathname);
          return;
        }
      } else if (subscriptionStatus === 'canceled') {
        // User canceled checkout, still allow them to proceed
        if (wasAuthenticated) {
          setCurrentPage("onboarding");
          // Clean up URL
          window.history.replaceState({}, '', window.location.pathname);
          return;
        }
      }
      
      // If authenticated and on public pages, redirect to chat
      if (wasAuthenticated && (currentPage === "landing" || currentPage === "login")) {
        setCurrentPage("chat");
      }
    };

    initializeAuth();
  }, []); // Only run on mount

  // Protect routes - redirect to login if accessing protected route without auth
  useEffect(() => {
    if (!isLoading && PROTECTED_ROUTES.includes(currentPage) && !isAuthenticated) {
      setCurrentPage("login");
    }
  }, [currentPage, isAuthenticated, isLoading]);

  // Redirect authenticated users away from login page
  useEffect(() => {
    if (!isLoading && isAuthenticated && currentPage === "login") {
      setCurrentPage("chat");
    }
  }, [isAuthenticated, isLoading, currentPage]);

  const handleLogin = async (email: string) => {
    // Get the current user from auth service (should be set after successful login)
    const user = authService.getUser();
    if (user) {
      setCurrentUser(user);
      setUserEmail(user.email);
      setIsAuthenticated(true);
      
      // Check if user has already uploaded a resume
      // Resume data is indicated by having bio, company, role, or linkedin_profile
      const hasResumeData = !!(user.bio || user.company || user.role || user.linkedin_profile);
      
      if (hasResumeData) {
        // User already has resume data, skip onboarding and go to chat
        setCurrentPage("chat");
      } else {
        // New users or users without resume data go to onboarding
        setCurrentPage("onboarding");
      }
    } else {
      // Fallback to email if user not in storage yet
      setUserEmail(email);
      // If we don't have user data, go to onboarding to be safe
      setCurrentPage("onboarding");
    }
  };

  const handleOnboardingComplete = (talkingPoints: string[], fileName: string) => {
    setUserTalkingPoints(talkingPoints);
    setResumeFileName(fileName);
    setHasCompletedOnboarding(true);
    setCurrentPage("chat");
    setShowWelcome(true);
  };

  const handleOnboardingSkip = () => {
    setHasCompletedOnboarding(true);
    setCurrentPage("chat");
    setShowWelcome(true);
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      // Clear all state regardless of API call success
      setUserEmail("");
      setCurrentUser(null);
      setIsAuthenticated(false);
      setHasCompletedOnboarding(false);
      setUserTalkingPoints([]);
      setResumeFileName("");
      setCurrentPage("landing");
    }
  };

  const handleNavigate = (page: "chat" | "profile" | "admin") => {
    // Only allow navigation if authenticated
    if (isAuthenticated) {
      // Check admin access for admin page
      if (page === "admin" && currentUser && !currentUser.is_admin) {
        setCurrentPage("chat");
        return;
      }
      setCurrentPage(page);
    } else {
      // Redirect to login if not authenticated
      setCurrentPage("login");
    }
  };

  // Handle navigation attempts - protect routes
  const handlePageChange = (page: Page) => {
    // Allow public routes
    if (page === "landing" || page === "login") {
      setCurrentPage(page);
      return;
    }

    // Protect other routes
    if (PROTECTED_ROUTES.includes(page)) {
      if (isAuthenticated) {
        setCurrentPage(page);
      } else {
        // Redirect to login if trying to access protected route
        setCurrentPage("login");
      }
    } else {
      setCurrentPage(page);
    }
  };

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-amber-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-stone-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Landing page - public
  if (currentPage === "landing") {
    // If authenticated, redirect to chat
    if (isAuthenticated) {
      return <Landing onGetStarted={() => handlePageChange("chat")} />;
    }
    return <Landing onGetStarted={() => handlePageChange("login")} />;
  }

  // Login page - public, but redirect if already authenticated
  if (currentPage === "login") {
    // If already authenticated, show loading while redirecting
    if (isAuthenticated) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-orange-50 flex items-center justify-center">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-amber-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-stone-600">Redirecting...</p>
          </div>
        </div>
      );
    }
    
    return (
      <Login
        onLogin={handleLogin}
        onBack={() => handlePageChange("landing")}
      />
    );
  }

  // Onboarding page - protected, requires authentication
  if (currentPage === "onboarding") {
    if (!isAuthenticated) {
      // Redirect to login if not authenticated
      handlePageChange("login");
      return null;
    }
    
    // Check if user already has resume data - if so, skip onboarding
    if (currentUser) {
      const hasResumeData = !!(currentUser.bio || currentUser.company || currentUser.role || currentUser.linkedin_profile);
      if (hasResumeData) {
        // User already has resume data, redirect to chat
        setCurrentPage("chat");
        return null;
      }
    }
    
    return (
      <OnboardingResumeUpload
        onComplete={handleOnboardingComplete}
        onSkip={handleOnboardingSkip}
      />
    );
  }

  // Authenticated pages with navigation - all require authentication
  if (!isAuthenticated) {
    // Redirect to login if not authenticated
    handlePageChange("login");
    return null;
  }

  return (
    <div className="h-screen flex flex-col">
      <Navigation
        currentPage={currentPage as "chat" | "profile" | "admin"}
        onNavigate={handleNavigate}
        onLogout={handleLogout}
        userEmail={userEmail}
        isAdmin={currentUser?.is_admin || false}
      />
      <div className="flex-1 overflow-auto">
        {currentPage === "chat" && <Chat />}
        {currentPage === "profile" && (
          <Profile 
            userEmail={userEmail}
            initialTalkingPoints={userTalkingPoints}
            initialResumeFileName={resumeFileName}
          />
        )}
        {currentPage === "admin" && <Admin />}
      </div>
      
      {/* Welcome overlay for new users */}
      {showWelcome && (
        <WelcomeOverlay onGetStarted={() => setShowWelcome(false)} />
      )}
    </div>
  );
}
