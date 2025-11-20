"""
Monit Patient - Main FastAPI Application

AI-powered ICU patient monitoring system with real-time streaming and voice interface.
Tagline: "Predict the future where uncertainty is the enemy"
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.logging_config import app_logger
from backend.api.routes import agents, patients, chat, alerts
from contextlib import asynccontextmanager
from backend.services.agent_service import AgentService

# Initialize agent service
agent_service = AgentService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown.
    """
    # Startup
    app_logger.info("Starting Monit Patient application...")

    # Initialize agent system with default configuration
    try:
        config = agent_service.load_configuration()
        if config:
            agent_service.initialize_agents(config)
            app_logger.info("Agent system initialized successfully")
        else:
            app_logger.warning("No agent configuration found - will use default on first request")
    except Exception as e:
        app_logger.error(f"Error initializing agents: {e}")

    app_logger.info("Monit Patient application started successfully")

    yield

    # Shutdown
    app_logger.info("Shutting down Monit Patient application...")


# Create FastAPI app
app = FastAPI(
    title="Monit Patient API",
    description="AI-powered real-time patient monitoring system",
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
app.include_router(agents.router)
app.include_router(patients.router)
app.include_router(chat.router)
app.include_router(alerts.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "application": "Monit Patient",
        "tagline": "Predict the future where uncertainty is the enemy",
        "version": "1.0.0",
        "status": "running",
        "features": {
            "multi_agent_system": settings.ENABLE_MULTI_AGENT_SYSTEM,
            "real_time_streaming": settings.ENABLE_REAL_TIME_STREAMING,
            "voice_interface": settings.ENABLE_VOICE_INTERFACE,
            "email_alerts": settings.ENABLE_EMAIL_ALERTS
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent_system": "active" if agent_service.active_orchestrator else "not_initialized"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.BACKEND_RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
