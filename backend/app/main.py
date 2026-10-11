import logging
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

from app.api.recommendations import router as recommendations_router

app = FastAPI(
    title="Touch Grass AI API",
    description="Backend API powering Touch Grass AI: screen-free offline activity recommendations, deterministic safety, and grounded experiences.",
    version="1.0.0"
)

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Clean origins list
configured_origins = [o.strip() for o in settings.CORS_ORIGINS if o.strip()]
has_wildcard = "*" in configured_origins

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=configured_origins if configured_origins else ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=not has_wildcard,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid check-in parameters",
            "details": [f"{e['loc'][-1]}: {e['msg']}" for e in exc.errors()]
        }
    )

app.include_router(recommendations_router)

from app.services.gemma_service import is_ollama_model_ready

@app.get("/")
def root():
    return {
        "app": "Touch Grass AI API",
        "description": "Helping people spend less time on screens and more time experiencing the real world.",
        "version": "1.0.0",
        "health_check": "/api/health"
    }

@app.get("/api/health")
async def health_check():
    ollama_ready, reason = await is_ollama_model_ready(settings.OLLAMA_BASE_URL, settings.GEMMA_MODEL)
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ai_provider": settings.AI_INFERENCE_PROVIDER,
        "gemma_model": settings.GEMMA_MODEL,
        "ollama_ready": ollama_ready,
        "ollama_model_status": reason,
        "places_mode": settings.PLACES_MODE,
        "deterministic_safety": "active",
        "version": "1.0.0"
    }
