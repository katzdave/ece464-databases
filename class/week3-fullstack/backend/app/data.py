from app.models import Animal, AnimalClass, Diet, ConservationStatus, AnimalStats
from typing import Optional


# Sample animal data
ANIMALS = [
    Animal(
        id=1,
        name="African Elephant",
        species="Loxodonta africana",
        animal_class=AnimalClass.MAMMAL,
        habitat="African savannas and forests",
        diet=Diet.HERBIVORE,
        lifespan="60-70 years",
        behavior="Social, lives in matriarchal herds",
        size="3-4 meters tall",
        weight="4,000-7,000 kg",
        speed="40 km/h",
        color="Gray",
        interesting_fact="Elephants are the largest land animals and have excellent memory",
        conservation_status=ConservationStatus.ENDANGERED
    ),
    Animal(
        id=2,
        name="Bald Eagle",
        species="Haliaeetus leucocephalus",
        animal_class=AnimalClass.BIRD,
        habitat="Near large bodies of water in North America",
        diet=Diet.CARNIVORE,
        lifespan="20-30 years",
        behavior="Solitary or pairs, territorial",
        size="70-102 cm length, 1.8-2.3 m wingspan",
        weight="3-6.3 kg",
        speed="120-160 km/h diving",
        color="Brown body with white head and tail",
        interesting_fact="The bald eagle is the national bird of the United States",
        conservation_status=ConservationStatus.LEAST_CONCERN
    ),
    Animal(
        id=3,
        name="Bengal Tiger",
        species="Panthera tigris tigris",
        animal_class=AnimalClass.MAMMAL,
        habitat="Indian subcontinent forests and grasslands",
        diet=Diet.CARNIVORE,
        lifespan="8-10 years",
        behavior="Solitary, territorial apex predator",
        size="2.7-3.1 meters long",
        weight="180-260 kg",
        speed="49-65 km/h",
        color="Orange with black stripes",
        interesting_fact="Each tiger's stripe pattern is unique, like a fingerprint",
        conservation_status=ConservationStatus.ENDANGERED
    ),
    Animal(
        id=4,
        name="Green Sea Turtle",
        species="Chelonia mydas",
        animal_class=AnimalClass.REPTILE,
        habitat="Tropical and subtropical oceans worldwide",
        diet=Diet.HERBIVORE,
        lifespan="80+ years",
        behavior="Solitary, migrates long distances",
        size="1-1.2 meters long",
        weight="65-130 kg",
        speed="35 km/h swimming",
        color="Green and brown",
        interesting_fact="Named for the green color of their fat, not their shells",
        conservation_status=ConservationStatus.ENDANGERED
    ),
    Animal(
        id=5,
        name="Giant Panda",
        species="Ailuropoda melanoleuca",
        animal_class=AnimalClass.MAMMAL,
        habitat="Mountain forests in central China",
        diet=Diet.HERBIVORE,
        lifespan="20 years",
        behavior="Solitary, spends 12+ hours eating bamboo",
        size="1.2-1.9 meters long",
        weight="70-120 kg",
        speed="32 km/h",
        color="Black and white",
        interesting_fact="Pandas eat up to 38 kg of bamboo per day",
        conservation_status=ConservationStatus.VULNERABLE
    ),
    Animal(
        id=6,
        name="Red Poison Dart Frog",
        species="Oophaga pumilio",
        animal_class=AnimalClass.AMPHIBIAN,
        habitat="Rainforests of Central America",
        diet=Diet.CARNIVORE,
        lifespan="4-6 years",
        behavior="Diurnal, territorial",
        size="17-24 mm",
        weight="3-5 grams",
        speed=None,
        color="Bright red or orange",
        interesting_fact="Their bright colors warn predators of their toxicity",
        conservation_status=ConservationStatus.LEAST_CONCERN
    ),
    Animal(
        id=7,
        name="Great White Shark",
        species="Carcharodon carcharias",
        animal_class=AnimalClass.FISH,
        habitat="Coastal waters worldwide",
        diet=Diet.CARNIVORE,
        lifespan="70+ years",
        behavior="Solitary apex predator",
        size="4-6 meters long",
        weight="680-1,100 kg",
        speed="56 km/h",
        color="Gray with white underside",
        interesting_fact="Can detect a single drop of blood in 100 liters of water",
        conservation_status=ConservationStatus.VULNERABLE
    ),
    Animal(
        id=8,
        name="Emperor Penguin",
        species="Aptenodytes forsteri",
        animal_class=AnimalClass.BIRD,
        habitat="Antarctic ice and surrounding waters",
        diet=Diet.CARNIVORE,
        lifespan="15-20 years",
        behavior="Colonial, mates for life",
        size="100-130 cm tall",
        weight="22-45 kg",
        speed="9 km/h swimming",
        color="Black, white, and yellow",
        interesting_fact="Males incubate eggs in harsh Antarctic winter for 64 days without eating",
        conservation_status=ConservationStatus.LEAST_CONCERN
    ),
    Animal(
        id=9,
        name="Monarch Butterfly",
        species="Danaus plexippus",
        animal_class=AnimalClass.INVERTEBRATE,
        habitat="North and Central America",
        diet=Diet.HERBIVORE,
        lifespan="2-6 weeks (adults)",
        behavior="Migratory, travels up to 4,800 km",
        size="8.9-10.2 cm wingspan",
        weight="0.5 grams",
        speed="40 km/h",
        color="Orange and black",
        interesting_fact="Migration generation lives 8 months, much longer than other generations",
        conservation_status=ConservationStatus.VULNERABLE
    ),
    Animal(
        id=10,
        name="Red Kangaroo",
        species="Osphranter rufus",
        animal_class=AnimalClass.MAMMAL,
        habitat="Australian grasslands and deserts",
        diet=Diet.HERBIVORE,
        lifespan="12-18 years",
        behavior="Social, lives in groups called mobs",
        size="1.3-1.6 meters tall",
        weight="18-95 kg",
        speed="70 km/h hopping",
        color="Reddish-brown",
        interesting_fact="Can jump 3 meters high and 9 meters long in a single leap",
        conservation_status=ConservationStatus.LEAST_CONCERN
    ),
]


