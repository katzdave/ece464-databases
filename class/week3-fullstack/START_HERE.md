# 🚀 Animal Explorer - Start Here!

Welcome to the Animal Explorer full-stack web application!

## 📋 What You Need

- **Python 3.11+** with [UV](https://docs.astral.sh/uv/) package manager
- **Node.js 18+** with npm

## ⚡ Quick Start (Choose One)

### Option 1: Automated Script (Linux/Mac)
```bash
./run-dev.sh
```
This opens two terminals and starts both servers automatically.

### Option 2: Manual Start (All Platforms)

**Terminal 1 - Backend:**
```bash
cd backend
uv sync                 # First time only
uv run uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install            # First time only
npm run dev
```

## 🌐 Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ✅ Verify Installation

### Test Backend
```bash
cd backend
uv run pytest -v
```
Expected: **17 passed**

### Test Frontend
Open http://localhost:5173 in your browser
You should see 10 animal cards!

## 📚 Documentation

- **[README.md](./README.md)** - Full project overview
- **[QUICKSTART.md](./QUICKSTART.md)** - 5-minute tutorial
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Technical details
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - What was built

## 🎯 Try These Features

1. **Browse Animals**: See the grid of 10 animal cards
2. **View Details**: Click any animal card for full information
3. **Search**: Type "tiger" or "stripe" in the search box
4. **Filter**: Select "Mammal" from the class dropdown
5. **Statistics**: Click "Statistics" to see visual charts

## 🆘 Troubleshooting

**Backend won't start?**
- Check Python version: `python3 --version` (need 3.11+)
- Check UV is installed: `uv --version`
- Port 8000 in use? Change port: `uv run uvicorn app.main:app --reload --port 8001`

**Frontend won't start?**
- Check Node version: `node --version` (need 18+)
- Port 5173 in use? Vite will auto-select next port

**Frontend shows errors?**
- Make sure backend is running at http://localhost:8000
- Check browser console (F12) for error messages

**CORS errors?**
- Access frontend through Vite dev server, not direct file:// URL
- Backend CORS is pre-configured for http://localhost:5173

## 📞 Need Help?

See the full [QUICKSTART.md](./QUICKSTART.md) guide for detailed instructions and troubleshooting.

## 🎓 Educational Context

Built for **ECE464: Databases** course (Week 3 - Full-Stack Development)

**Learning Topics**:
- RESTful API design with FastAPI
- React frontend development
- Backend-frontend integration
- Type-safe data models with Pydantic
- Modern development tools (UV, Vite)

Enjoy exploring the animal kingdom! 🦁🐘🦅
