#!/bin/bash

echo "🚀 Starting Garmin Health Analyzer..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install it first."
    exit 1
fi

echo "✅ Python and Node.js found"
echo ""

# Setup Backend
echo -e "${BLUE}Setting up Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

echo "Installing Python dependencies..."
pip install -r requirements.txt -q

echo -e "${GREEN}✅ Backend ready${NC}"
cd ..

# Setup Frontend
echo -e "${BLUE}Setting up Frontend...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install -q
fi

echo -e "${GREEN}✅ Frontend ready${NC}"
cd ..

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo ""
