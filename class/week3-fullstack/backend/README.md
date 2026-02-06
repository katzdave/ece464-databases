# Animal Explorer Backend

FastAPI backend for the Animal Explorer web application.

## Features

- RESTful API for animal data
- 10 diverse sample animals from 6 animal classes
- Search and filter capabilities
- Statistics endpoint
- CORS enabled for frontend integration

## API Endpoints

- `GET /api/animals` - List all animals (with optional filters)
- `GET /api/animals/{id}` - Get single animal by ID
- `GET /api/animals/search?q=query` - Search animals
- `GET /api/stats` - Get collection statistics
- `GET /` - API information
- `GET /health` - Health check

## Setup

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest
```

## Project Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI application
│   ├── models.py        # Pydantic models
│   ├── data.py          # Sample animal data
│   └── routers/         # API route handlers
├── tests/               # Test suite
└── pyproject.toml       # Dependencies
```
