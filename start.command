#!/bin/bash

# Robot Arm Control - Quick Start for Mac
# Double-click to start!

echo "================================================"
echo "   🤖 RoboArm Studio"
echo "================================================"
echo ""

# Find the script directory
cd "$(dirname "$0")"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Install Python from: https://www.python.org/downloads/"
    read -p "Press ENTER to exit..."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate the virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check and install dependencies
echo "📦 Checking dependencies..."
if ! python -c "import flask" 2>/dev/null || ! python -c "import serial" 2>/dev/null; then
    echo "⚙️  Installing dependencies..."
    pip install -q -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies OK"
fi

echo ""

# Check if Arduino is connected
echo "🔍 Searching for Arduino..."
if ls /dev/cu.usbmodem* 1> /dev/null 2>&1 || ls /dev/cu.usbserial* 1> /dev/null 2>&1; then
    echo "✅ Arduino found!"
else
    echo "⚠️  Arduino not detected. Connect it via USB before connecting."
fi
echo ""

# Start the server
echo "🚀 Starting server..."
echo "📱 Open browser at: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================"
echo ""

python robot_arm_server.py
