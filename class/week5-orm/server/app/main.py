from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, rooms, submissions, users
from app.ws import router as ws_router

app = FastAPI(title="Jackbox Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(rooms.router)
app.include_router(submissions.router)
app.include_router(users.router)
app.include_router(ws_router)
