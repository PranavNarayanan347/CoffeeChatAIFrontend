import { Coffee } from "lucide-react";

export function TypingIndicator() {
  return (
    <div className="flex gap-4 mb-6">
      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center flex-shrink-0 shadow-lg">
        <Coffee className="w-5 h-5 text-white" />
      </div>
      <div className="bg-gradient-to-br from-white to-amber-50 rounded-2xl px-6 py-4 border border-amber-200 shadow-lg">
        <div className="flex gap-2">
          <div className="w-3 h-3 bg-gradient-to-r from-amber-500 to-orange-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-3 h-3 bg-gradient-to-r from-amber-500 to-orange-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <div className="w-3 h-3 bg-gradient-to-r from-amber-500 to-orange-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
}

