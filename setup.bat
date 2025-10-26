@echo off
echo 🚀 Starting Research Paper Agent...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python first.
    pause
    exit /b 1
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist uploads mkdir uploads

echo ✅ Setup complete!
echo.
echo 🎯 To start the application:
echo    python app.py
echo.
echo 🌐 The application will be available at:
echo    Web Interface: http://localhost:5000
echo    API: http://localhost:5000/api
echo.
echo 📄 Upload your research paper PDF and generate a complete web application!
pause
