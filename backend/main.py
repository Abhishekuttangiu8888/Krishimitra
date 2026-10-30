
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.connection import create_database_tables

from backend.api.auth_routes import router as auth_router
from backend.api.farmer_routes import router as farmer_router
from backend.api.voice_routes import router as voice_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    create_database_tables()

    yield


app = FastAPI(
    title="KRISHI MITRA API",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)


app.include_router(
    auth_router,
    prefix="/api",
)

app.include_router(
    farmer_router,
    prefix="/api",
)

app.include_router(
    voice_router,
    prefix="/api",
)


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "KRISHI MITRA API",
    }
