import React from 'react';
import { Link } from 'react-router-dom';
import { formatDateWithTimezone } from '../utils/dateUtils';
import '../styles/EstateCard.css';

// Функциональный компонент со стрелочной функцией для презентационного компонента
const EstateCard = ({ estate, onView, onEdit, onDelete }) => {
  const handleViewClick = (e) => {
    // Only prevent default if onView handler is provided
    if (onView) {
      e.preventDefault();
      onView(estate);
    }
    // Otherwise let Link handle navigation normally
  };

  const handleEditClick = (e) => {
    e.preventDefault();
    if (onEdit) onEdit(estate);
  };

  const handleDeleteClick = (e) => {
    e.preventDefault();
    if (window.confirm('Are you sure you want to delete this estate?')) {
      if (onDelete) onDelete(estate._id);
    }
  };

  const costPerSquareMeter = estate.area > 0 
    ? (estate.cost / estate.area).toFixed(2) 
    : 0;

  return (
    <div className="estate-card">
      <div className="estate-card-image">
        {estate.image ? (
          <img src={`http://localhost:3001${estate.image}`} alt={estate.address} />
        ) : (
          <div className="no-image">No Image</div>
        )}
        <span className={`status-badge status-${estate.status}`}>
          {estate.status}
        </span>
      </div>
      <div className="estate-card-body">
        <h5 className="estate-card-title">{estate.address}</h5>
        <div className="estate-card-info">
          <div className="info-item">
            <i className="bi bi-currency-dollar"></i>
            <span>${estate.cost.toLocaleString()}</span>
          </div>
          <div className="info-item">
            <i className="bi bi-rulers"></i>
            <span>{estate.area} m²</span>
          </div>
          {estate.rooms && (
            <div className="info-item">
              <i className="bi bi-door-open"></i>
              <span>{estate.rooms} rooms</span>
            </div>
          )}
          <div className="info-item">
            <i className="bi bi-calculator"></i>
            <span>${costPerSquareMeter}/m²</span>
          </div>
        </div>
        <p className="estate-card-description">
          {estate.description?.substring(0, 100)}...
        </p>
        {estate.category && (
          <div className="estate-card-category">
            {estate.category.name}
          </div>
        )}
        {estate.createdAt && (
          <div className="estate-card-date">
            Added: {formatDateWithTimezone(estate.createdAt, 'MMM dd, yyyy')}
          </div>
        )}
        <div className="estate-card-actions">
          <Link 
            to={`/estates/${estate._id}`} 
            className="btn btn-primary btn-sm"
            onClick={handleViewClick}
          >
            View Details
          </Link>
          {onEdit && (
            <button 
              className="btn btn-secondary btn-sm"
              onClick={handleEditClick}
            >
              Edit
            </button>
          )}
          {onDelete && (
            <button 
              className="btn btn-danger btn-sm"
              onClick={handleDeleteClick}
            >
              Delete
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default EstateCard;

