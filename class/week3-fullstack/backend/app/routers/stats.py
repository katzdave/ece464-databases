from fastapi import APIRouter
from app.models import AnimalStats
from app.data import get_stats


router = APIRouter(prefix="/api/stats", tags=["statistics"])


@router.get("", response_model=AnimalStats)
async def get_statistics():
    """
    Get statistics about the animal collection

    Returns counts by:
    - Animal class
    - Diet type
    - Habitat
    - Conservation status
    """
    return get_stats()
