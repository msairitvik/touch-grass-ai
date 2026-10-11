from fastapi import APIRouter, HTTPException
from app.models.schemas import CheckInRequest, RecommendationResponse
from app.services.recommender import generate_recommendations

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.post("", response_model=RecommendationResponse)
async def get_recommendations(request: CheckInRequest):
    """
    Generate grounded, screen-free activity recommendations
    with strictly enforced deterministic safety rules and optional OSM places.
    """
    try:
        recommendations = await generate_recommendations(request)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation processing error: {str(e)}")
