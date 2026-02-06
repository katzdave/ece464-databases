import React from 'react';
import './AnimalDetail.css';

function AnimalDetail({ animal, onClose }) {
  if (!animal) return null;

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
    <div className="animal-detail-overlay" onClick={onClose}>
      <div className="animal-detail" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>&times;</button>

        <div className="detail-header">
          <h1>{animal.name}</h1>
          <span className="class-badge">{animal.animal_class}</span>
        </div>

        <p className="species-name"><em>{animal.species}</em></p>

        <div className="detail-sections">
          <section className="detail-section">
            <h3>General Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <strong>Habitat:</strong>
                <span>{animal.habitat}</span>
              </div>
              <div className="info-item">
                <strong>Diet:</strong>
                <span>{animal.diet}</span>
              </div>
              <div className="info-item">
                <strong>Lifespan:</strong>
                <span>{animal.lifespan}</span>
              </div>
              <div className="info-item">
                <strong>Behavior:</strong>
                <span>{animal.behavior}</span>
              </div>
            </div>
          </section>

          <section className="detail-section">
            <h3>Physical Characteristics</h3>
            <div className="info-grid">
              <div className="info-item">
                <strong>Size:</strong>
                <span>{animal.size}</span>
              </div>
              <div className="info-item">
                <strong>Weight:</strong>
                <span>{animal.weight}</span>
              </div>
              <div className="info-item">
                <strong>Speed:</strong>
                <span>{animal.speed || 'N/A'}</span>
              </div>
              <div className="info-item">
                <strong>Color:</strong>
                <span>{animal.color}</span>
              </div>
            </div>
          </section>

          <section className="detail-section fun-fact-section">
            <h3>Did You Know?</h3>
            <p className="fun-fact">{animal.interesting_fact}</p>
          </section>

          <section className="detail-section">
            <h3>Conservation Status</h3>
            <div
              className="conservation-badge"
              style={{ backgroundColor: getStatusColor(animal.conservation_status) }}
            >
              {animal.conservation_status}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

export default AnimalDetail;
