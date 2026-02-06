from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class AnimalClass(str, Enum):
    """Classification of animals by their biological class"""
    MAMMAL = "Mammal"
    BIRD = "Bird"
    REPTILE = "Reptile"
    AMPHIBIAN = "Amphibian"
    FISH = "Fish"
    INVERTEBRATE = "Invertebrate"


class Diet(str, Enum):
    """Dietary classification"""
    CARNIVORE = "Carnivore"
    HERBIVORE = "Herbivore"
    OMNIVORE = "Omnivore"


class ConservationStatus(str, Enum):
    """IUCN Conservation Status"""
    LEAST_CONCERN = "Least Concern"
    VULNERABLE = "Vulnerable"
    ENDANGERED = "Endangered"
    CRITICALLY_ENDANGERED = "Critically Endangered"


class Animal(BaseModel):
    """Complete animal data model"""
    # Basic Information
    id: int
    name: str
    species: str
    animal_class: AnimalClass
    habitat: str

    # Diet and Behavior
    diet: Diet
    lifespan: str = Field(description="Average lifespan in the wild")
    behavior: str = Field(description="Typical behavioral characteristics")

    # Physical Characteristics
    size: str = Field(description="Typical size/length")
    weight: str = Field(description="Typical weight")
    speed: Optional[str] = Field(default=None, description="Maximum speed if applicable")
    color: str = Field(description="Primary coloration")

    # Fun Facts
    interesting_fact: str
    conservation_status: ConservationStatus


class AnimalStats(BaseModel):
    """Statistics about the animal collection"""
    total_animals: int
    by_class: dict[str, int]
    by_diet: dict[str, int]
    by_habitat: dict[str, int]
    by_conservation_status: dict[str, int]
