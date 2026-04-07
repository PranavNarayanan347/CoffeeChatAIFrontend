# Gmail API Setup Guide

## Prerequisites
1. Python 3.7+
2. Google account with Gmail access
3. Google Cloud Console access

## Step-by-Step Setup

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name (e.g., "CoffeeChat AI")
4. Click "Create"

### 2. Enable Gmail API
1. In your project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on "Gmail API" → "Enable"

### 3. Create OAuth 2.0 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - Choose "External" user type
   - Fill in app name: "CoffeeChat AI"
   - Add your email as developer contact
   - Add scopes: `https://www.googleapis.com/auth/gmail.compose`
   - Add test users (your email)
4. Choose "Desktop application" as application type
5. Name it "CoffeeChat AI Desktop"
6. Click "Create"

### 4. Download Credentials
1. Click the download button (⬇️) next to your OAuth client
2. Save the file as `credentials.json` in your project directory

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. First Run Authentication
1. Run the script: `python backend/services/ai_people_search.py`
2. When prompted for Gmail draft creation, it will open a browser
3. Sign in with your Google account
4. Grant permissions for Gmail access
5. The script will save authentication tokens for future use

## Troubleshooting

### "credentials.json not found"
- Make sure you downloaded the OAuth client credentials file
- Rename it to exactly `credentials.json`
- Place it in the project root directory (or backend/ directory)

### "Access blocked" error
- Make sure you added your email as a test user in OAuth consent screen
- If using a Google Workspace account, contact your admin

### "Invalid scope" error
- Ensure Gmail API is enabled in your project
- Check that the scope `https://www.googleapis.com/auth/gmail.compose` is added

## Security Notes
- Never commit `credentials.json` or `token.json` to version control
- These files contain sensitive authentication information
- Add them to `.gitignore` if using Git

## File Structure After Setup
```
your-project/
├── backend/
│   ├── services/
│   │   └── ai_people_search.py
├── credentials.json          # OAuth client credentials
├── token.json               # Auto-generated auth tokens
├── requirements.txt
└── README.md
```




