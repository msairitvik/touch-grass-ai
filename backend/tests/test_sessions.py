import pytest
from app.services.session_service import validate_and_record_session, calculate_impact_metrics

def test_validate_valid_session():
    """
    Verifies that a valid session is correctly formatted and recorded.
    """
    res = validate_and_record_session(
        activity_title="Five-Senses Tree Canopy Immersion",
        category="outdoor",
        planned_minutes=25,
        actual_minutes=30,
        completed=True,
        reflection_note="Felt the breeze and heard cardinals singing."
    )
    assert res["activity_title"] == "Five-Senses Tree Canopy Immersion"
    assert res["planned_minutes"] == 25
    assert res["self_reported_minutes"] == 30
    assert res["completed"] is True
    assert "cardinals" in res["reflection_note"]
    assert "recorded_at" in res

def test_validate_negative_duration_raises_error():
    """
    Verifies that negative self-reported minutes are rejected.
    """
    with pytest.raises(ValueError, match="cannot be negative"):
        validate_and_record_session(
            activity_title="Reading in park",
            category="outdoor",
            planned_minutes=30,
            actual_minutes=-10,
            completed=True
        )

def test_validate_empty_title_raises_error():
    """
    Verifies that empty activity titles are rejected.
    """
    with pytest.raises(ValueError, match="cannot be empty"):
        validate_and_record_session(
            activity_title="   ",
            category="outdoor",
            planned_minutes=30,
            actual_minutes=20,
            completed=True
        )

def test_validate_excessive_duration_clamping():
    """
    Verifies that unrealistic durations exceeding 24 hours are safely clamped to 1440 mins.
    """
    res = validate_and_record_session(
        activity_title="Long Nature Hike",
        category="outdoor",
        planned_minutes=60,
        actual_minutes=99999,
        completed=True
    )
    assert res["self_reported_minutes"] == 1440

def test_calculate_impact_metrics_empty():
    """
    Verifies impact metrics handle empty history gracefully.
    """
    metrics = calculate_impact_metrics([])
    assert metrics["total_screen_free_minutes"] == 0
    assert metrics["total_sessions_completed"] == 0
    assert metrics["total_sessions_attempted"] == 0

def test_calculate_impact_metrics_aggregation():
    """
    Verifies impact aggregation correctly sums minutes and counts without manipulative streaks.
    """
    sessions = [
        {"self_reported_minutes": 25, "completed": True, "category": "outdoor"},
        {"self_reported_minutes": 40, "completed": True, "category": "indoor"},
        {"self_reported_minutes": 15, "completed": False, "category": "outdoor"},
    ]
    metrics = calculate_impact_metrics(sessions)
    assert metrics["total_screen_free_minutes"] == 80
    assert metrics["total_sessions_completed"] == 2
    assert metrics["total_sessions_attempted"] == 3
    assert metrics["categories_breakdown"]["outdoor"] == 2
    assert metrics["categories_breakdown"]["indoor"] == 1
