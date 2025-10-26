@echo off
echo 🚀 Starting Appraisalsystem Application...
echo.

echo 📦 Setting up Backend...
cd backend
call npm run setup
if errorlevel 1 (
    echo ❌ Backend setup failed!
    pause
    exit /b 1
)

echo 📦 Setting up Frontend...
cd ../frontend
call npm run setup
if errorlevel 1 (
    echo ❌ Frontend setup failed!
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo 🎯 Starting Application...
echo.
echo 📡 Starting Backend Server (Terminal 1)...
start "Backend Server" cmd /k "cd backend && npm run dev"

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo 🌐 Starting Frontend Server (Terminal 2)...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo 🎉 Application is starting!
echo 📡 Backend: http://localhost:5000
echo 🌐 Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul
