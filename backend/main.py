"""FastAPI main application for NVIDIA Dashboard backend."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from logging.config import dictConfig

from config import settings
from database.database import init_db
from api.routes import router
from scheduler import start_scheduler, stop_scheduler

# Configure logging
logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'nvidia_dashboard.log',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file'],
    },
}

dictConfig(logging_config)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting NVIDIA Dashboard API")
    logger.info(f"Environment: {settings.environment}")
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Start scheduler
    if settings.environment == 'production':
        start_scheduler()
    else:
        logger.info("Scheduler disabled in development mode")
    
    yield
    
    # Shutdown
    logger.info("Shutting down NVIDIA Dashboard API")
    stop_scheduler()


# Create FastAPI app
app = FastAPI(
    title="NVIDIA Economic Dashboard API",
    description="Backend API for NVIDIA economic analysis dashboard",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api", tags=["dashboard"])


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "NVIDIA Economic Dashboard API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.environment
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
