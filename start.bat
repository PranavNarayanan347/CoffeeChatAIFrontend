@echo off
REM CoffeeChat AI - Full Stack Startup Script for Windows

echo 🚀 Starting CoffeeChat AI Full Stack Application...
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
npm install

REM Check if credentials.json exists
if not exist "credentials.json" (
    echo ⚠️  WARNING: Gmail credentials.json not found!
    echo    Gmail draft creation will not work until credentials are set up.
    echo    See docs\GMAIL_SETUP.md for instructions.
    echo.
)

echo 🔧 Starting Backend Server (Flask)...
start "CoffeeChat Backend" cmd /k "python backend\app.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

echo 🎨 Starting Frontend Server (Vite)...
start "CoffeeChat Frontend" cmd /k "npm run dev"

echo.
echo ✅ Both servers are starting up!
echo.
echo 🌐 Frontend: http://localhost:5173
echo 🔧 Backend API: http://localhost:5000
echo.
echo 📧 Gmail Integration: Ready (if credentials.json is configured)
echo.
echo Press any key to exit...
pause >nul




