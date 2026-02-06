import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Animal Explorer" in data["message"]


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_all_animals():
    """Test listing all animals"""
    response = client.get("/api/animals")
    assert response.status_code == 200
    animals = response.json()
    assert len(animals) == 10
    assert animals[0]["name"] == "African Elephant"


def test_filter_by_class():
    """Test filtering animals by class"""
    response = client.get("/api/animals?animal_class=Mammal")
    assert response.status_code == 200
    animals = response.json()
    assert len(animals) == 4  # Elephant, Tiger, Panda, Kangaroo
    for animal in animals:
        assert animal["animal_class"] == "Mammal"


def test_filter_by_habitat():
    """Test filtering animals by habitat keyword"""
    response = client.get("/api/animals?habitat=forest")
    assert response.status_code == 200
    animals = response.json()
    assert len(animals) > 0
    for animal in animals:
        assert "forest" in animal["habitat"].lower()


def test_get_animal_by_id():
    """Test getting a single animal by ID"""
    response = client.get("/api/animals/1")
    assert response.status_code == 200
    animal = response.json()
    assert animal["id"] == 1
    assert animal["name"] == "African Elephant"
    assert animal["species"] == "Loxodonta africana"


def test_get_nonexistent_animal():
    """Test getting an animal that doesn't exist"""
    response = client.get("/api/animals/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_search_animals():
    """Test searching animals"""
    response = client.get("/api/animals/search?q=tiger")
    assert response.status_code == 200
    animals = response.json()
    assert len(animals) >= 1
    assert any("tiger" in animal["name"].lower() for animal in animals)


def test_search_by_fact():
    """Test searching animals by interesting fact"""
    response = client.get("/api/animals/search?q=stripe")
    assert response.status_code == 200
    animals = response.json()
    assert len(animals) >= 1


def test_search_no_results():
    """Test search with no matching results"""
    response = client.get("/api/animals/search?q=dinosaur")
    assert response.status_code == 200
    animals = response.json()
    assert len(animals) == 0


def test_get_stats():
    """Test getting statistics"""
    response = client.get("/api/stats")
    assert response.status_code == 200
    stats = response.json()

    assert stats["total_animals"] == 10
    assert "by_class" in stats
    assert "by_diet" in stats
    assert "by_habitat" in stats
    assert "by_conservation_status" in stats

    # Check that mammals count is correct (Elephant, Tiger, Panda, Kangaroo)
    assert stats["by_class"]["Mammal"] == 4


def test_stats_structure():
    """Test that stats have correct structure"""
    response = client.get("/api/stats")
    stats = response.json()

    # Verify diet categories
    assert "Carnivore" in stats["by_diet"]
    assert "Herbivore" in stats["by_diet"]

    # Verify conservation statuses
    assert "Least Concern" in stats["by_conservation_status"]
    assert "Endangered" in stats["by_conservation_status"]
