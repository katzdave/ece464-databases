import React, { useState } from 'react';
import './SearchBar.css';

function SearchBar({ onSearch, onFilterChange, filters }) {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      onSearch(searchQuery);
    }
  };

  const handleClear = () => {
    setSearchQuery('');
    onFilterChange({ animal_class: '', habitat: '', species: '' });
  };

  return (
    <div className="search-bar">
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Search animals by name, species, or facts..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="search-button">Search</button>
        <button type="button" onClick={handleClear} className="clear-button">Clear</button>
      </form>

      <div className="filters">
        <select
          value={filters.animal_class}
          onChange={(e) => onFilterChange({ ...filters, animal_class: e.target.value })}
          className="filter-select"
        >
          <option value="">All Classes</option>
          <option value="Mammal">Mammal</option>
          <option value="Bird">Bird</option>
          <option value="Reptile">Reptile</option>
          <option value="Amphibian">Amphibian</option>
          <option value="Fish">Fish</option>
          <option value="Invertebrate">Invertebrate</option>
        </select>

        <input
          type="text"
          placeholder="Filter by habitat..."
          value={filters.habitat}
          onChange={(e) => onFilterChange({ ...filters, habitat: e.target.value })}
          className="filter-input"
        />
      </div>
    </div>
  );
}

export default SearchBar;
