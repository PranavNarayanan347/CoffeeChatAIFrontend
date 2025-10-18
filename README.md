# CoffeeChatAI Frontend

A modern, responsive frontend application for CoffeeChatAI - an AI-powered coffee chat platform that facilitates meaningful conversations and connections.

## ðŸš€ Features

- **Modern UI/UX**: Clean, intuitive interface designed for seamless user experience
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Real-time Chat**: Live messaging capabilities with AI integration
- **User Authentication**: Secure login and registration system
- **Profile Management**: User profiles with customizable settings
- **Coffee Matching**: AI-powered coffee preference matching
- **Social Features**: Connect with other coffee enthusiasts

## ðŸ› ï¸ Tech Stack

- **Frontend Framework**: React.js / Next.js
- **Styling**: Tailwind CSS / Styled Components
- **State Management**: Redux Toolkit / Zustand
- **HTTP Client**: Axios / Fetch API
- **Authentication**: JWT / OAuth
- **Real-time Communication**: Socket.io / WebSockets
- **Build Tool**: Vite / Webpack
- **Package Manager**: npm / yarn

## ðŸ“‹ Prerequisites

Before running this project, make sure you have the following installed:

- Node.js (version 16.0 or higher)
- npm or yarn package manager
- Git

## ðŸš€ Getting Started

### Installation

1. Clone the repository:
`ash
git clone https://github.com/PranavNarayanan347/CoffeeChatAIFrontend.git
cd CoffeeChatAIFrontend
`

2. Install dependencies:
`ash
npm install
# or
yarn install
`

3. Create environment variables:
`ash
cp .env.example .env.local
`

4. Configure your environment variables in .env.local:
`env
REACT_APP_API_URL=http://localhost:3001/api
REACT_APP_SOCKET_URL=http://localhost:3001
REACT_APP_GOOGLE_CLIENT_ID=your_google_client_id
REACT_APP_STRIPE_PUBLISHABLE_KEY=your_stripe_key
`

### Development

Start the development server:
`ash
npm run dev
# or
yarn dev
`

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Building for Production

`ash
npm run build
# or
yarn build
`

## ðŸ“ Project Structure

`
CoffeeChatAIFrontend/
â”œâ”€â”€ public/                 # Static assets
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ components/        # Reusable UI components
â”‚   â”œâ”€â”€ pages/            # Page components
â”‚   â”œâ”€â”€ hooks/            # Custom React hooks
â”‚   â”œâ”€â”€ services/         # API services
â”‚   â”œâ”€â”€ store/            # State management
â”‚   â”œâ”€â”€ utils/            # Utility functions
â”‚   â”œâ”€â”€ styles/           # Global styles
â”‚   â””â”€â”€ types/            # TypeScript type definitions
â”œâ”€â”€ .env.example          # Environment variables template
â”œâ”€â”€ .gitignore           # Git ignore rules
â”œâ”€â”€ package.json         # Project dependencies
â””â”€â”€ README.md           # Project documentation
`

## ðŸŽ¨ Design System

The project follows a consistent design system with:

- **Color Palette**: Coffee-inspired warm tones
- **Typography**: Modern, readable fonts
- **Components**: Reusable UI components
- **Icons**: Consistent iconography
- **Spacing**: Standardized spacing scale

## ðŸ”§ Available Scripts

- 
pm run dev - Start development server
- 
pm run build - Build for production
- 
pm run test - Run tests
- 
pm run lint - Run ESLint
- 
pm run type-check - Run TypeScript type checking

## ðŸ¤ Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

### Code Style

- Follow ESLint configuration
- Use Prettier for code formatting
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

## ðŸ“ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ðŸ†˜ Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/PranavNarayanan347/CoffeeChatAIFrontend/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## ðŸ”— Links

- [Live Demo](https://coffeechat-ai.vercel.app)
- [Backend Repository](https://github.com/PranavNarayanan347/CoffeeChatAIBackend)
- [Documentation](https://docs.coffeechat-ai.com)

## ðŸ™ Acknowledgments

- Coffee community for inspiration
- Open source contributors
- Design inspiration from modern coffee shops

---

**Happy Coding! â˜•ï¸**
