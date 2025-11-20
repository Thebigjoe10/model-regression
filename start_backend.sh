#!/bin/bash

echo "======================================"
echo "Solar Fish Dryer ML System - Startup"
echo "======================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created"
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
echo "Checking dependencies..."
python -c "import flask, sklearn, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Dependencies not installed"
    echo "Installing requirements..."
    pip install -r requirements.txt
    echo "Dependencies installed"
else
    echo "Dependencies already installed"
fi

echo
echo "Starting backend server..."
echo "   Access at: http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo

python backend.py
