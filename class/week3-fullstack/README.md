# Animal Explorer - Full-Stack Web Application

A modern full-stack web application for exploring the animal kingdom, built with React and FastAPI.

## Features

### Frontend (React + Vite)
- **Browse Animals**: Grid view with beautiful cards showing key animal info
- **Detailed View**: Click any animal for comprehensive details
- **Search**: Find animals by name, species, or interesting facts
- **Filter**: Filter by animal class (Mammal, Bird, etc.) or habitat
- **Statistics Dashboard**: Visual charts showing collection statistics
- **Responsive Design**: Works great on desktop and mobile

### Backend (FastAPI)
- **RESTful API**: Clean, documented API endpoints
- **10 Sample Animals**: Diverse collection from 6 animal classes
- **Search & Filter**: Multiple query options
- **Statistics**: Aggregate data by class, diet, habitat, and conservation status
- **CORS Enabled**: Seamless frontend integration
- **Full Test Coverage**: Comprehensive pytest suite

## Quick Start

See [QUICKSTART.md](./QUICKSTART.md) for a 5-minute tutorial.

### Prerequisites
- Python 3.11+ with [UV](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with npm

### Installation

1. **Clone and navigate to the project**:
   ```bash
   cd week3-fullstack
   ```

2. **Start the backend**:
   ```bash
   cd backend
   uv sync
   uv run uvicorn app.main:app --reload
   ```
   Backend runs at: http://localhost:8000
   API docs: http://localhost:8000/docs

3. **Start the frontend** (in a new terminal):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend runs at: http://localhost:5173

## Project Structure

```
week3-fullstack/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # FastAPI app with CORS
│   │   ├── models.py          # Pydantic models & enums
│   │   ├── data.py            # Sample animals & queries
│   │   └── routers/           # API endpoints
│   │       ├── animals.py     # Animal CRUD routes
│   │       └── stats.py       # Statistics route
│   ├── tests/                 # Pytest test suite
│   └── pyproject.toml         # UV configuration
├── frontend/                   # React application
│   ├── src/
│   │   ├── App.jsx            # Main component
│   │   ├── components/        # React components
│   │   │   ├── AnimalCard.jsx
│   │   │   ├── AnimalGrid.jsx
│   │   │   ├── AnimalDetail.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   └── StatsPanel.jsx
│   │   └── services/
│   │       └── api.js         # API client
│   └── package.json           # npm configuration
└── README.md                   # This file
```

## API Endpoints

- `GET /api/animals` - List all animals (with optional filters)
  - Query params: `animal_class`, `habitat`, `species`
- `GET /api/animals/{id}` - Get single animal by ID
- `GET /api/animals/search?q=query` - Search animals
- `GET /api/stats` - Get collection statistics
- `GET /health` - Health check

## Sample Animals

The collection includes 10 diverse animals:
- **Mammals**: African Elephant, Bengal Tiger, Giant Panda, Red Kangaroo
- **Birds**: Bald Eagle, Emperor Penguin
- **Reptiles**: Green Sea Turtle
- **Amphibians**: Red Poison Dart Frog
- **Fish**: Great White Shark
- **Invertebrates**: Monarch Butterfly

## Development

### Run Backend Tests
```bash
cd backend
uv run pytest -v
```

### Build Frontend for Production
```bash
cd frontend
npm run build
```

### Environment Variables
Backend defaults to `localhost:8000`
Frontend API client defaults to `http://localhost:8000`

To change the API URL, edit `frontend/src/services/api.js`

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation with type hints
- **Uvicorn**: ASGI server
- **Pytest**: Testing framework

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **CSS3**: Styling with Flexbox/Grid
- **Fetch API**: HTTP client

## Educational Context

This project is for **ECE464: Databases** (Week 3 - Full-Stack Development).

**Learning Objectives**:
- Build RESTful APIs with FastAPI
- Create responsive React frontends
- Implement CRUD operations
- Design data models with Pydantic
- Write comprehensive tests
- Integrate frontend and backend

## License

MIT - Educational use for ECE464

## Credits

Built with Claude Code for ECE464 Databases course.
