import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: list[str] = [
        origin.strip() 
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
        if origin.strip()
    ]
    AI_INFERENCE_PROVIDER: str = os.getenv("AI_INFERENCE_PROVIDER", "ollama") # "ollama", "hosted", "fallback"
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_TIMEOUT: float = float(os.getenv("OLLAMA_TIMEOUT", "45.0"))
    GEMMA_MODEL: str = os.getenv("GEMMA_MODEL", "gemma2:2b")
    HOSTED_API_BASE_URL: str = os.getenv("HOSTED_API_BASE_URL", "https://openrouter.ai/api/v1")
    HOSTED_API_KEY: str = os.getenv("HOSTED_API_KEY", "")
    HOSTED_MODEL: str = os.getenv("HOSTED_MODEL", "google/gemma-2-9b-it:free")
    PLACES_MODE: str = os.getenv("PLACES_MODE", "osm")

settings = Settings()
