import React from 'react';
import './StatsPanel.css';

function StatsPanel({ stats }) {
  if (!stats) {
    return <div className="stats-panel">Loading statistics...</div>;
  }

  return (
    <div className="stats-panel">
      <h2>Animal Kingdom Statistics</h2>

      <div className="stats-grid">
        <div className="stat-card total">
          <h3>Total Animals</h3>
          <p className="stat-number">{stats.total_animals}</p>
        </div>

        <div className="stat-section">
          <h3>By Animal Class</h3>
          <div className="stat-bars">
            {Object.entries(stats.by_class).map(([className, count]) => (
              <div key={className} className="stat-bar-item">
                <span className="stat-label">{className}</span>
                <div className="stat-bar">
                  <div
                    className="stat-bar-fill class"
                    style={{ width: `${(count / stats.total_animals) * 100}%` }}
                  ></div>
                </div>
                <span className="stat-count">{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="stat-section">
          <h3>By Diet</h3>
          <div className="stat-bars">
            {Object.entries(stats.by_diet).map(([diet, count]) => (
              <div key={diet} className="stat-bar-item">
                <span className="stat-label">{diet}</span>
                <div className="stat-bar">
                  <div
                    className="stat-bar-fill diet"
                    style={{ width: `${(count / stats.total_animals) * 100}%` }}
                  ></div>
                </div>
                <span className="stat-count">{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="stat-section">
          <h3>Conservation Status</h3>
          <div className="stat-bars">
            {Object.entries(stats.by_conservation_status).map(([status, count]) => (
              <div key={status} className="stat-bar-item">
                <span className="stat-label">{status}</span>
                <div className="stat-bar">
                  <div
                    className="stat-bar-fill conservation"
                    style={{
                      width: `${(count / stats.total_animals) * 100}%`,
                      backgroundColor: getConservationColor(status)
                    }}
                  ></div>
                </div>
                <span className="stat-count">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function getConservationColor(status) {
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
}

export default StatsPanel;
