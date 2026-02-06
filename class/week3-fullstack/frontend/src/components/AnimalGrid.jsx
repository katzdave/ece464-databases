import React from 'react';
import AnimalCard from './AnimalCard';
import './AnimalGrid.css';

function AnimalGrid({ animals, onAnimalSelect, loading, error }) {
  if (loading) {
    return <div className="message">Loading animals...</div>;
  }

  if (error) {
    return <div className="message error">Error: {error}</div>;
  }

  if (animals.length === 0) {
    return <div className="message">No animals found. Try a different search or filter.</div>;
  }

  return (
    <div className="animal-grid">
      {animals.map(animal => (
        <AnimalCard
          key={animal.id}
          animal={animal}
          onSelect={onAnimalSelect}
        />
      ))}
    </div>
  );
}

export default AnimalGrid;
