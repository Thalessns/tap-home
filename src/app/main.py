"""Main file to run the api."""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database.database import Database
from src.routing.tags.router import tag_router
from src.routing.music.router import music_router
from src.routing.preference.router import preference_router
from src.routing.routine.router import routine_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    await Database.init_models()
    yield


app = FastAPI(
    title="Python API Crud", version="0.1.0", lifespan=lifespan)


@app.get("/")
async def root() -> dict:
    """Root endpoint to check if the API is running.
    
    Returns:
        dict: A message indicating the API is running.
    """
    return {"message": "API is running"}


app.include_router(tag_router)
app.include_router(music_router)
app.include_router(preference_router)
app.include_router(routine_router)
