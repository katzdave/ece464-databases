from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models import Animal
from app.data import get_all_animals, get_animal_by_id, search_animals


router = APIRouter(prefix="/api/animals", tags=["animals"])


@router.get("", response_model=list[Animal])
async def list_animals(
    animal_class: Optional[str] = Query(None, description="Filter by animal class"),
    habitat: Optional[str] = Query(None, description="Filter by habitat keyword"),
    species: Optional[str] = Query(None, description="Filter by species")
):
    """
    Get all animals with optional filters

    - **animal_class**: Filter by class (e.g., "Mammal", "Bird")
    - **habitat**: Filter by habitat keyword
    - **species**: Filter by species name
    """
    return get_all_animals(animal_class=animal_class, habitat=habitat, species=species)


@router.get("/search", response_model=list[Animal])
async def search(q: str = Query(..., description="Search query")):
    """
    Search animals by name, species, or interesting facts

    - **q**: Search query string
    """
    results = search_animals(q)
    return results


@router.get("/{animal_id}", response_model=Animal)
async def get_animal(animal_id: int):
    """
    Get a single animal by ID

    - **animal_id**: Unique animal identifier
    """
    animal = get_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal
