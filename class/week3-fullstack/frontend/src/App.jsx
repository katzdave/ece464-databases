import React, { useState, useEffect } from 'react';
import api from './services/api';
import SearchBar from './components/SearchBar';
import AnimalGrid from './components/AnimalGrid';
import AnimalDetail from './components/AnimalDetail';
import StatsPanel from './components/StatsPanel';
import './App.css';

function App() {
  const [animals, setAnimals] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedAnimal, setSelectedAnimal] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [view, setView] = useState('grid'); // 'grid' or 'stats'
  const [filters, setFilters] = useState({
    animal_class: '',
    habitat: '',
    species: ''
  });

  useEffect(() => {
    loadAnimals();
    loadStats();
  }, []);

  useEffect(() => {
    loadAnimals();
  }, [filters]);

  const loadAnimals = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getAllAnimals(filters);
      setAnimals(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const data = await api.getStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  const handleSearch = async (query) => {
    try {
      setLoading(true);
      setError(null);
      const results = await api.searchAnimals(query);
      setAnimals(results);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const handleAnimalSelect = (animal) => {
    setSelectedAnimal(animal);
  };

  const handleCloseDetail = () => {
    setSelectedAnimal(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Animal Explorer</h1>
        <p>Discover the fascinating world of animals</p>
      </header>

      <nav className="app-nav">
        <button
          className={view === 'grid' ? 'active' : ''}
          onClick={() => setView('grid')}
        >
          Browse Animals
        </button>
        <button
          className={view === 'stats' ? 'active' : ''}
          onClick={() => setView('stats')}
        >
          Statistics
        </button>
      </nav>

      <main className="app-content">
        {view === 'grid' ? (
          <>
            <SearchBar
              onSearch={handleSearch}
              onFilterChange={handleFilterChange}
              filters={filters}
            />
            <AnimalGrid
              animals={animals}
              onAnimalSelect={handleAnimalSelect}
              loading={loading}
              error={error}
            />
          </>
        ) : (
          <StatsPanel stats={stats} />
        )}
      </main>

      {selectedAnimal && (
        <AnimalDetail
          animal={selectedAnimal}
          onClose={handleCloseDetail}
        />
      )}

      <footer className="app-footer">
        <p>Animal Explorer - A full-stack web application for ECE464</p>
      </footer>
    </div>
  );
}

export default App;
