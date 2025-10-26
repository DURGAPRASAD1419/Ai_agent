#!/bin/bash

echo "🚀 Starting Appraisalsystem Application..."
echo

echo "📦 Setting up Backend..."
cd backend
npm run setup
if [ $? -ne 0 ]; then
    echo "❌ Backend setup failed!"
    exit 1
fi

echo "📦 Setting up Frontend..."
cd ../frontend
npm run setup
if [ $? -ne 0 ]; then
    echo "❌ Frontend setup failed!"
    exit 1
fi

echo
echo "✅ Setup complete!"
echo
echo "🎯 Starting Application..."
echo
echo "📡 Starting Backend Server..."
gnome-terminal -- bash -c "cd backend && npm run dev; exec bash" 2>/dev/null || xterm -e "cd backend && npm run dev" 2>/dev/null || osascript -e 'tell app "Terminal" to do script "cd backend && npm run dev"' 2>/dev/null || echo "Please manually run: cd backend && npm run dev"

echo "⏳ Waiting for backend to start..."
sleep 5

echo "🌐 Starting Frontend Server..."
gnome-terminal -- bash -c "cd frontend && npm start; exec bash" 2>/dev/null || xterm -e "cd frontend && npm start" 2>/dev/null || osascript -e 'tell app "Terminal" to do script "cd frontend && npm start"' 2>/dev/null || echo "Please manually run: cd frontend && npm start"

echo
echo "🎉 Application is starting!"
echo "📡 Backend: http://localhost:5000"
echo "🌐 Frontend: http://localhost:3000"
echo
echo "Press Enter to exit..."
read
