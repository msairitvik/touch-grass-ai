from datetime import datetime
from typing import List, Tuple
from app.models.schemas import CheckInRequest, Activity

RULE_EXTREME_HEAT = "EXTREME_HEAT_PROTECTION: Outdoor strenuous sports & long sun exposure blocked. Indoor cool space prioritized to prevent heat illness."
RULE_STORMY = "SEVERE_WEATHER_PROTECTION: Outdoor open spaces, bodies of water, and exposed parks blocked. Sheltered indoor activities enforced."
RULE_LATE_NIGHT_SOLO = "LATE_NIGHT_SOLO_SAFETY: Solitary night walks and isolated outdoor areas blocked. Cozy home wind-down or morning plan enforced for personal safety."

def evaluate_safety_constraints(request: CheckInRequest) -> Tuple[List[str], dict]:
    """
    Deterministically computes non-negotiable safety constraints based on
    weather, time of day, and social context.
    """
    applied_rules = []
    constraints = {
        "allow_outdoor_sports": True,
        "allow_outdoor_general": True,
        "enforce_indoor_only": False,
        "enforce_home_winddown": False,
        "hydration_mandatory": False
    }

    # 1. Extreme Heat Rule
    if request.weather_condition.lower() in ["extreme_heat", "heatwave", "very_hot"]:
        applied_rules.append(RULE_EXTREME_HEAT)
        constraints["allow_outdoor_sports"] = False
        constraints["allow_outdoor_general"] = False
        constraints["enforce_indoor_only"] = True
        constraints["hydration_mandatory"] = True

    # 2. Stormy Weather Rule
    if request.weather_condition.lower() in ["stormy", "severe_rain", "thunderstorm", "blizzard"]:
        applied_rules.append(RULE_STORMY)
        constraints["allow_outdoor_sports"] = False
        constraints["allow_outdoor_general"] = False
        constraints["enforce_indoor_only"] = True

    # 3. Late-Night Solo Outing Rule
    # Check explicitly passed time_of_day or current local hour if not specified
    time_of_day = request.time_of_day.lower() if request.time_of_day else ""
    current_hour = datetime.now().hour
    is_late_night = (time_of_day == "late_night") or (not time_of_day and (current_hour >= 22 or current_hour < 5))

    if is_late_night and request.social_context.lower() == "alone":
        applied_rules.append(RULE_LATE_NIGHT_SOLO)
        constraints["allow_outdoor_general"] = False
        constraints["allow_outdoor_sports"] = False
        constraints["enforce_home_winddown"] = True

    return applied_rules, constraints

def enforce_deterministic_safety(activity: Activity, request: CheckInRequest, constraints: dict) -> Activity:
    """
    Deterministically sanitizes and adjusts an activity so no LLM or prompt
    can violate core real-world safety policies.
    """
    # Rule 1 & 2: Outdoor blocked due to extreme heat or storm
    if constraints.get("enforce_indoor_only") and activity.category in ["outdoor", "sports", "movement_outdoor"]:
        if "extreme_heat" in request.weather_condition.lower():
            activity.title = f"Indoor Cool Escape: {activity.title.replace('Outdoor', 'Indoor')}"
            activity.category = "indoor_cool"
            activity.safety_notes = "Adjusted for extreme heat: stay in an air-conditioned or well-ventilated indoor space. Drink cold water."
            activity.steps = [
                "Move to a cool indoor environment (library, quiet cafe, or shaded home room).",
                "Keep a chilled glass or bottle of water right beside you.",
                "Leave phone in another room or turn on 'Do Not Disturb'.",
                "Engage in hands-on calm focus without overheating."
            ]
        elif "storm" in request.weather_condition.lower():
            activity.title = f"Sheltered Offline Sanctuary: {activity.title}"
            activity.category = "indoor_sheltered"
            activity.safety_notes = "Adjusted for severe weather: safe indoor environment enforced away from hazardous outdoor conditions."
            activity.steps = [
                "Stay safely indoors away from open windows and storm hazards.",
                "Make yourself a warm cup of herbal tea or warm water.",
                "Turn off digital screens and enjoy the tactile sound of rain against the shelter.",
                "Engage in an offline analog pastime (sketching, reading, physical puzzle)."
            ]
        activity.safety_verified = True

    # Rule 3: Late night solo outings
    if constraints.get("enforce_home_winddown") and activity.category in ["outdoor", "night_walk", "outdoor_solitary"]:
        activity.title = "Gentle Night Wind-Down & Morning Intention"
        activity.category = "home_winddown"
        activity.safety_notes = "Adjusted for late-night solo safety: isolated outdoor outings after dark are avoided to ensure personal peace of mind and safety."
        activity.steps = [
            "Keep the phone face-down and dimmed.",
            "Dim the room lighting and do 5 minutes of gentle neck and shoulder stretches.",
            "Write down on physical paper 2 things you look forward to doing outdoors tomorrow morning.",
            "Sip water or herbal chamomile tea and rest your eyes from all blue-light screens."
        ]
        activity.safety_verified = True

    return activity
