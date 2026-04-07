import { Coffee, MessageSquare, User, LogOut, Shield } from "lucide-react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { useEffect, useState } from "react";
import { subscriptionService } from "../services/subscription";

interface NavigationProps {
  currentPage: "chat" | "profile" | "admin";
  onNavigate: (page: "chat" | "profile" | "admin") => void;
  onLogout: () => void;
  userEmail: string;
  isAdmin?: boolean;
}

export function Navigation({ currentPage, onNavigate, onLogout, userEmail, isAdmin = false }: NavigationProps) {
  const [subscriptionStatus, setSubscriptionStatus] = useState<'none' | 'trial' | 'active' | 'expired' | 'canceled'>('none');
  const [loadingStatus, setLoadingStatus] = useState(true);

  useEffect(() => {
    const loadSubscriptionStatus = async () => {
      try {
        const status = await subscriptionService.getSubscriptionStatus();
        if (status && status.success !== false) {
          setSubscriptionStatus(status.status);
        } else {
          // Default to 'none' if API returns error
          setSubscriptionStatus('none');
        }
      } catch (error) {
        console.error("Failed to load subscription status:", error);
        // Default to 'none' on error so UI doesn't break
        setSubscriptionStatus('none');
      } finally {
        setLoadingStatus(false);
      }
    };

    loadSubscriptionStatus();
  }, []);

  const getStatusBadge = () => {
    if (loadingStatus) return null;
    
    if (subscriptionStatus === 'trial') {
      return (
        <Badge className="bg-gradient-to-r from-green-500 to-emerald-600 text-white border-0 shadow-md">
          Trial
        </Badge>
      );
    } else if (subscriptionStatus === 'active') {
      return (
        <Badge className="bg-gradient-to-r from-amber-500 to-orange-500 text-white border-0 shadow-md">
          Active
        </Badge>
      );
    } else if (subscriptionStatus === 'expired' || subscriptionStatus === 'canceled') {
      return (
        <Badge variant="outline" className="border-amber-300 text-amber-700">
          Expired
        </Badge>
      );
    }
    return null;
  };

  return (
    <div className="bg-gradient-to-r from-white via-amber-50/30 to-orange-50/30 border-b border-amber-200 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
              <Coffee className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-amber-700 via-orange-600 to-amber-600 bg-clip-text text-transparent">
              CoffeeChat AI
            </span>
          </div>
          
          <nav className="flex gap-2">
            <Button
              variant="ghost"
              onClick={() => onNavigate("chat")}
              className={`px-4 py-2 rounded-xl transition-all duration-300 ${
                currentPage === "chat" 
                  ? "bg-gradient-to-r from-amber-100 to-orange-100 text-amber-900 shadow-md border border-amber-200" 
                  : "text-amber-700 hover:bg-gradient-to-r hover:from-amber-50 hover:to-orange-50 hover:text-amber-900"
              }`}
            >
              <div className={`w-5 h-5 mr-2 ${
                currentPage === "chat" 
                  ? "text-amber-600" 
                  : "text-amber-500"
              }`}>
                <MessageSquare className="w-full h-full" />
              </div>
              <span className="font-semibold">Chat</span>
            </Button>
            <Button
              variant="ghost"
              onClick={() => onNavigate("profile")}
              className={`px-4 py-2 rounded-xl transition-all duration-300 ${
                currentPage === "profile" 
                  ? "bg-gradient-to-r from-amber-100 to-orange-100 text-amber-900 shadow-md border border-amber-200" 
                  : "text-amber-700 hover:bg-gradient-to-r hover:from-amber-50 hover:to-orange-50 hover:text-amber-900"
              }`}
            >
              <div className={`w-5 h-5 mr-2 ${
                currentPage === "profile" 
                  ? "text-amber-600" 
                  : "text-amber-500"
              }`}>
                <User className="w-full h-full" />
              </div>
              <span className="font-semibold">Profile</span>
            </Button>
            {isAdmin && (
              <Button
                variant="ghost"
                onClick={() => onNavigate("admin")}
                className={`px-4 py-2 rounded-xl transition-all duration-300 ${
                  currentPage === "admin" 
                    ? "bg-gradient-to-r from-purple-100 to-purple-100 text-purple-900 shadow-md border border-purple-200" 
                    : "text-purple-700 hover:bg-gradient-to-r hover:from-purple-50 hover:to-purple-50 hover:text-purple-900"
                }`}
              >
                <div className={`w-5 h-5 mr-2 ${
                  currentPage === "admin" 
                    ? "text-purple-600" 
                    : "text-purple-500"
                }`}>
                  <Shield className="w-full h-full" />
                </div>
                <span className="font-semibold">Admin</span>
              </Button>
            )}
          </nav>
        </div>

        <div className="flex items-center gap-4">
          {getStatusBadge()}
          <span className="text-sm text-amber-700 font-medium hidden sm:block bg-gradient-to-r from-amber-50 to-orange-50 px-3 py-1 rounded-lg border border-amber-200">
            {userEmail}
          </span>
          <Button
            variant="ghost"
            size="sm"
            onClick={onLogout}
            className="text-amber-700 hover:text-amber-900 hover:bg-gradient-to-r hover:from-amber-50 hover:to-orange-50 px-3 py-2 rounded-xl transition-all duration-300 font-semibold"
          >
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>
      </div>
    </div>
  );
}