def get_all_animals(
    animal_class: Optional[str] = None,
    habitat: Optional[str] = None,
    species: Optional[str] = None
) -> list[Animal]:
    """Get all animals with optional filters"""
    filtered = ANIMALS

    if animal_class:
        filtered = [a for a in filtered if a.animal_class.value.lower() == animal_class.lower()]

    if habitat:
        filtered = [a for a in filtered if habitat.lower() in a.habitat.lower()]

    if species:
        filtered = [a for a in filtered if species.lower() in a.species.lower()]

    return filtered


def get_animal_by_id(animal_id: int) -> Optional[Animal]:
    """Get a single animal by ID"""
    for animal in ANIMALS:
        if animal.id == animal_id:
            return animal
    return None


def search_animals(query: str) -> list[Animal]:
    """Search animals by name, species, or interesting facts"""
    query_lower = query.lower()
    results = []

    for animal in ANIMALS:
        if (query_lower in animal.name.lower() or
            query_lower in animal.species.lower() or
            query_lower in animal.interesting_fact.lower()):
            results.append(animal)

    return results


def get_stats() -> AnimalStats:
    """Calculate statistics about the animal collection"""
    by_class = {}
    by_diet = {}
    by_habitat = {}
    by_conservation = {}

    for animal in ANIMALS:
        # Count by class
        class_name = animal.animal_class.value
        by_class[class_name] = by_class.get(class_name, 0) + 1

        # Count by diet
        diet_name = animal.diet.value
        by_diet[diet_name] = by_diet.get(diet_name, 0) + 1

        # Count by habitat (simplified - just use first word)
        habitat_key = animal.habitat.split()[0]
        by_habitat[habitat_key] = by_habitat.get(habitat_key, 0) + 1

        # Count by conservation status
        status_name = animal.conservation_status.value
        by_conservation[status_name] = by_conservation.get(status_name, 0) + 1

    return AnimalStats(
        total_animals=len(ANIMALS),
        by_class=by_class,
        by_diet=by_diet,
        by_habitat=by_habitat,
        by_conservation_status=by_conservation
    )
