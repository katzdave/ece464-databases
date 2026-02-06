import React from 'react';
import './AnimalCard.css';

function AnimalCard({ animal, onSelect }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'Least Concern':
        return '#4CAF50';
      case 'Vulnerable':
        return '#FF9800';
      case 'Endangered':
        return '#F44336';
      case 'Critically Endangered':
        return '#B71C1C';
      default:
        return '#757575';
    }
  };

  return (
    <div className="animal-card" onClick={() => onSelect(animal)}>
      <div className="animal-card-header">
        <h3>{animal.name}</h3>
        <span className="animal-class">{animal.animal_class}</span>
      </div>

      <div className="animal-card-body">
        <p className="species"><em>{animal.species}</em></p>
        <p className="habitat"><strong>Habitat:</strong> {animal.habitat}</p>
        <p className="diet"><strong>Diet:</strong> {animal.diet}</p>

        <div
          className="conservation-status"
          style={{ backgroundColor: getStatusColor(animal.conservation_status) }}
        >
          {animal.conservation_status}
        </div>
      </div>

      <div className="animal-card-footer">
        <button className="view-details-btn">View Details</button>
      </div>
    </div>
  );
}

export default AnimalCard;
