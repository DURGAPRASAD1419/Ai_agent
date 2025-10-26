#!/bin/bash

# Research Paper Agent Startup Script

echo "🚀 Starting Research Paper Agent..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads

echo "✅ Setup complete!"
echo ""
echo "🎯 To start the application:"
echo "   python3 app.py"
echo ""
echo "🌐 The application will be available at:"
echo "   Web Interface: http://localhost:5000"
echo "   API: http://localhost:5000/api"
echo ""
echo "📄 Upload your research paper PDF and generate a complete web application!"
