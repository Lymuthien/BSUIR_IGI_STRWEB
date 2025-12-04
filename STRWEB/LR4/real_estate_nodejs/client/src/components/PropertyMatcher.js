import React, { useState } from 'react';
import { estatesAPI } from '../services/api';
import '../styles/PropertyMatcher.css';

// Функциональный компонент для подбора объектов
const PropertyMatcher = () => {
  const [criteria, setCriteria] = useState({
    minCost: '',
    maxCost: '',
    minArea: '',
    maxArea: '',
    rooms: ''
  });
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCriteria(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleMatch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const params = {};
      if (criteria.minCost) params.minCost = criteria.minCost;
      if (criteria.maxCost) params.maxCost = criteria.maxCost;
      if (criteria.minArea) params.minArea = criteria.minArea;
      if (criteria.maxArea) params.maxArea = criteria.maxArea;

      const response = await estatesAPI.getAll(params);
      let filtered = response.data.estates || [];

      // Filter by rooms if specified
      if (criteria.rooms) {
        filtered = filtered.filter(e => e.rooms === parseInt(criteria.rooms));
      }

      setMatches(filtered);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setCriteria({
      minCost: '',
      maxCost: '',
      minArea: '',
      maxArea: '',
      rooms: ''
    });
    setMatches([]);
    setError(null);
  };

  return (
    <div className="property-matcher">
      <h3>Find Your Perfect Property</h3>
      <form onSubmit={handleMatch} className="matcher-form">
        <div className="form-grid">
          <div className="form-group">
            <label>Min Cost ($)</label>
            <input
              type="number"
              name="minCost"
              value={criteria.minCost}
              onChange={handleInputChange}
              className="form-control"
              placeholder="0"
            />
          </div>
          <div className="form-group">
            <label>Max Cost ($)</label>
            <input
              type="number"
              name="maxCost"
              value={criteria.maxCost}
              onChange={handleInputChange}
              className="form-control"
              placeholder="1000000"
            />
          </div>
          <div className="form-group">
            <label>Min Area (m²)</label>
            <input
              type="number"
              name="minArea"
              value={criteria.minArea}
              onChange={handleInputChange}
              className="form-control"
              placeholder="0"
            />
          </div>
          <div className="form-group">
            <label>Max Area (m²)</label>
            <input
              type="number"
              name="maxArea"
              value={criteria.maxArea}
              onChange={handleInputChange}
              className="form-control"
              placeholder="500"
            />
          </div>
          <div className="form-group">
            <label>Rooms</label>
            <select
              name="rooms"
              value={criteria.rooms}
              onChange={handleInputChange}
              className="form-control"
            >
              <option value="">Any</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4+</option>
            </select>
          </div>
        </div>
        <div className="form-actions">
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Searching...' : 'Find Properties'}
          </button>
          <button type="button" onClick={handleReset} className="btn btn-secondary">
            Reset
          </button>
        </div>
      </form>

      {error && (
        <div className="alert alert-danger">{error}</div>
      )}

      {matches.length > 0 && (
        <div className="matches-results">
          <h4>Found {matches.length} properties:</h4>
          <div className="matches-list">
            {matches.map(estate => (
              <div key={estate._id} className="match-item">
                <strong>{estate.address}</strong> - 
                ${estate.cost.toLocaleString()} - 
                {estate.area} m² - 
                {estate.rooms || 'N/A'} rooms
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PropertyMatcher;

