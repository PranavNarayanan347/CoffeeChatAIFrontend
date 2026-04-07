# CoffeeChat AI - Full Stack Application

A complete AI-powered networking assistant that helps you find the right people and generate personalized outreach emails, with seamless Gmail integration.

## 🚀 Features

- **AI-Powered People Search**: Find professionals by role, company, and location
- **Personalized Email Generation**: Create tailored outreach emails using OpenAI
- **Gmail Integration**: Automatically create drafts in your Gmail
- **Modern React Frontend**: Beautiful, responsive UI with real-time chat
- **Flask Backend**: Robust API with error handling and CORS support

## 🏗️ Architecture

```
Frontend (React + Vite)     Backend (Flask + Python)
├── Chat Interface         ├── People Search API
├── Email Preview          ├── Email Generation API  
├── Gmail Integration      ├── Gmail Draft API
└── Modern UI Components  └── AI Processing Engine
```

## 📋 Prerequisites

- **Python 3.7+** with pip
- **Node.js 16+** with npm
- **Google Cloud Account** (for Gmail API)
- **OpenAI API Key**
- **People Data Labs API Key**

## 🛠️ Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Setup

1. **Install Dependencies:**
   ```bash
   # Python dependencies
   pip install -r requirements.txt
   
   # Node.js dependencies
   npm install
   ```

2. **Configure API Keys:**
   - Add your OpenAI API key to `backend/services/ai_people_search.py`
   - Add your PDL API key to `backend/services/ai_people_search.py`
   - Set up Gmail API credentials (see docs/GMAIL_SETUP.md)

3. **Start Servers:**
   ```bash
   # Terminal 1: Backend
   python backend/app.py
   
   # Terminal 2: Frontend
   npm run dev
   ```

4. **Access Application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

## 🔧 API Endpoints

### Backend API (Flask)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/search-people` | POST | Search for people |
| `/api/generate-email` | POST | Generate personalized email |
| `/api/create-gmail-draft` | POST | Create Gmail draft |
| `/api/chat` | POST | Main chat endpoint |

### Example API Usage

```javascript
// Search for people
const response = await fetch('http://localhost:5000/api/search-people', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'Find me software engineers at Google' })
});

// Generate email
const emailResponse = await fetch('http://localhost:5000/api/generate-email', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    person_info: { name: 'John Doe', company: 'Google' },
    email_type: 'cold_outreach',
    custom_message: 'Interested in AI roles'
  })
});
```

## 📧 Gmail Integration Setup

1. **Google Cloud Console Setup:**
   - Create a new project
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download `credentials.json`

2. **First Run Authentication:**
   - Run the application
   - Try creating a Gmail draft
   - Browser will open for Google authentication
   - Grant permissions for Gmail access

3. **Troubleshooting:**
   - See `GMAIL_SETUP.md` for detailed instructions
   - Add your email as a test user in OAuth consent screen
   - Ensure `credentials.json` is in the project root

## 🎨 Frontend Components

### Key Components

- **ChatInterface**: Main chat UI with real-time messaging
- **EmailPreviewCard**: Email preview with Gmail integration
- **ChatMessage**: Individual message display
- **TypingIndicator**: Loading animation
- **Navigation**: App navigation and user management

### State Management

- React hooks for local state
- API service layer for backend communication
- Error handling and loading states
- Real-time UI updates

## 🔍 Backend Services

### Core Functions

- **People Search**: PDL API integration with AI parsing
- **Email Generation**: OpenAI-powered personalized emails
- **Gmail Integration**: OAuth 2.0 authentication and draft creation
- **Error Handling**: Comprehensive error management

### File Structure

```
backend/
├── app.py                 # Flask server
├── models.py              # Database models
├── auth.py                # Authentication utilities
├── services/
│   ├── ai_people_search.py    # Core AI functionality
│   ├── stripe_service.py      # Stripe integration
│   └── resume_parser.py       # Resume parsing
├── credentials.json       # Gmail API credentials
└── token.json            # Gmail auth tokens

frontend/
├── components/            # React components
├── services/             # API service layer
├── pages/                # Page components
└── package.json          # Node.js dependencies
```

## 🚨 Troubleshooting

### Common Issues

1. **"Backend connection failed"**
   - Ensure Flask server is running on port 5000
   - Check CORS configuration
   - Verify API endpoints are accessible

2. **"Gmail authentication failed"**
   - Check `credentials.json` exists
   - Verify OAuth consent screen setup
   - Add your email as test user

3. **"People search returns no results"**
   - Verify PDL API key is correct
   - Check API quota limits
   - Try different search terms

4. **"Email generation fails"**
   - Verify OpenAI API key
   - Check API quota and billing
   - Ensure internet connection

### Debug Mode

Enable debug logging:
```python
# In backend/app.py
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🔒 Security Notes

- Never commit API keys to version control
- Use environment variables for production
- Add `credentials.json` and `token.json` to `.gitignore`
- Implement rate limiting for production use
- Use HTTPS in production environment

## 📈 Production Deployment

### Backend (Flask)
- Use Gunicorn or similar WSGI server
- Set up reverse proxy (Nginx)
- Configure environment variables
- Enable HTTPS

### Frontend (React)
- Build for production: `npm run build`
- Serve static files
- Configure API endpoints for production
- Set up CDN for assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Check the troubleshooting section above
- Review `GMAIL_SETUP.md` for Gmail issues
- Open an issue on GitHub for bugs
- Contact support for API key issues

---

**Happy Networking! ☕🤝**




