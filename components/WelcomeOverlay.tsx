import { Button } from "./ui/button";
import { Sparkles, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import { ImageWithFallback } from "./figma/ImageWithFallback";

interface WelcomeOverlayProps {
  onGetStarted: () => void;
}

export function WelcomeOverlay({ onGetStarted }: WelcomeOverlayProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-6"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
        className="bg-[#F5F1E8] rounded-2xl shadow-2xl max-w-4xl w-full overflow-hidden"
      >
        <div className="grid md:grid-cols-2 gap-8 p-12">
          {/* Left side - Content */}
          <div className="text-center md:text-left flex flex-col justify-center">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.4 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#F4E4C1] mb-6 self-center md:self-start"
            >
              <Sparkles className="w-4 h-4 text-[#C66E2F]" />
              <span className="text-[#C66E2F] text-sm">AI-Powered Networking Assistant</span>
            </motion.div>

            {/* Heading */}
            <motion.h1
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.4 }}
              className="text-4xl md:text-5xl text-stone-900 mb-2"
            >
              Type your dream role.
            </motion.h1>
            <motion.h2
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.35, duration: 0.4 }}
              className="text-4xl md:text-5xl text-[#E07E2F] mb-6"
            >
              Get real conversations started.
            </motion.h2>

            {/* Description */}
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.4 }}
              className="text-lg text-stone-700 mb-8 leading-relaxed"
            >
              CoffeeChat AI helps students and professionals turn interest into action.
              Find the right people, craft personalized emails, and build meaningful
              connections.
            </motion.p>

            {/* CTA Button */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.4 }}
              className="self-center md:self-start"
            >
              <Button
                onClick={onGetStarted}
                className="bg-[#E07E2F] hover:bg-[#C66E2F] text-white text-lg px-8 py-6 rounded-xl shadow-lg"
              >
                Get Started Free
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </motion.div>
          </div>

          {/* Right side - Preview Image */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="hidden md:flex items-center justify-center"
          >
            <div className="relative w-full rounded-xl overflow-hidden shadow-lg">
              <ImageWithFallback
                src="https://images.unsplash.com/photo-1623278132336-bd316c0f9c78?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjaGF0JTIwaW50ZXJmYWNlJTIwbGFwdG9wfGVufDF8fHx8MTc2MDc1NjY0MXww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                alt="Chat interface preview"
                className="w-full h-full object-cover rounded-xl"
              />
            </div>
          </motion.div>
        </div>
      </motion.div>
    </motion.div>
  );
}