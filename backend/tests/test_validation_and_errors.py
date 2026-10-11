from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_missing_required_mood():
    """
    Verifies that omitting required fields returns HTTP 422 with a structured error message.
    """
    payload = {
        "free_time_minutes": 30,
        "social_context": "alone"
        # missing 'mood'
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert any("mood" in str(d) for d in data.get("details", []))

def test_invalid_negative_duration():
    """
    Verifies that durations below the minimum (10 mins) return HTTP 422.
    """
    payload = {
        "mood": "calm",
        "free_time_minutes": 2, # Minimum is 10
        "social_context": "alone"
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert any("free_time_minutes" in str(d) for d in data.get("details", []))

def test_options_cors_preflight():
    """
    Verifies CORS preflight OPTIONS returns allowed methods.
    """
    response = client.options(
        "/api/recommendations",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST"
        }
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
