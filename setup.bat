@echo off
REM Windows setup script

echo 🚀 Starting Garmin Health Analyzer...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install it first.
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install it first.
    exit /b 1
)

echo ✅ Python and Node.js found
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt -q

echo ✅ Backend ready
cd ..

REM Setup Frontend
echo Setting up Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install -q
)

echo ✅ Frontend ready
cd ..

echo.
echo 🎉 Setup complete!
echo.
echo To start the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   python app.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm start
echo.
echo Then open http://localhost:3000 in your browser
echo.
pause
