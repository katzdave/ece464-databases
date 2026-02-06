#!/bin/bash

# Animal Explorer - Development Server Launcher
# Starts both backend and frontend in separate terminal windows

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "🚀 Starting Animal Explorer Development Servers..."

# Function to detect terminal emulator
launch_terminal() {
    local cmd=$1
    local title=$2

    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal --title="$title" -- bash -c "$cmd; exec bash"
    elif command -v konsole &> /dev/null; then
        konsole --title="$title" -e bash -c "$cmd; exec bash" &
    elif command -v xterm &> /dev/null; then
        xterm -T "$title" -e bash -c "$cmd; exec bash" &
    else
        echo "❌ No supported terminal emulator found"
        echo "Please start the servers manually:"
        echo "  Terminal 1: cd backend && uv run uvicorn app.main:app --reload"
        echo "  Terminal 2: cd frontend && npm run dev"
        exit 1
    fi
}

# Start backend
echo "📦 Starting Backend (FastAPI)..."
launch_terminal "cd '$SCRIPT_DIR/backend' && echo '🐍 Starting FastAPI backend...' && uv run uvicorn app.main:app --reload" "Animal Explorer - Backend"

sleep 2

# Start frontend
echo "⚛️  Starting Frontend (React + Vite)..."
launch_terminal "cd '$SCRIPT_DIR/frontend' && echo '⚛️  Starting React frontend...' && npm run dev" "Animal Explorer - Frontend"

sleep 2

echo ""
echo "✅ Development servers started!"
echo ""
echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo "📍 Frontend: http://localhost:5173"
echo ""
echo "💡 To stop the servers, close the terminal windows or press Ctrl+C in each"
echo ""
