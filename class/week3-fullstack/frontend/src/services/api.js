const API_BASE_URL = 'http://localhost:8888';

class AnimalAPI {
  async getAllAnimals(filters = {}) {
    const params = new URLSearchParams();
    if (filters.animal_class) params.append('animal_class', filters.animal_class);
    if (filters.habitat) params.append('habitat', filters.habitat);
    if (filters.species) params.append('species', filters.species);

    const url = `${API_BASE_URL}/api/animals${params.toString() ? '?' + params.toString() : ''}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch animals');
    return await response.json();
  }

  async getAnimalById(id) {
    const response = await fetch(`${API_BASE_URL}/api/animals/${id}`);
    if (!response.ok) {
      if (response.status === 404) throw new Error('Animal not found');
      throw new Error('Failed to fetch animal');
    }
    return await response.json();
  }

  async searchAnimals(query) {
    const response = await fetch(`${API_BASE_URL}/api/animals/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error('Search failed');
    return await response.json();
  }

  async getStats() {
    const response = await fetch(`${API_BASE_URL}/api/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return await response.json();
  }
}

export default new AnimalAPI();
