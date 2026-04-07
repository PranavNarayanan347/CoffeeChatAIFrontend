import { Avatar } from "./ui/avatar";
import { Coffee, User } from "lucide-react";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
}

export function ChatMessage({ message, isUser, timestamp }: ChatMessageProps) {
  return (
    <div className={`flex gap-4 mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center flex-shrink-0 shadow-lg">
          <Coffee className="w-5 h-5 text-white" />
        </div>
      )}
      <div className={`max-w-[75%] ${isUser ? 'order-first' : ''}`}>
        <div
          className={`rounded-2xl px-6 py-4 shadow-lg ${
            isUser
              ? 'bg-gradient-to-r from-amber-500 to-orange-600 text-white'
              : 'bg-gradient-to-br from-white to-amber-50 text-amber-900 border border-amber-200'
          }`}
        >
          <p className="whitespace-pre-wrap leading-relaxed">{message}</p>
        </div>
        {timestamp && (
          <p className={`text-xs mt-2 px-3 ${isUser ? 'text-amber-600' : 'text-amber-600'}`}>{timestamp}</p>
        )}
      </div>
      {isUser && (
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-orange-500 to-amber-600 flex items-center justify-center flex-shrink-0 shadow-lg">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
}
