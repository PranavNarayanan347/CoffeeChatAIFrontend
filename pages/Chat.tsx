import { useState, useEffect } from "react";
import { ChatInterface } from "../components/ChatInterface";
import { HistorySidebar } from "../components/HistorySidebar";
import { apiService } from "../services/api";

interface ChatHistory {
  id: string;
  title: string;
  timestamp: string;
  preview: string;
}

function formatTimestamp(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) {
    return "Just now";
  } else if (diffMins < 60) {
    return `${diffMins} ${diffMins === 1 ? "minute" : "minutes"} ago`;
  } else if (diffHours < 24) {
    return `${diffHours} ${diffHours === 1 ? "hour" : "hours"} ago`;
  } else if (diffDays === 1) {
    return "Yesterday";
  } else if (diffDays < 7) {
    return `${diffDays} days ago`;
  } else {
    return date.toLocaleDateString();
  }
}

function formatHistoryItem(email: {
  id: number;
  recipient_name: string | null;
  recipient_email: string;
  person_role: string | null;
  person_company: string | null;
  status: string;
  created_at: string;
}): ChatHistory {
  // Title: Role at Company (or recipient name if role/company not available)
  const title = email.person_role && email.person_company
    ? `${email.person_role} at ${email.person_company}`
    : email.recipient_name || email.recipient_email;

  // Preview: Action based on status
  const recipientName = email.recipient_name || email.recipient_email.split("@")[0];
  let preview = "";
  if (email.status === "draft_created") {
    preview = `Draft created for ${recipientName}`;
  } else if (email.status === "sent") {
    preview = `Connected with ${recipientName}`;
  } else if (email.status === "generated") {
    preview = `Email generated for ${recipientName}`;
  } else {
    preview = `Email for ${recipientName}`;
  }

  return {
    id: email.id.toString(),
    title,
    timestamp: formatTimestamp(email.created_at),
    preview,
  };
}

export function Chat() {
  const [chatHistory, setChatHistory] = useState<ChatHistory[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string>();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEmailHistory = async () => {
      try {
        setLoading(true);
        const response = await apiService.getUserEmails({ limit: 50 });
        if (response.success && response.emails) {
          const history = response.emails.map(formatHistoryItem);
          setChatHistory(history);
        }
      } catch (error) {
        console.error("Failed to fetch email history:", error);
        // Keep empty history on error
      } finally {
        setLoading(false);
      }
    };

    fetchEmailHistory();
  }, []);

  const handleNewChat = () => {
    setCurrentChatId(undefined);
    // In a real app, this would create a new chat session
  };

  const handleSelectChat = (id: string) => {
    setCurrentChatId(id);
    // In a real app, this would load the selected chat
  };

  return (
    <div className="flex h-screen bg-stone-50">
      <HistorySidebar
        history={chatHistory}
        currentChatId={currentChatId}
        onSelectChat={handleSelectChat}
        onNewChat={handleNewChat}
      />
      <ChatInterface />
    </div>
  );
}
