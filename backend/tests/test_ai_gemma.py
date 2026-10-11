import json
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

MOCK_GEMMA_SUCCESS_OUTPUT = json.dumps({
    "primary": {
        "title": "Gemma AI Personalized Forest Canopy Stroll",
        "why_recommended": "Tailored for your stress to dissolve screen tension through fractal pine patterns.",
        "steps": [
            "Put phone in pocket on silent.",
            "Walk 10 minutes to the nearest cluster of trees.",
            "Touch the rough bark of the oldest tree and take 4 deep belly breaths.",
            "Notice 3 birds or insect calls in the canopy."
        ]
    },
    "backup": {
        "title": "Gemma AI Tactile Charcoal Sketching",
        "why_recommended": "Engages physical motor skills away from glass displays.",
        "steps": [
            "Take scrap paper and pencil.",
            "Sketch the natural outline of your own hand.",
            "Focus on the texture and graphite friction."
        ]
    }
})

def test_gemma_personalization_success():
    """
    Verifies that when Ollama responds with valid Gemma output,
    the recommendations are personalized and metadata reflects active local AI.
    """
    async def mock_personalize(*args, **kwargs):
        return json.loads(MOCK_GEMMA_SUCCESS_OUTPUT), "active_gemma_local", "Personalized by Gemma 2 (2B) via local Ollama."

    with patch("app.services.recommender.personalize_with_gemma", new=mock_personalize):
        payload = {
            "mood": "stressed",
            "free_time_minutes": 45,
            "social_context": "alone",
            "interests": ["nature", "walking"],
            "weather_condition": "pleasant",
            "time_of_day": "afternoon"
        }
        response = client.post("/api/recommendations", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["ai_personalized"] is True
        assert "Gemma" in data["engine"]
        assert data["ai_status"] == "active_gemma_local"
        assert data["primary_activity"]["title"] == "Gemma AI Personalized Forest Canopy Stroll"
        assert "fractal pine" in data["primary_activity"]["why_recommended"]
        assert len(data["primary_activity"]["steps"]) == 4

def test_gemma_failure_fallback_to_deterministic():
    """
    Verifies that when Ollama is unavailable or times out,
    the app transparently falls back to deterministic recommendations.
    """
    async def mock_personalize_failure(*args, **kwargs):
        return None, "fallback_timeout", "Local Gemma 2 (2B) took longer than 45s to generate."

    with patch("app.services.recommender.personalize_with_gemma", new=mock_personalize_failure):
        payload = {
            "mood": "calm",
            "free_time_minutes": 30,
            "social_context": "alone",
            "weather_condition": "pleasant",
            "time_of_day": "afternoon"
        }
        response = client.post("/api/recommendations", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["ai_personalized"] is False
        assert "Deterministic" in data["engine"]
        assert data["ai_status"] == "fallback_timeout"
        assert "primary_activity" in data
        assert "backup_activity" in data
        assert data["primary_activity"]["title"] is not None

def test_gemma_invalid_output_fallback():
    """
    Verifies that malformed JSON or schema mismatches from LLM fallback cleanly.
    """
    async def mock_personalize_invalid(*args, **kwargs):
        return None, "fallback_invalid_schema", "Output missing primary or backup keys."

    with patch("app.services.recommender.personalize_with_gemma", new=mock_personalize_invalid):
        payload = {
            "mood": "bored",
            "free_time_minutes": 45,
            "social_context": "alone",
            "weather_condition": "pleasant"
        }
        response = client.post("/api/recommendations", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["ai_personalized"] is False
        assert data["ai_status"] == "fallback_invalid_schema"
        assert data["primary_activity"]["title"] is not None

def test_gemma_cannot_override_extreme_heat():
    """
    Verifies that even if Gemma returns an intense outdoor sport,
    deterministic safety strictly intercepts and overrides it during extreme heat.
    """
    async def mock_unsafe_heat_gemma(*args, **kwargs):
        return {
            "primary": {
                "title": "Outdoor Midday Sun Sprint",
                "why_recommended": "Run under the direct sun",
                "steps": ["Sprint outside in the heat"]
            },
            "backup": {
                "title": "Open Field Football",
                "why_recommended": "Play in the sun",
                "steps": ["Play outside"]
            }
        }, "active_gemma_local", "Personalized"

    with patch("app.services.recommender.personalize_with_gemma", new=mock_unsafe_heat_gemma):
        payload = {
            "mood": "restless",
            "free_time_minutes": 45,
            "social_context": "alone",
            "interests": ["sports"],
            "weather_condition": "extreme_heat",
            "time_of_day": "afternoon"
        }
        response = client.post("/api/recommendations", json=payload)
        assert response.status_code == 200
        data = response.json()

        # Deterministic safety MUST win
        assert data["safety_status"] == "safety_override_applied"
        assert any("EXTREME_HEAT_PROTECTION" in r for r in data["applied_safety_rules"])
        assert data["primary_activity"]["category"] in ["indoor_cool", "indoor"]
        assert "Indoor Cool" in data["primary_activity"]["title"] or "indoor" in data["primary_activity"]["category"]
        assert data["primary_activity"]["safety_verified"] is True

def test_gemma_cannot_override_late_night_solo():
    """
    Verifies that even if Gemma returns an isolated night stroll,
    deterministic safety overrides it for late-night solo outings.
    """
    async def mock_unsafe_night_gemma(*args, **kwargs):
        return {
            "primary": {
                "title": "Midnight Isolated Dark Trail Stroll",
                "why_recommended": "Walk alone in the pitch dark",
                "steps": ["Hike in isolated woods alone"]
            },
            "backup": {
                "title": "Remote Night Alley Walk",
                "why_recommended": "...",
                "steps": ["..."]
            }
        }, "active_gemma_local", "Personalized"

    with patch("app.services.recommender.personalize_with_gemma", new=mock_unsafe_night_gemma):
        payload = {
            "mood": "restless",
            "free_time_minutes": 30,
            "social_context": "alone",
            "interests": ["walking"],
            "weather_condition": "pleasant",
            "time_of_day": "late_night"
        }
        response = client.post("/api/recommendations", json=payload)
        assert response.status_code == 200
        data = response.json()

        # Deterministic safety MUST win
        assert data["safety_status"] == "safety_override_applied"
        assert any("LATE_NIGHT_SOLO_SAFETY" in r for r in data["applied_safety_rules"])
        assert data["primary_activity"]["category"] == "home_winddown"
        assert "Wind-Down" in data["primary_activity"]["title"]
        assert data["primary_activity"]["safety_verified"] is True
