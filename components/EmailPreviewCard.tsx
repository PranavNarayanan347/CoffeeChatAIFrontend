import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Mail, Send, Copy, Check } from "lucide-react";
import { useState } from "react";
import { apiService } from "../services/api";

interface EmailPreviewCardProps {
  recipient: string;
  subject: string;
  body: string;
  matchedContact?: {
    name: string;
    role: string;
    company: string;
  };
  onSendToDrafts?: () => void;
}

export function EmailPreviewCard({
  recipient,
  subject,
  body,
  matchedContact,
  onSendToDrafts,
}: EmailPreviewCardProps) {
  const [copied, setCopied] = useState(false);
  const [sent, setSent] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCopy = () => {
    navigator.clipboard.writeText(`Subject: ${subject}\n\n${body}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSend = async () => {
    if (recipient === 'N/A') {
      setError('No valid email address found for this person');
      return;
    }

    setSending(true);
    setError(null);

    try {
      const result = await apiService.createGmailDraft(recipient, subject, body);
      
      if (result.success) {
        setSent(true);
        onSendToDrafts?.();
      } else {
        setError(result.error || 'Failed to create Gmail draft');
      }
    } catch (error) {
      console.error('Error creating Gmail draft:', error);
      setError('Failed to connect to Gmail. Please check your credentials.');
    } finally {
      setSending(false);
    }
  };

  return (
    <Card className="p-6 bg-gradient-to-br from-white to-amber-50 border-amber-200 shadow-lg hover:shadow-xl transition-all duration-300">
      {matchedContact && (
        <div className="mb-6 pb-6 border-b border-amber-200">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center flex-shrink-0 shadow-lg">
              <span className="text-white font-semibold text-lg">
                {matchedContact.name.charAt(0)}
              </span>
            </div>
            <div>
              <h4 className="text-amber-900 font-semibold text-lg">{matchedContact.name}</h4>
              <p className="text-sm text-amber-700 font-medium">
                {matchedContact.role} at {matchedContact.company}
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="space-y-4 mb-6">
        <div>
          <label className="text-xs text-amber-600 font-medium block mb-2">To:</label>
          <p className="text-sm text-amber-900 font-medium">{recipient}</p>
        </div>
        <div>
          <label className="text-xs text-amber-600 font-medium block mb-2">Subject:</label>
          <p className="text-sm text-amber-900 font-medium">{subject}</p>
        </div>
        <div>
          <label className="text-xs text-amber-600 font-medium block mb-2">Message:</label>
          <div className="text-sm text-amber-800 bg-gradient-to-r from-orange-50 to-amber-50 rounded-xl p-4 whitespace-pre-wrap border border-amber-200 leading-relaxed">
            {body}
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      <div className="flex gap-3">
        <Button
          onClick={handleSend}
          disabled={sent || sending}
          className="flex-1 bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white shadow-lg"
        >
          {sending ? (
            <>
              <div className="w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Creating Draft...
            </>
          ) : sent ? (
            <>
              <Check className="w-4 h-4 mr-2" />
              Sent to Drafts
            </>
          ) : (
            <>
              <Send className="w-4 h-4 mr-2" />
              Send to Gmail Drafts
            </>
          )}
        </Button>
        <Button
          onClick={handleCopy}
          variant="outline"
          className="border-amber-300 text-amber-700 hover:bg-amber-50 hover:border-amber-400"
        >
          {copied ? (
            <Check className="w-4 h-4" />
          ) : (
            <Copy className="w-4 h-4" />
          )}
        </Button>
      </div>
    </Card>
  );
}
