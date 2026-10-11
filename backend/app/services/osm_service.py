import httpx
from typing import Optional
from app.models.schemas import LocationInfo

OSM_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "TouchGrassAI/1.0 (Hackathon Digital Wellbeing Project; contact: support@touchgrass.local)"

async def search_osm_place(query_location: str, place_type_hint: str = "park") -> Optional[LocationInfo]:
    """
    Queries real OpenStreetMap data via Nominatim when a user provides a location.
    Never invents events, attendance, opening hours, or venue safety.
    """
    if not query_location or not query_location.strip():
        return None

    search_query = f"{place_type_hint} {query_location.strip()}"
    params = {
        "q": search_query,
        "format": "jsonv2",
        "limit": 1,
        "addressdetails": 1
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(OSM_NOMINATIM_URL, params=params, headers=headers)
            if resp.status_code == 200:
                results = resp.json()
                if results and len(results) > 0:
                    top = results[0]
                    osm_type = top.get("osm_type", "node")
                    osm_id = top.get("osm_id")
                    osm_url = f"https://www.openstreetmap.org/{osm_type}/{osm_id}" if osm_id else None
                    name = top.get("name") or top.get("display_name", "").split(",")[0] or f"Public {place_type_hint.title()}"
                    address = top.get("display_name")
                    return LocationInfo(
                        name=name,
                        place_type=place_type_hint,
                        address=address,
                        osm_id=str(osm_id) if osm_id else None,
                        osm_url=osm_url,
                        is_genuine_osm=True,
                        note="Real OpenStreetMap verified place. Opening hours and real-time conditions are not tracked—please check independently."
                    )
    except Exception:
        # Fall back gracefully if network is unavailable or OSM times out
        pass

    return None
