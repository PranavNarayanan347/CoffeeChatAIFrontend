import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { Coffee, Mail, Sparkles, Users, ArrowRight, CheckCircle } from "lucide-react";

interface LandingProps {
  onGetStarted: () => void;
}

export function Landing({ onGetStarted }: LandingProps) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-amber-50 via-white to-stone-50">
      {/* Navigation */}
      <nav className="border-b border-stone-200 bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
              <Coffee className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-amber-700 via-orange-600 to-amber-600 bg-clip-text text-transparent">
              CoffeeChat AI
            </span>
          </div>
          <Button
            onClick={onGetStarted}
            variant="outline"
            className="border-stone-300"
          >
            Sign In
          </Button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 pt-20 pb-16 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-100 text-amber-800 text-sm mb-6">
          <Sparkles className="w-4 h-4" />
          AI-Powered Networking Assistant
        </div>
        
        <h1 className="text-5xl md:text-6xl text-stone-900 mb-6 max-w-4xl mx-auto leading-tight">
          Type your dream role.
          <br />
          <span className="text-amber-600">Get real conversations started.</span>
        </h1>
        
        <p className="text-xl text-stone-600 mb-8 max-w-2xl mx-auto">
          CoffeeChat AI helps students and professionals turn interest into action. 
          Find the right people, craft personalized emails, and build meaningful connections.
        </p>
        
        <div className="flex gap-4 justify-center">
          <Button
            onClick={onGetStarted}
            className="bg-amber-600 hover:bg-amber-700 text-white text-lg px-8 py-6"
          >
            Start Free Trial
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
        </div>

        {/* Demo Preview */}
        <div className="mt-16 max-w-5xl mx-auto">
          <Card className="p-8 shadow-2xl border-stone-200 bg-white">
            <div className="aspect-video bg-gradient-to-br from-amber-50 to-stone-100 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <Coffee className="w-16 h-16 text-amber-600 mx-auto mb-4" />
                <p className="text-stone-600">
                  Chat interface preview
                </p>
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-gradient-to-br from-white via-amber-50 to-orange-50 py-20">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl font-bold bg-gradient-to-r from-amber-700 via-orange-600 to-amber-600 bg-clip-text text-transparent text-center mb-16">
            From interest to inbox in minutes
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="p-8 border-amber-200 bg-gradient-to-br from-white to-amber-50 hover:shadow-xl transition-all duration-300 group">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center mb-6 shadow-lg">
                <Coffee className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-amber-900 mb-4 group-hover:text-amber-800 transition-colors">
                Chat-Based Input
              </h3>
              <p className="text-amber-700 leading-relaxed">
                Simply tell our chatbot what company and position you're interested in. 
                Natural conversation, no forms to fill out.
              </p>
            </Card>

            <Card className="p-8 border-orange-200 bg-gradient-to-br from-white to-orange-50 hover:shadow-xl transition-all duration-300 group">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-orange-500 to-amber-600 flex items-center justify-center mb-6 shadow-lg">
                <Users className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-orange-900 mb-4 group-hover:text-orange-800 transition-colors">
                Smart Matching
              </h3>
              <p className="text-orange-700 leading-relaxed">
                AI finds relevant professionals based on role, company, and field. 
                Connect with recruiters, alumni, or employees.
              </p>
            </Card>

            <Card className="p-8 border-amber-200 bg-gradient-to-br from-white to-amber-50 hover:shadow-xl transition-all duration-300 group">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-amber-600 to-orange-600 flex items-center justify-center mb-6 shadow-lg">
                <Mail className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-amber-900 mb-4 group-hover:text-amber-800 transition-colors">
                Personalized Emails
              </h3>
              <p className="text-amber-700 leading-relaxed">
                Crafts authentic, conversational outreach emails. 
                Automatically placed in Gmail drafts, ready to send.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-gradient-to-br from-amber-50 via-orange-50 to-white py-20">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl font-bold bg-gradient-to-r from-amber-600 via-orange-600 to-amber-700 bg-clip-text text-transparent text-center mb-16">
            How it works
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="relative bg-gradient-to-br from-amber-50 to-orange-50 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-amber-200 hover:border-amber-300 group">
              <div className="absolute top-4 right-4 w-16 h-16 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                1
              </div>
              <div className="mb-4">
                <span className="text-sm font-medium text-amber-600 uppercase tracking-wide">STEP 1</span>
                <h3 className="text-xl font-bold text-amber-900 mt-2 group-hover:text-amber-800 transition-colors">Tell us your goal</h3>
              </div>
              <p className="text-amber-700 leading-relaxed">
                "I want to chat with a Product Manager at Google"
              </p>
              <div className="mt-4 w-full h-1 bg-gradient-to-r from-amber-400 to-orange-500 rounded-full opacity-60"></div>
            </div>

            {/* Step 2 */}
            <div className="relative bg-gradient-to-br from-orange-50 to-amber-50 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-orange-200 hover:border-orange-300 group">
              <div className="absolute top-4 right-4 w-16 h-16 bg-gradient-to-br from-orange-400 to-amber-600 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                2
              </div>
              <div className="mb-4">
                <span className="text-sm font-medium text-orange-600 uppercase tracking-wide">STEP 2</span>
                <h3 className="text-xl font-bold text-orange-900 mt-2 group-hover:text-orange-800 transition-colors">We find the right people</h3>
              </div>
              <p className="text-orange-700 leading-relaxed">
                Our AI matches you with relevant professionals who can help
              </p>
              <div className="mt-4 w-full h-1 bg-gradient-to-r from-orange-400 to-amber-600 rounded-full opacity-60"></div>
            </div>

            {/* Step 3 */}
            <div className="relative bg-gradient-to-br from-white to-amber-50 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-amber-200 hover:border-amber-300 group">
              <div className="absolute top-4 right-4 w-16 h-16 bg-gradient-to-br from-amber-500 to-orange-600 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                3
              </div>
              <div className="mb-4">
                <span className="text-sm font-medium text-amber-600 uppercase tracking-wide">STEP 3</span>
                <h3 className="text-xl font-bold text-amber-900 mt-2 group-hover:text-amber-800 transition-colors">Review & send your email</h3>
              </div>
              <p className="text-amber-700 leading-relaxed">
                Personalized draft appears in your Gmail, ready to send
              </p>
              <div className="mt-4 w-full h-1 bg-gradient-to-r from-amber-500 to-orange-600 rounded-full opacity-60"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="bg-gradient-to-br from-white via-amber-50 to-orange-50 py-20">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl font-bold bg-gradient-to-r from-amber-700 via-orange-600 to-amber-600 bg-clip-text text-transparent text-center mb-16">
            Built for students and early-career professionals
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <Card className="p-8 border-amber-200 bg-gradient-to-br from-white to-amber-50 hover:shadow-xl transition-all duration-300 group">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-amber-500 to-orange-500 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg">
                  <CheckCircle className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h4 className="text-amber-900 mb-2 font-semibold group-hover:text-amber-800 transition-colors">
                    Explore career paths
                  </h4>
                  <p className="text-amber-700 text-sm leading-relaxed">
                    Learn about industries and roles directly from people who work there
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-8 border-orange-200 bg-gradient-to-br from-white to-orange-50 hover:shadow-xl transition-all duration-300 group">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-amber-600 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg">
                  <CheckCircle className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h4 className="text-orange-900 mb-2 font-semibold group-hover:text-orange-800 transition-colors">
                    Expand your network
                  </h4>
                  <p className="text-orange-700 text-sm leading-relaxed">
                    Build meaningful connections with professionals in your field
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-8 border-amber-200 bg-gradient-to-br from-white to-amber-50 hover:shadow-xl transition-all duration-300 group">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-amber-600 to-orange-600 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg">
                  <CheckCircle className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h4 className="text-amber-900 mb-2 font-semibold group-hover:text-amber-800 transition-colors">
                    Get response-worthy emails
                  </h4>
                  <p className="text-amber-700 text-sm leading-relaxed">
                    No templates or spam. Authentic messages designed to start conversations
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-8 border-orange-200 bg-gradient-to-br from-white to-orange-50 hover:shadow-xl transition-all duration-300 group">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-orange-600 to-amber-700 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg">
                  <CheckCircle className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h4 className="text-orange-900 mb-2 font-semibold group-hover:text-orange-800 transition-colors">
                    Track your outreach
                  </h4>
                  <p className="text-orange-700 text-sm leading-relaxed">
                    Chat history helps you build consistent networking momentum
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="bg-gradient-to-br from-white via-amber-50 to-orange-50 py-20">
        <div className="max-w-4xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold bg-gradient-to-r from-amber-700 via-orange-600 to-amber-600 bg-clip-text text-transparent mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-xl text-stone-600">
              Start your free trial today. No credit card required.
            </p>
          </div>

          <Card className="max-w-md mx-auto p-8 border-amber-200 bg-gradient-to-br from-white to-amber-50 shadow-2xl hover:shadow-3xl transition-all duration-300">
            <div className="text-center mb-6">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-100 text-green-800 text-sm font-semibold mb-4">
                <CheckCircle className="w-4 h-4" />
                7-Day Free Trial
              </div>
              <div className="mb-4">
                <span className="text-5xl font-bold text-amber-900">$15</span>
                <span className="text-xl text-amber-700">/month</span>
              </div>
              <p className="text-stone-600 mb-6">
                After your 7-day free trial, continue for just $15/month
              </p>
            </div>

            <div className="space-y-4 mb-8">
              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <span className="text-stone-700">Unlimited people searches</span>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <span className="text-stone-700">AI-powered email generation</span>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <span className="text-stone-700">Gmail draft integration</span>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <span className="text-stone-700">Chat history & analytics</span>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <span className="text-stone-700">Resume parsing & talking points</span>
              </div>
            </div>

            <Button
              onClick={onGetStarted}
              className="w-full bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 text-white text-lg px-8 py-6 shadow-lg"
            >
              Start Free Trial
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
            <p className="text-xs text-center text-stone-500 mt-4">
              Cancel anytime. No hidden fees.
            </p>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-br from-amber-600 to-orange-600 py-20">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-4xl text-white mb-6">
            Ready to start networking?
          </h2>
          <p className="text-xl text-amber-50 mb-8">
            Join CoffeeChat AI and turn your career interests into real conversations.
          </p>
          <Button
            onClick={onGetStarted}
            className="bg-white text-amber-600 hover:bg-amber-50 text-lg px-8 py-6"
          >
            Start Free Trial
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-stone-900 text-stone-400 py-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center shadow-lg">
              <Coffee className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-amber-300 via-orange-400 to-amber-300 bg-clip-text text-transparent">
              CoffeeChat AI
            </span>
          </div>
          <p className="text-sm">
            Type your dream role. Get real conversations started.
          </p>
        </div>
      </footer>
    </div>
  );
}
