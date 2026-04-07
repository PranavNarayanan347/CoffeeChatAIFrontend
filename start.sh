#!/bin/bash

# CoffeeChat AI - Full Stack Startup Script

echo "🚀 Starting CoffeeChat AI Full Stack Application..."
echo "=" * 50

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Check if credentials.json exists
if [ ! -f "credentials.json" ]; then
    echo "⚠️  WARNING: Gmail credentials.json not found!"
    echo "   Gmail draft creation will not work until credentials are set up."
    echo "   See docs/GMAIL_SETUP.md for instructions."
    echo ""
fi

echo "🔧 Starting Backend Server (Flask)..."
# Start Flask backend in background
python backend/app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "🎨 Starting Frontend Server (Vite)..."
# Start Vite frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers are starting up!"
echo ""
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:5000"
echo ""
echo "📧 Gmail Integration: Ready (if credentials.json is configured)"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped. Goodbye!"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID




