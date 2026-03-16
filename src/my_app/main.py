from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.my_app.db.database import engine
from src.my_app.db.db_models import Base
from src.my_app.routers import (
    admin_router,
    auth_router,
    bikes_router,
    rentals_router,
    stations_router,
    users_router,
    predictions_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> STARTUP: creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(">>> STARTUP: done")
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(bikes_router.router)
app.include_router(users_router.router)
app.include_router(rentals_router.router)
app.include_router(admin_router.router)
app.include_router(stations_router.router)
app.include_router(auth_router.router)
app.include_router(predictions_router.router)


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Welcome to EcomunTE API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {"bikes": "/bikes", "users": "/users"},
    }
