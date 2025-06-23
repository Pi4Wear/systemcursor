#!/bin/bash
# This script handles setup and execution for the Pro AI Completer.

# Navigate to the script's directory
cd "$(dirname "$0")"

echo "🚀 Starting Pro AI Completer..."

# --- 1. Check for Dependencies ---
if ! command -v xdotool &> /dev/null; then
    echo "⚠️ xdotool is not installed. This is required for application context."
    echo "Please install it by running: sudo apt-get install xdotool"
    # Exit if not found, as it's a critical dependency now.
    exit 1
fi

# --- 2. Check for API Key ---
if [ ! -f .env ]; then
    echo "❌ .env file not found! Please create one with your GEMINI_API_KEY."
    exit 1
fi

source .env
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY not set in .env file!"
    exit 1
fi
echo "✅ API key found."

# --- 3. Set up Python Virtual Environment ---
VENV_PATH="venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "🔧 No virtual environment found. Creating one now..."
    python3 -m venv "$VENV_PATH"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment. Please ensure python3 and python3-venv are installed."
        exit 1
    fi
fi

# Activate and install dependencies
source "$VENV_PATH/bin/activate"
echo "🐍 Installing/checking dependencies from requirements.txt..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies."
    exit 1
fi
echo "✅ Dependencies are up to date."

# --- 4. Run the main application with sudo ---
VENV_PYTHON="$VENV_PATH/bin/python"
echo "🔐 Running main.py with sudo for global keyboard access..."
echo "💡 You will be prompted for your password."

# Export the API key so the sudo environment can access it
export GEMINI_API_KEY

sudo -E env "PATH=$PATH" "$VENV_PYTHON" main.py

echo "✅ Pro AI Completer has shut down." 