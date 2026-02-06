import pytest
from pydantic import ValidationError
from app.models import Animal, AnimalClass, Diet, ConservationStatus


def test_valid_animal():
    """Test creating a valid animal"""
    animal = Animal(
        id=1,
        name="Test Animal",
        species="Testus animalus",
        animal_class=AnimalClass.MAMMAL,
        habitat="Test habitat",
        diet=Diet.HERBIVORE,
        lifespan="10 years",
        behavior="Friendly",
        size="1 meter",
        weight="50 kg",
        speed="30 km/h",
        color="Brown",
        interesting_fact="This is a test animal",
        conservation_status=ConservationStatus.LEAST_CONCERN
    )

    assert animal.id == 1
    assert animal.name == "Test Animal"
    assert animal.animal_class == AnimalClass.MAMMAL


def test_animal_without_optional_speed():
    """Test creating an animal without speed (optional field)"""
    animal = Animal(
        id=2,
        name="Slow Animal",
        species="Slowus creature",
        animal_class=AnimalClass.REPTILE,
        habitat="Swamp",
        diet=Diet.CARNIVORE,
        lifespan="20 years",
        behavior="Sluggish",
        size="2 meters",
        weight="100 kg",
        color="Green",
        interesting_fact="Very slow",
        conservation_status=ConservationStatus.VULNERABLE
    )

    assert animal.speed is None


def test_invalid_animal_class():
    """Test that invalid animal class raises validation error"""
    with pytest.raises(ValidationError):
        Animal(
            id=3,
            name="Invalid Animal",
            species="Invalid species",
            animal_class="InvalidClass",  # Invalid enum value
            habitat="Nowhere",
            diet=Diet.OMNIVORE,
            lifespan="5 years",
            behavior="Confused",
            size="1 meter",
            weight="20 kg",
            color="Gray",
            interesting_fact="Doesn't exist",
            conservation_status=ConservationStatus.LEAST_CONCERN
        )


def test_missing_required_field():
    """Test that missing required field raises validation error"""
    with pytest.raises(ValidationError):
        Animal(
            id=4,
            name="Incomplete Animal",
            # Missing species and other required fields
            animal_class=AnimalClass.BIRD,
            habitat="Sky"
        )


def test_enum_values():
    """Test that enum values are correct"""
    assert AnimalClass.MAMMAL.value == "Mammal"
    assert Diet.CARNIVORE.value == "Carnivore"
    assert ConservationStatus.ENDANGERED.value == "Endangered"
