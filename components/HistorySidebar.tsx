import { ScrollArea } from "./ui/scroll-area";
import { Button } from "./ui/button";
import { MessageSquare, Plus, Clock } from "lucide-react";

interface ChatHistory {
  id: string;
  title: string;
  timestamp: string;
  preview: string;
}

interface HistorySidebarProps {
  history: ChatHistory[];
  currentChatId?: string;
  onSelectChat: (id: string) => void;
  onNewChat: () => void;
}

export function HistorySidebar({
  history,
  currentChatId,
  onSelectChat,
  onNewChat,
}: HistorySidebarProps) {
  return (
    <div className="w-72 bg-gradient-to-br from-white via-amber-50 to-orange-50 border-r border-amber-200 flex flex-col h-screen">
      <div className="p-6 border-b border-amber-200">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
            <MessageSquare className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-lg font-bold bg-gradient-to-r from-amber-700 via-orange-600 to-amber-600 bg-clip-text text-transparent">CoffeeChat AI</h2>
        </div>
        <Button
          onClick={onNewChat}
          className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white shadow-lg font-semibold"
        >
          <Plus className="w-4 h-4 mr-2" />
          New Conversation
        </Button>
      </div>

      <ScrollArea className="flex-1">
        <div className="p-4 space-y-2">
          {history.length === 0 ? (
            <div className="text-center py-12 text-amber-600">
              <Clock className="w-12 h-12 mx-auto mb-4 opacity-60" />
              <p className="text-sm font-medium">No chat history yet</p>
            </div>
          ) : (
            history.map((chat) => (
              <button
                key={chat.id}
                onClick={() => onSelectChat(chat.id)}
                className={`w-full text-left p-4 rounded-xl transition-all duration-300 ${
                  currentChatId === chat.id
                    ? 'bg-gradient-to-r from-amber-100 to-orange-100 shadow-lg border border-amber-300'
                    : 'hover:bg-gradient-to-r hover:from-amber-50 hover:to-orange-50 hover:shadow-md'
                }`}
              >
                <h3 className="text-sm text-amber-900 font-semibold mb-2 truncate">
                  {chat.title}
                </h3>
                <p className="text-xs text-amber-700 truncate mb-2">{chat.preview}</p>
                <p className="text-xs text-amber-600 font-medium">{chat.timestamp}</p>
              </button>
            ))
          )}
        </div>
      </ScrollArea>

      <div className="p-6 border-t border-amber-200 text-xs text-amber-700 bg-gradient-to-r from-amber-50 to-orange-50">
        <p className="font-semibold mb-1">💬 Type your dream role.</p>
        <p className="font-medium">Get real conversations started.</p>
      </div>
    </div>
  );
}
