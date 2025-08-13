#!/bin/bash

echo "========================================"
echo "Learning Platform Installation Script"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

echo "Python found! Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing required packages..."
pip install -r requirements.txt

echo
echo "========================================"
echo "Installation completed successfully!"
echo "========================================"
echo
echo "To start the application:"
echo "1. Run: source venv/bin/activate"
echo "2. Run: python app.py"
echo "3. Open browser and go to: http://localhost:5000"
echo 