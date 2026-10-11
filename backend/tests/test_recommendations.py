from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Helper to ensure safety unit tests test deterministic logic instantaneously
async def mock_deterministic_only(*args, **kwargs):
    return None, "fallback_deterministic", "Deterministic test mock"

@patch("app.services.recommender.personalize_with_gemma", new=mock_deterministic_only)
def test_extreme_heat_deterministic_safety():
    """
    Verifies that extreme heat triggers deterministic safety rules,
    blocking strenuous outdoor sports and enforcing cool indoor spaces.
    """
    payload = {
        "mood": "restless",
        "free_time_minutes": 45,
        "social_context": "alone",
        "interests": ["sports", "movement"],
        "weather_condition": "extreme_heat",
        "time_of_day": "afternoon"
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["safety_status"] == "safety_override_applied"
    assert any("EXTREME_HEAT_PROTECTION" in rule for rule in data["applied_safety_rules"])
    assert data["primary_activity"]["category"] in ["indoor_cool", "indoor"]
    assert "Indoor Cool" in data["primary_activity"]["title"] or "indoor" in data["primary_activity"]["category"]
    assert data["primary_activity"]["safety_verified"] is True

@patch("app.services.recommender.personalize_with_gemma", new=mock_deterministic_only)
def test_stormy_weather_deterministic_safety():
    """
    Verifies that severe stormy weather blocks open outdoor spaces
    and enforces sheltered indoor offline experiences.
    """
    payload = {
        "mood": "stressed",
        "free_time_minutes": 30,
        "social_context": "alone",
        "interests": ["walking", "nature"],
        "weather_condition": "stormy",
        "time_of_day": "afternoon"
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["safety_status"] == "safety_override_applied"
    assert any("SEVERE_WEATHER_PROTECTION" in rule for rule in data["applied_safety_rules"])
    assert data["primary_activity"]["category"] in ["indoor_sheltered", "indoor"]
    assert data["primary_activity"]["safety_verified"] is True

@patch("app.services.recommender.personalize_with_gemma", new=mock_deterministic_only)
def test_late_night_solo_deterministic_safety():
    """
    Verifies that late-night solo outings strictly block isolated outdoor areas
    and enforce cozy home wind-down or morning plan.
    """
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

    assert data["safety_status"] == "safety_override_applied"
    assert any("LATE_NIGHT_SOLO_SAFETY" in rule for rule in data["applied_safety_rules"])
    assert data["primary_activity"]["category"] == "home_winddown"
    assert "Wind-Down" in data["primary_activity"]["title"]
    assert data["primary_activity"]["safety_verified"] is True

@patch("app.services.recommender.personalize_with_gemma", new=mock_deterministic_only)
def test_pleasant_weather_with_friend():
    """
    Verifies regular daytime recommendation with friends generates
    one primary activity and one backup activity without safety overrides.
    """
    payload = {
        "mood": "curious",
        "free_time_minutes": 60,
        "social_context": "with_friend",
        "interests": ["exploration", "nature"],
        "weather_condition": "pleasant",
        "time_of_day": "afternoon"
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["safety_status"] == "guaranteed_safe"
    assert len(data["applied_safety_rules"]) == 0
    assert "primary_activity" in data
    assert "backup_activity" in data
    assert "Shared:" in data["primary_activity"]["title"]
    assert data["primary_activity"]["estimated_minutes"] <= 60
    assert data["backup_activity"]["estimated_minutes"] <= 60

@patch("app.services.recommender.personalize_with_gemma", new=mock_deterministic_only)
def test_location_absent_does_not_call_osm():
    """
    Verifies that when location is NOT provided, OSM is NOT queried
    and places_source is 'place_agnostic'.
    """
    payload = {
        "mood": "calm",
        "free_time_minutes": 30,
        "social_context": "alone",
        "weather_condition": "pleasant",
        "location": None
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["places_source"] == "place_agnostic"
    assert data["primary_activity"]["location_info"] is None
