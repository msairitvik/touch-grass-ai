from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class CheckInRequest(BaseModel):
    mood: str = Field(..., description="Current mood: stressed, restless, bored, curious, calm")
    free_time_minutes: int = Field(..., ge=10, le=480, description="Available screen-free time in minutes")
    social_context: str = Field("alone", description="alone, with_friend, group")
    interests: List[str] = Field(default_factory=list, description="User interest tags")
    location: Optional[str] = Field(None, description="Optional city or neighborhood for genuine OSM discovery")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    weather_condition: str = Field("pleasant", description="pleasant, extreme_heat, stormy, chilly")
    time_of_day: Optional[str] = Field(None, description="morning, afternoon, evening, late_night")

class LocationInfo(BaseModel):
    name: str
    place_type: str
    address: Optional[str] = None
    osm_id: Optional[str] = None
    osm_url: Optional[str] = None
    is_genuine_osm: bool = False
    note: str = "Please check local daylight and opening hours independently."

class Activity(BaseModel):
    id: str
    title: str
    category: str
    estimated_minutes: int
    why_recommended: str
    safety_verified: bool = True
    safety_notes: Optional[str] = None
    steps: List[str]
    location_info: Optional[LocationInfo] = None

class RecommendationResponse(BaseModel):
    primary_activity: Activity
    backup_activity: Activity
    applied_safety_rules: List[str]
    safety_status: str
    places_source: str
    engine: str
    ai_personalized: bool = False
    ai_status: str = "deterministic_fallback"
    ai_note: Optional[str] = None
    timestamp: str
