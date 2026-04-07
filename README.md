# ☕ CoffeeChat AI

**Your AI-powered networking assistant** that helps students and professionals connect with industry contacts by generating personalized outreach emails.

Repository: [CoffeeChatAIFrontend](https://github.com/PranavNarayanan347/CoffeeChatAIFrontend) (frontend app; backend may live under `backend/` in this workspace).

## 🎨 Features

- **AI-Powered Email Generation** - Type your dream role and get personalized email drafts
- **Resume-Based Personalization** - Upload your resume to extract talking points
- **Chat Interface** - Natural conversation flow with AI assistant
- **Email Preview & Export** - Review and send drafts directly to Gmail
- **Chat History** - Track all your networking conversations
- **Profile Management** - Update resume and preferences anytime

## 🚀 Tech Stack

- **Frontend Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui + Radix UI
- **Routing**: React Router v6
- **Icons**: Lucide React
- **Animations**: Motion (Framer Motion)
- **Charts**: Recharts
- **Notifications**: Sonner

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PranavNarayanan347/CoffeeChatAIFrontend.git
   cd CoffeeChatAIFrontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

5. **Preview production build**
   ```bash
   npm run preview
   ```

## 📁 Project Structure

```
CoffeeChatAIFrontend/
├── components/          # React components
│   ├── ui/             # shadcn/ui components
│   └── ...             # Core app components
├── pages/              # Route pages
│   ├── Landing.tsx     # Landing page
│   ├── Login.tsx       # Authentication
│   ├── Chat.tsx        # Main chat interface
│   └── Profile.tsx     # User profile
├── styles/             # Global styles
│   └── globals.css     # Tailwind + custom CSS
├── App.tsx             # Main app component with routing
├── main.tsx            # React entry point
└── index.html          # HTML entry point
```

## 🎨 Design System

CoffeeChat AI uses a warm, professional color palette:

- **Primary**: Amber/Orange gradient (`from-amber-400 to-orange-500`)
- **Neutral**: Stone tones for backgrounds and text
- **Accent**: Beige and caramel brown for depth

## 🔧 Development

### Available Scripts

- `npm run dev` - Start development server (port 3000)
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Key Components

- **ChatInterface** - Main chat UI with message handling
- **EmailPreviewCard** - Preview generated emails
- **HistorySidebar** - Chat history navigation
- **OnboardingResumeUpload** - Resume upload flow
- **WelcomeOverlay** - First-time user experience

## 🌐 Deployment

Build the project and deploy the `dist` folder to any static hosting service:

- Vercel
- Netlify
- GitHub Pages
- Cloudflare Pages

## 📄 License

This project is proprietary software.

## 🤝 Contributing

This is a private project. For any questions, please contact the project maintainer.

---

**Made with ☕ and AI**
