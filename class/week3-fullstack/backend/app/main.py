from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import animals, stats


app = FastAPI(
    title="Animal Explorer API",
    description="A RESTful API for exploring the animal kingdom",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # Create React App default
        "http://localhost:5174",  # Vite alternate
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(animals.router)
app.include_router(stats.router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Animal Explorer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
