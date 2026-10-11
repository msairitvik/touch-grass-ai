import uuid
from datetime import datetime, timezone
from app.models.schemas import CheckInRequest, Activity, RecommendationResponse, LocationInfo
from app.services.safety_rules import evaluate_safety_constraints, enforce_deterministic_safety
from app.services.osm_service import search_osm_place
from app.services.gemma_service import personalize_with_gemma

ACTIVITY_CATALOG = {
    # 1. Stressed / Overstimulated
    "stressed": [
        {
            "title": "Five-Senses Tree Canopy Immersion",
            "category": "outdoor",
            "base_minutes": 25,
            "why_recommended": "Overstimulation from digital feeds is quickly reset through natural fractal vision and ambient organic sound.",
            "steps": [
                "Leave your phone in your pocket on 'Do Not Disturb' or face-down.",
                "Walk to the nearest tree or green canopy and stand or sit beneath it.",
                "Identify: 5 distinct colors of foliage, 4 textures of bark or ground, 3 ambient non-mechanical sounds.",
                "Take 5 deep breaths feeling your feet anchored to the earth."
            ]
        },
        {
            "title": "Tactile Pen & Paper Freeform Scribble & Sketch",
            "category": "indoor",
            "base_minutes": 20,
            "why_recommended": "Moving physical graphite across textured paper engages motor cortex pathways that screen tapping leaves numb.",
            "steps": [
                "Place your phone completely out of sight in a closed drawer.",
                "Grab a blank sheet of paper and any pen, pencil, or crayon.",
                "Draw continuous unbroken lines without judging the outcome for 10 minutes.",
                "Notice the friction and sound of the tip against paper."
            ]
        }
    ],

    # 2. Restless / Energetic
    "restless": [
        {
            "title": "Rhythmic Neighborhood Perimeter Walk",
            "category": "outdoor",
            "base_minutes": 35,
            "why_recommended": "Converts agitated digital restlessness into kinetic blood flow and bilateral neurological stimulation.",
            "steps": [
                "Put shoes on and leave digital devices resting at home or in an unzipped bag.",
                "Pick a route around 4 blocks you do not usually pay attention to.",
                "Walk with brisk, steady strides without headphones.",
                "Spot 3 architectural details or garden flowers you've never noticed before."
            ]
        },
        {
            "title": "Analog Living Space Reset & Physical Movement",
            "category": "indoor",
            "base_minutes": 25,
            "why_recommended": "Physical interaction with tangible objects channels restless energy into satisfying spatial order.",
            "steps": [
                "Silence phone notifications and set it facedown across the room.",
                "Open a window to invite fresh air into the room.",
                "Pick one surface (desk, shelf, or counter) and mindfully clear and wipe it down.",
                "Do 10 mindful arm and shoulder rolls while looking out into the horizon."
            ]
        }
    ],

    # 3. Bored / Sluggish
    "bored": [
        {
            "title": "Public Library Wonder Expedition",
            "category": "indoor",
            "base_minutes": 45,
            "why_recommended": "Boredom is a craving for genuine surprise that algorithmic feeds flatten. Libraries offer serendipitous tactile discovery.",
            "steps": [
                "Visit your neighborhood public library or a nearby bookstore.",
                "Walk to a section you have never explored (e.g. Astronomy, Architecture, or Traditional Crafts).",
                "Pull three random hardcover books off the shelf purely based on spine design.",
                "Sit in a quiet chair and flip through 20 physical pages with your fingers."
            ]
        },
        {
            "title": "Micro-Botanical Scavenger Hunt",
            "category": "outdoor",
            "base_minutes": 30,
            "why_recommended": "Trains observation skills on microscopic real-world complexity rather than algorithmic novelty.",
            "steps": [
                "Step outside into a garden, park, or sidewalk verge.",
                "Look closely at ground level for 3 completely different leaf edge patterns (serrated, smooth, lobed).",
                "Feel the tactile difference between a smooth pebble and rough mulch.",
                "Take a moment to inhale the scent of damp earth."
            ]
        }
    ],

    # 4. Curious / Exploratory
    "curious": [
        {
            "title": "Cartography Without GPS: Hand-Drawn Map",
            "category": "outdoor",
            "base_minutes": 40,
            "why_recommended": "Digital navigation robs us of spatial memory; hand-mapping reconnects you with physical orientation.",
            "steps": [
                "Take a small pocket notebook and pencil with you.",
                "Walk 15 minutes away from your starting point without consulting any map app.",
                "Sit on a bench and draw a rough hand-sketch of your route with notable trees or houses.",
                "Walk back using only your visual memory of landmarks."
            ]
        },
        {
            "title": "Blind Sensory Beverage Tasting",
            "category": "indoor",
            "base_minutes": 20,
            "why_recommended": "Deepens acute olfactory and gustatory sensations without visual screen distraction.",
            "steps": [
                "Brew a fresh loose-leaf tea, coffee, or infused herbal water.",
                "Sit in a quiet spot without screens or audio.",
                "Close your eyes and inhale the steam for 60 seconds, noticing 3 subtle notes.",
                "Take slow sips, experiencing temperature and texture across your palate."
            ]
        }
    ],

    # 5. Calm / Reflective
    "calm": [
        {
            "title": "Quiet Bench Journaling & Cloud Observation",
            "category": "outdoor",
            "base_minutes": 30,
            "why_recommended": "Anchors peaceful mindsets into durable memories through open skies and ink on paper.",
            "steps": [
                "Take a physical notepad and pen to a nearby quiet park bench.",
                "Spend 5 minutes simply watching cloud movements or breeze in leaves.",
                "Write down three thoughts that feel grounded, spacious, or grateful.",
                "Allow yourself to sit in stillness without checking the time repeatedly."
            ]
        },
        {
            "title": "Gentle Floor Somatics & Breath Grounding",
            "category": "indoor",
            "base_minutes": 25,
            "why_recommended": "Releases screen-neck posture and regulates the nervous system through gravity and breath.",
            "steps": [
                "Lay a mat or blanket on the floor; phone stays completely out of reach.",
                "Lie flat on your back with knees bent and feet flat on the floor.",
                "Place both hands on your belly and breathe slowly: 4 seconds in, 6 seconds out.",
                "Gently rock your knees side to side feeling spinal articulation."
            ]
        }
    ]
}

