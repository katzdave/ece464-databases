# Animal Explorer - Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Check

```bash
# Check Python (need 3.11+)
python3 --version

# Check UV package manager
uv --version
# If not installed: curl -LsSf https://astral.sh/uv/install.sh | sh

# Check Node.js (need 18+)
node --version

# Check npm
npm --version
```

## Step 1: Start the Backend (2 minutes)

Open a terminal in the `week3-fullstack` directory:

```bash
# Navigate to backend
cd backend

# Install dependencies (first time only)
uv sync

# Start the server
uv run uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**Test it**: Open http://localhost:8000/docs in your browser
You should see the FastAPI interactive documentation!

## Step 2: Start the Frontend (2 minutes)

Open a **new terminal** in the `week3-fullstack` directory:

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start the dev server
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
```

The app should automatically open in your browser at http://localhost:5173

## Step 3: Explore the App (1 minute)

### Browse Animals
- You'll see a grid of 10 animal cards
- Each card shows the animal's name, class, habitat, diet, and conservation status
- Click any card to see full details in a modal

### Try Search & Filter
- **Search**: Type "tiger" or "stripe" in the search box
- **Filter by Class**: Select "Mammal" from the dropdown
- **Filter by Habitat**: Type "forest" in the habitat filter
- **Clear**: Click "Clear" to reset filters

### View Statistics
- Click the "Statistics" button in the navigation
- See visual bar charts showing:
  - Total animals
  - Distribution by animal class
  - Distribution by diet type
  - Conservation status breakdown

## Step 4: Run Tests (optional)

Test the backend API:

```bash
cd backend
uv run pytest -v
```

You should see all 17 tests pass:
```
============================== 17 passed in 0.33s ==============================
```

## Troubleshooting

### Backend won't start
- **Problem**: Port 8000 already in use
- **Solution**: Kill the process using port 8000 or change the port:
  ```bash
  uv run uvicorn app.main:app --reload --port 8001
  ```
  Then update `frontend/src/services/api.js` to use port 8001

### Frontend won't start
- **Problem**: Port 5173 already in use
- **Solution**: Vite will automatically try port 5174, 5175, etc.

### Frontend shows errors
- **Problem**: Can't connect to backend
- **Solution**: Make sure the backend is running at http://localhost:8000
- Check the browser console for error messages

### CORS errors
- **Problem**: Browser blocks requests from frontend to backend
- **Solution**: The backend is already configured for CORS. Make sure you're accessing the frontend through the Vite dev server (http://localhost:5173), not opening index.html directly in the browser.

## Next Steps

Now that you're up and running:

1. **Explore the Code**:
   - Backend: `backend/app/models.py` - See the data models
   - Backend: `backend/app/data.py` - Check out the sample animals
   - Frontend: `frontend/src/App.jsx` - Understand the React structure
   - Frontend: `frontend/src/components/` - Examine individual components

2. **Make Changes**:
   - Add a new animal to `backend/app/data.py`
   - Customize colors in the component CSS files
   - Add new API endpoints in `backend/app/routers/`
   - Create new React components

3. **Learn More**:
   - Backend API docs: http://localhost:8000/docs
   - FastAPI tutorial: https://fastapi.tiangolo.com/tutorial/
   - React docs: https://react.dev/

## Development Tips

- **Backend hot-reload**: The `--reload` flag automatically restarts the server when you change Python files
- **Frontend hot-reload**: Vite automatically refreshes the browser when you change React files
- **API testing**: Use the interactive docs at http://localhost:8000/docs to test API endpoints
- **Browser DevTools**: Open the Network tab to see API requests and responses

## Shutting Down

When you're done:
1. Press `Ctrl+C` in the backend terminal
2. Press `Ctrl+C` in the frontend terminal

That's it! You now have a fully functional full-stack application running locally.
