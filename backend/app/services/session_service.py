from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

def validate_and_record_session(
    activity_title: str,
    category: str,
    planned_minutes: int,
    actual_minutes: int,
    completed: bool,
    reflection_note: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validates and sanitizes a self-reported screen-free session.
    Clamps minutes to reasonable non-negative boundaries and records metadata.
    """
    if not activity_title or not activity_title.strip():
        raise ValueError("Activity title cannot be empty.")
    
    # Validation: actual minutes must be positive and capped at 24 hours (1440 mins)
    if actual_minutes < 0:
        raise ValueError("Self-reported minutes cannot be negative.")
    
    sanitized_minutes = max(1, min(actual_minutes, 1440))
    sanitized_planned = max(5, min(planned_minutes, 1440))

    return {
        "activity_title": activity_title.strip(),
        "category": category.strip() if category else "general",
        "planned_minutes": sanitized_planned,
        "self_reported_minutes": sanitized_minutes,
        "completed": bool(completed),
        "reflection_note": reflection_note.strip() if reflection_note else None,
        "recorded_at": datetime.now(timezone.utc).isoformat()
    }

def calculate_impact_metrics(sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes honest, calm impact metrics from session history.
    Never calculates manipulative streaks or guilt scores.
    """
    if not sessions:
        return {
            "total_screen_free_minutes": 0,
            "total_sessions_completed": 0,
            "total_sessions_attempted": 0,
            "categories_breakdown": {},
            "summary_message": "No screen-free sessions recorded yet. Step outside whenever you are ready."
        }

    total_minutes = sum(s.get("self_reported_minutes", 0) for s in sessions)
    completed_sessions = [s for s in sessions if s.get("completed", False)]
    
    category_counts = {}
    for s in sessions:
        cat = s.get("category", "general")
        category_counts[cat] = category_counts.get(cat, 0) + 1

    return {
        "total_screen_free_minutes": total_minutes,
        "total_sessions_completed": len(completed_sessions),
        "total_sessions_attempted": len(sessions),
        "categories_breakdown": category_counts,
        "summary_message": f"You have spent {total_minutes} self-reported minutes grounded in the physical world across {len(sessions)} sessions."
    }