async def generate_recommendations(request: CheckInRequest) -> RecommendationResponse:
    """
    Recommendation orchestrator:
    1. Computes deterministic safety rules.
    2. Builds safe baseline activities.
    3. Attempts local Gemma 2 AI personalization via Ollama.
    4. Enforces safety invariants (Gemma cannot override heat, storms, or late-night solo).
    5. Grounds with OpenStreetMap when a location is provided.
    6. Returns transparent AI and safety metadata.
    """
    applied_rules, constraints = evaluate_safety_constraints(request)

    # 1. Base activity candidates
    mood_key = request.mood.lower().strip()
    if mood_key not in ACTIVITY_CATALOG:
        mood_key = "calm"

    candidates = ACTIVITY_CATALOG[mood_key]
    primary_raw = candidates[0].copy()
    backup_raw = candidates[1].copy()

    if request.social_context in ["with_friend", "group"]:
        primary_raw["title"] = f"Shared: {primary_raw['title']}"
        primary_raw["why_recommended"] += " Shared offline presence creates real human bonding without screen mediation."
        backup_raw["title"] = f"Shared: {backup_raw['title']}"

    user_time = min(max(request.free_time_minutes, 10), 180)
    primary_minutes = min(primary_raw["base_minutes"], user_time)
    backup_minutes = min(backup_raw["base_minutes"], user_time)

    primary_activity = Activity(
        id=str(uuid.uuid4())[:8],
        title=primary_raw["title"],
        category=primary_raw["category"],
        estimated_minutes=primary_minutes,
        why_recommended=primary_raw["why_recommended"],
        safety_verified=True,
        steps=primary_raw["steps"]
    )

    backup_activity = Activity(
        id=str(uuid.uuid4())[:8],
        title=backup_raw["title"],
        category=backup_raw["category"],
        estimated_minutes=backup_minutes,
        why_recommended=backup_raw["why_recommended"],
        safety_verified=True,
        steps=backup_raw["steps"]
    )

    # 2. Attempt Gemma personalization
    gemma_data, ai_status_code, ai_status_note = await personalize_with_gemma(request, primary_activity, backup_activity, applied_rules)

    if gemma_data:
        primary_activity.title = gemma_data["primary"]["title"]
        primary_activity.why_recommended = gemma_data["primary"]["why_recommended"]
        primary_activity.steps = gemma_data["primary"]["steps"]
        
        backup_activity.title = gemma_data["backup"]["title"]
        backup_activity.why_recommended = gemma_data["backup"]["why_recommended"]
        backup_activity.steps = gemma_data["backup"]["steps"]

        engine_name = "Gemma 2 2B (Local Ollama)"
        ai_personalized = True
        ai_status = ai_status_code
        ai_note = ai_status_note
    else:
        engine_name = "Deterministic Safety Engine"
        ai_personalized = False
        ai_status = ai_status_code
        ai_note = ai_status_note

    # 3. NON-NEGOTIABLE SAFETY GUARANTEE:
    # Deterministic safety runs AFTER AI personalization to prevent any AI override!
    primary_activity = enforce_deterministic_safety(primary_activity, request, constraints)
    backup_activity = enforce_deterministic_safety(backup_activity, request, constraints)

    # 4. OpenStreetMap Grounding (Only when location is specified)
    places_source = "place_agnostic"
    if request.location and request.location.strip():
        hint = "park" if primary_activity.category in ["outdoor", "outdoor_sports"] else "library"
        location_info = await search_osm_place(request.location, place_type_hint=hint)
        if location_info:
            primary_activity.location_info = location_info
            places_source = "osm_live"
        else:
            places_source = "location_provided_no_osm_match"

    safety_status = "safety_override_applied" if len(applied_rules) > 0 else "guaranteed_safe"

    return RecommendationResponse(
        primary_activity=primary_activity,
        backup_activity=backup_activity,
        applied_safety_rules=applied_rules,
        safety_status=safety_status,
        places_source=places_source,
        engine=engine_name,
        ai_personalized=ai_personalized,
        ai_status=ai_status,
        ai_note=ai_note,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
