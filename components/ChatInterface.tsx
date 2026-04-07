import { useState, useRef, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Send, Sparkles } from "lucide-react";
import { ChatMessage } from "./ChatMessage";
import { TypingIndicator } from "./TypingIndicator";
import { EmailPreviewCard } from "./EmailPreviewCard";
import { PeopleList } from "./PeopleList";
import { apiService, Person } from "../services/api";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
  people?: Person[];
  emailData?: {
    recipient: string;
    subject: string;
    body: string;
    matchedContact: {
      name: string;
      role: string;
      company: string;
    };
  };
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hi! I'm CoffeeChat AI ☕\n\nTell me what role or company you're interested in, and I'll help you find the right people to connect with and draft personalized outreach emails.\n\nTry something like:\n• \"I want to chat with a Product Manager at Google\"\n• \"Find someone from Deloitte's AI team\"\n• \"Connect me with a software engineer at Netflix\"\n\nAfter generating an email, you can also update it by saying things like:\n• \"Make it more casual\"\n• \"Add that we're both USC alumni\"\n• \"Make it shorter\"",
      isUser: false,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [lastEmailData, setLastEmailData] = useState<Message['emailData'] | null>(null);
  const [lastPersonInfo, setLastPersonInfo] = useState<Person | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const generateResponse = async (userMessage: string): Promise<Message[]> => {
    try {
      // Call the backend API
      const response = await apiService.chat(userMessage);
      
      if (!response.success) {
        return [
          {
            id: Date.now().toString(),
            text: `Sorry, I encountered an error: ${response.error || 'Unknown error'}`,
            isUser: false,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          }
        ];
      }

      // Handle case where no results are found
      if (response.count === 0) {
        const infoMessage = (response as any).info || 'No people found matching your criteria. Try adjusting your search terms.';
        return [
          {
            id: Date.now().toString(),
            text: infoMessage,
            isUser: false,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          }
        ];
      }

      const messages: Message[] = [
        {
          id: Date.now().toString(),
          text: `Great! I found ${response.count} people matching your criteria. Here they are:`,
          isUser: false,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          people: response.search_results,
        }
      ];

      return messages;
    } catch (error) {
      console.error('Error generating response:', error);
      return [
        {
          id: Date.now().toString(),
          text: `Sorry, I'm having trouble connecting to the backend. Please make sure the server is running on http://localhost:5000`,
          isUser: false,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        }
      ];
    }
  };

  const handleGenerateEmail = async (person: Person) => {
    try {
      setIsTyping(true);
      
      // Generate email for the selected person
      const emailResponse = await apiService.generateEmail(person, 'cold_outreach', '');
      
      if (emailResponse.success) {
        const emailMessage: Message = {
          id: Date.now().toString(),
          text: `✨ I've generated a personalized email for ${person.name}!`,
          isUser: false,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          emailData: {
            recipient: person.work_email !== 'N/A' ? person.work_email : person.personal_email,
            subject: "Coffee chat opportunity?",
            body: emailResponse.email_content,
            matchedContact: {
              name: person.name,
              role: person.title,
              company: person.company,
            },
          },
        };
        
        setMessages((prev) => [...prev, emailMessage]);
        // Store the email data and person info for potential updates
        setLastEmailData(emailMessage.emailData);
        setLastPersonInfo(person);
      } else {
        const errorMessage: Message = {
          id: Date.now().toString(),
          text: `Sorry, I couldn't generate an email: ${emailResponse.error}`,
          isUser: false,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error generating email:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: "Sorry, I encountered an error while generating the email.",
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleUpdateEmail = async (updateInstructions: string) => {
    if (!lastEmailData || !lastPersonInfo) {
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: "I don't have a previous email to update. Please generate an email first.",
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMessage]);
      return;
    }

    try {
      setIsTyping(true);
      
      // Update the email based on user instructions
      const updateResponse = await apiService.updateEmail(
        lastEmailData.body,
        lastPersonInfo,
        updateInstructions,
        'cold_outreach'
      );
      
      if (updateResponse.success) {
        const updatedEmailData = {
          ...lastEmailData,
          body: updateResponse.updated_email,
        };
        
        const updateMessage: Message = {
          id: Date.now().toString(),
          text: `✨ I've updated the email for ${lastPersonInfo.name} based on your instructions!`,
          isUser: false,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          emailData: updatedEmailData,
        };
        
        setMessages((prev) => [...prev, updateMessage]);
        setLastEmailData(updatedEmailData);
      } else {
        const errorMessage: Message = {
          id: Date.now().toString(),
          text: `Sorry, I couldn't update the email: ${updateResponse.error}`,
          isUser: false,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error updating email:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: "Sorry, I encountered an error while updating the email.",
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const isEmailUpdateCommand = (message: string): boolean => {
    const updateKeywords = [
      'update', 'change', 'modify', 'edit', 'revise', 'make it', 'add', 'remove', 
      'shorten', 'longer', 'more casual', 'more formal', 'tone', 'style'
    ];
    const lowerMessage = message.toLowerCase();
    return updateKeywords.some(keyword => lowerMessage.includes(keyword)) && lastEmailData !== null;
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      isUser: true,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);
    const userInput = input;
    setInput("");
    setIsTyping(true);

    try {
      // Check if this is an email update command
      if (isEmailUpdateCommand(userInput)) {
        await handleUpdateEmail(userInput);
      } else {
        // Regular search or new request
        const responses = await generateResponse(userInput);
        setIsTyping(false);
        
        // Add responses with a slight delay for better UX
        for (let i = 0; i < responses.length; i++) {
          setTimeout(() => {
            setMessages((prev) => [...prev, responses[i]]);
          }, i * 1000); // 1 second delay between messages
        }
      }
    } catch (error) {
      console.error('Error in handleSend:', error);
      setIsTyping(false);
      setMessages((prev) => [...prev, {
        id: Date.now().toString(),
        text: "Sorry, I encountered an error. Please try again.",
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-gradient-to-br from-white via-amber-50 to-orange-50">
      {/* Header */}
      <div className="border-b border-amber-200 px-6 py-6 flex-shrink-0 bg-gradient-to-r from-white/95 to-amber-50/95 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center  grshadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-amber-700 via-orange-600 to-amber-600 bg-clip-text text-transparent">CoffeeChat AI</h1>
            <p className="text-sm text-amber-700 font-medium">
              Your AI networking assistant
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-8" ref={scrollRef}>
        <div className="max-w-3xl mx-auto">
          {messages.map((message) => (
            <div key={message.id}>
              <ChatMessage
                message={message.text}
                isUser={message.isUser}
                timestamp={message.timestamp}
              />
              {message.people && (
                <div className="mb-6 ml-14">
                  <PeopleList
                    people={message.people}
                    onGenerateEmail={handleGenerateEmail}
                  />
                </div>
              )}
              {message.emailData && (
                <div className="mb-6 ml-14">
                  <EmailPreviewCard
                    recipient={message.emailData.recipient}
                    subject={message.emailData.subject}
                    body={message.emailData.body}
                    matchedContact={message.emailData.matchedContact}
                    onSendToDrafts={() => {
                      console.log("Email sent to Gmail drafts successfully!");
                    }}
                  />
                </div>
              )}
            </div>
          ))}
          {isTyping && <TypingIndicator />}
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-amber-200 p-6 bg-gradient-to-r from-amber-50/95 to-orange-50/95 backdrop-blur-md flex-shrink-0">
        <div className="max-w-3xl mx-auto flex gap-3">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your dream role or company..."
            className="flex-1 bg-white/90 border-amber-300 focus:border-amber-500 focus:ring-amber-500 shadow-lg backdrop-blur-sm hover:bg-white transition-all duration-300"
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim()}
            className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white shadow-lg px-6 hover:shadow-xl transition-all duration-300 hover:scale-105"
          >
            <Send className="w-5 h-5" />
          </Button>
        </div>
        <p className="text-xs text-amber-600 text-center mt-3 font-medium">
          Try: "I want to chat with a Product Manager at Google"
        </p>
      </div>
    </div>
  );
}
