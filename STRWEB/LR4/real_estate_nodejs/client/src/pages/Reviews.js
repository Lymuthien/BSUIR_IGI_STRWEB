import React, { useState, useEffect, useCallback } from 'react';
import { reviewsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { formatDateWithTimezone } from '../utils/dateUtils';
import '../styles/Reviews.css';

const Reviews = () => {
  const { isAuthenticated } = useAuth();
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    rating: 5,
    text: '',
    estate: ''
  });

  const loadReviews = useCallback(async () => {
    setLoading(true);
    try {
      const response = await reviewsAPI.getAll();
      setReviews(response.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadReviews();
  }, [loadReviews]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'rating' ? parseInt(value) : value
    }));
  };

  const handleFocus = (e) => {
    e.target.classList.remove('is-invalid');
  };

  const handleBlur = (e) => {
    const { name, value } = e.target;
    if (name === 'text' && !value.trim()) {
      e.target.setCustomValidity('Review text is required');
      e.target.classList.add('is-invalid');
    } else {
      e.target.setCustomValidity('');
      e.target.classList.remove('is-invalid');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.target.tagName === 'TEXTAREA' && !e.shiftKey) {
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isAuthenticated) {
      alert('Please login to submit a review');
      return;
    }

    try {
      // Убираем поле estate, если оно пустое (сервер ожидает либо валидный ID, либо отсутствие поля)
      const submitData = { ...formData };
      if (!submitData.estate || submitData.estate.trim() === '') {
        delete submitData.estate;
      }
      
      await reviewsAPI.create(submitData);
      setFormData({ rating: 5, text: '', estate: '' });
      setShowForm(false);
      loadReviews();
    } catch (err) {
      alert(err.response?.data?.message || err.response?.data?.errors?.[0]?.msg || 'Error submitting review');
    }
  };

  return (
    <div className="reviews-page">
      <div className="container">
        <h1>Reviews</h1>
        
        {isAuthenticated && (
          <div className="reviews-actions mb-4">
            <button 
              onClick={() => setShowForm(!showForm)}
              className="btn btn-primary"
            >
              {showForm ? 'Cancel' : 'Write a Review'}
            </button>
          </div>
        )}

        {showForm && isAuthenticated && (
          <form onSubmit={handleSubmit} className="review-form mb-4">
            <div className="form-group">
              <label>Rating</label>
              <select
                name="rating"
                value={formData.rating}
                onChange={handleChange}
                className="form-control"
              >
                {[5, 4, 3, 2, 1].map(rating => (
                  <option key={rating} value={rating}>
                    {rating} {rating === 5 ? 'stars' : 'star' + (rating > 1 ? 's' : '')}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Review Text</label>
              <textarea
                name="text"
                value={formData.text}
                onChange={handleChange}
                onFocus={handleFocus}
                onBlur={handleBlur}
                onKeyPress={handleKeyPress}
                rows="4"
                className="form-control"
                required
                placeholder="Write your review here..."
              />
            </div>
            <div className="form-group">
              <label>Estate ID (optional)</label>
              <input
                type="text"
                name="estate"
                value={formData.estate}
                onChange={handleChange}
                className="form-control"
                placeholder="Leave empty for general review"
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Submit Review
            </button>
          </form>
        )}

        {loading && (
          <div className="text-center">
            <div className="spinner-border" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        )}

        {error && (
          <div className="alert alert-danger">{error}</div>
        )}

        {!loading && !error && (
          <div className="reviews-list">
            {reviews.length === 0 ? (
              <p className="text-center">No reviews yet. Be the first to review!</p>
            ) : (
              reviews.map(review => (
                <div key={review._id} className="review-card">
                  <div className="review-header">
                    <div>
                      <strong>{review.user?.firstName} {review.user?.lastName}</strong>
                      {review.estate && (
                        <span className="review-estate">
                          - {review.estate.address}
                        </span>
                      )}
                    </div>
                    <div className="rating">
                      {'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}
                    </div>
                  </div>
                  <p className="review-text">{review.text}</p>
                  <div className="review-footer">
                    <small>{formatDateWithTimezone(review.createdAt, 'MMM dd, yyyy HH:mm')}</small>
                    {review.updatedAt && review.updatedAt !== review.createdAt && (
                      <small className="text-muted">
                        (Updated: {formatDateWithTimezone(review.updatedAt, 'MMM dd, yyyy')})
                      </small>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Reviews;

