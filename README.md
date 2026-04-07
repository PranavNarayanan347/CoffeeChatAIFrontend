# CoffeeChatAI — Frontend

> AI-powered platform for meaningful professional coffee chats. Match, connect, and converse.

![React](https://img.shields.io/badge/React-0d2137?style=flat&logo=react&logoColor=58a6ff)
![Next.js](https://img.shields.io/badge/Next.js-0d2137?style=flat&logo=nextdotjs&logoColor=58a6ff)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-0d2137?style=flat&logo=tailwindcss&logoColor=58a6ff)
![TypeScript](https://img.shields.io/badge/TypeScript-0d2137?style=flat&logo=typescript&logoColor=58a6ff)

---

## What This Is

CoffeeChatAI is a networking platform that uses AI to match users for 1:1 coffee chats — removing the friction from cold outreach and making meaningful professional connections easier to find and start.

This repo is the frontend.

---

## Features

- 🤝 AI-powered coffee chat matching
- 💬 Real-time messaging via WebSockets
- 🔐 Secure authentication (JWT / OAuth)
- 👤 User profiles with customizable settings
- 📱 Fully responsive — desktop, tablet, mobile

---

## Tech Stack

| Layer | Choice |
|---|---|
| Framework | React.js / Next.js |
| Styling | Tailwind CSS |
| State | Redux Toolkit / Zustand |
| Auth | JWT / OAuth |
| Realtime | Socket.io |
| HTTP | Axios |
| Build | Vite |

---

## Getting Started

**Prerequisites:** Node.js 16+, npm or yarn, Git

```bash
# Clone
git clone https://github.com/PranavNarayanan347/CoffeeChatAIFrontend.git
cd CoffeeChatAIFrontend

# Install
npm install

# Set up environment
cp .env.example .env.local
```

Configure `.env.local`:

```env
REACT_APP_API_URL=http://localhost:3001/api
REACT_APP_SOCKET_URL=http://localhost:3001
REACT_APP_GOOGLE_CLIENT_ID=your_google_client_id
REACT_APP_STRIPE_PUBLISHABLE_KEY=your_stripe_key
```

```bash
# Run
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/          # Page components
├── hooks/          # Custom React hooks
├── services/       # API services
├── store/          # State management
├── utils/          # Utility functions
├── styles/         # Global styles
└── types/          # TypeScript definitions
```

---

## Scripts

```bash
npm run dev          # Start dev server
npm run build        # Production build
npm run test         # Run tests
npm run lint         # ESLint
npm run type-check   # TypeScript check
```

---

## Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a pull request

Please follow the existing ESLint config, use Prettier for formatting, and add tests for new features.

---

## License

MIT — see [LICENSE](LICENSE) for details.
