import { useState } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Upload, FileText, Sparkles, CheckCircle, AlertCircle } from "lucide-react";
import { motion } from "framer-motion";
import { apiService } from "../services/api";
import { authService } from "../services/auth";

interface OnboardingResumeUploadProps {
  onComplete: (talkingPoints: string[], resumeFileName: string) => void;
  onSkip: () => void;
}

export function OnboardingResumeUpload({ onComplete, onSkip }: OnboardingResumeUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState("");

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    const validTypes = ['.pdf', '.doc', '.docx'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!validTypes.includes(fileExtension)) {
      setError("Please upload a PDF, DOC, or DOCX file");
      return;
    }

    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      setError("File size must be less than 5MB");
      return;
    }

    setFileName(file.name);
    setUploading(true);
    setError("");
    
    try {
      // Parse resume using API
      const result = await apiService.parseResume(file);
      
      if (result.success) {
        setUploaded(true);
        
        // Update auth service with new user data
        if (result.user) {
          authService.setUser(result.user);
        }
        
        // Auto-complete after a short delay
        setTimeout(() => {
          onComplete(result.talking_points || [], file.name);
        }, 1500);
      } else {
        throw new Error(result.error || "Failed to parse resume");
      }
    } catch (err) {
      setUploading(false);
      setError(err instanceof Error ? err.message : "Failed to upload resume. Please try again.");
      console.error("Resume upload error:", err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-stone-50 flex items-center justify-center p-6 overflow-y-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="max-w-2xl w-full my-8"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="w-20 h-20 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center mx-auto mb-6 shadow-lg"
          >
            {uploaded ? (
              <CheckCircle className="w-10 h-10 text-white" />
            ) : (
              <Upload className="w-10 h-10 text-white" />
            )}
          </motion.div>
          
          <motion.h1
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.4 }}
            className="text-4xl text-stone-900 mb-3"
          >
            {uploaded ? "Processing your resume..." : "Let's get you started"}
          </motion.h1>
          
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35, duration: 0.4 }}
            className="text-lg text-stone-600"
          >
            {uploaded 
              ? "Extracting your key talking points and achievements"
              : "Upload your resume and we'll extract talking points to strengthen your networking"}
          </motion.p>
        </div>

        {/* Upload Card */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.4 }}
        >
          <Card className="p-8 border-stone-200 bg-white shadow-xl">
            {!uploaded ? (
              <div>
                <div className="border-2 border-dashed border-stone-300 rounded-lg p-12 text-center hover:border-amber-400 transition-colors">
                  <div className="w-16 h-16 rounded-full bg-amber-100 flex items-center justify-center mx-auto mb-4">
                    <FileText className="w-8 h-8 text-amber-600" />
                  </div>
                  <h3 className="text-xl text-stone-900 mb-2">
                    Drop your resume here
                  </h3>
                  <p className="text-stone-600 mb-6">
                    or click to browse your files
                  </p>
                  <label htmlFor="onboarding-resume-upload">
                    <Button
                      className="bg-amber-600 hover:bg-amber-700 text-white"
                      disabled={uploading}
                      asChild
                    >
                      <span>
                        {uploading ? "Uploading..." : "Choose File"}
                      </span>
                    </Button>
                  </label>
                  <input
                    id="onboarding-resume-upload"
                    type="file"
                    accept=".pdf,.doc,.docx"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                  <p className="text-xs text-stone-500 mt-4">
                    PDF, DOC, or DOCX (Max 5MB)
                  </p>
                </div>

                {/* Benefits */}
                <div className="mt-6 space-y-3">
                  <div className="flex items-start gap-3">
                    <Sparkles className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-stone-700">
                      AI extracts your key achievements and experiences
                    </p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Sparkles className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-stone-700">
                      Get personalized talking points for networking emails
                    </p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Sparkles className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-stone-700">
                      Make your outreach more compelling and specific
                    </p>
                  </div>
                </div>

                {error && (
                  <div className="mt-4 flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
                    <AlertCircle className="w-4 h-4 flex-shrink-0" />
                    <span>{error}</span>
                  </div>
                )}

                <div className="mt-8 text-center">
                  <button
                    onClick={onSkip}
                    className="text-stone-500 hover:text-stone-700 text-sm"
                    disabled={uploading}
                  >
                    Skip for now
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.5 }}
                  className="mb-6"
                >
                  <div className="w-24 h-24 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center mx-auto mb-4">
                    <CheckCircle className="w-12 h-12 text-white" />
                  </div>
                  <p className="text-stone-900 mb-1">{fileName}</p>
                  <p className="text-sm text-stone-600">Successfully uploaded</p>
                </motion.div>

                <div className="flex items-center justify-center gap-2 text-amber-600">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  >
                    <Sparkles className="w-5 h-5" />
                  </motion.div>
                  <p className="text-sm">Analyzing your resume...</p>
                </div>
              </div>
            )}
          </Card>
        </motion.div>
      </motion.div>
    </div>
  );
}
