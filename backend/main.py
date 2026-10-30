
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.connection import create_database_tables

from backend.api.auth_routes import router as auth_router
from backend.api.farmer_routes import router as farmer_router
from backend.api.voice_routes import router as voice_router
from backend.api.chat_routes import router as chat_router
from backend.api.agriculture_routes import router as agriculture_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables when the API starts.
    create_database_tables()
    yield


app = FastAPI(
    title="KRISHI MITRA API",
    description="AI-powered agricultural companion for farmers",
    version="1.0.0",
    lifespan=lifespan,
)

# Development CORS settings for the Streamlit frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers.
app.include_router(auth_router, prefix="/api")
app.include_router(farmer_router, prefix="/api")
app.include_router(voice_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(agriculture_router, prefix="/api")



@app.get("/")
def root():
    return {
        "success": True,
        "message": "KRISHI MITRA API is running",
    }


@app.get("/health")
def health_check():
    return {
        "success": True,
        "status": "healthy",
    }
