import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { estatesAPI, reviewsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import DateTimeDisplay from '../components/DateTimeDisplay';
import { formatDateWithTimezone } from '../utils/dateUtils';
import '../styles/EstateDetail.css';

// Функциональный компонент для просмотра деталей объекта
const EstateDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [estate, setEstate] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [reviewForm, setReviewForm] = useState({
    rating: 5,
    text: ''
  });
  const [analyzingImage, setAnalyzingImage] = useState(false);
  const [imageAnalysis, setImageAnalysis] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  const loadEstate = useCallback(async () => {
    try {
      const response = await estatesAPI.getById(id);
      setEstate(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [id]);

  const loadReviews = useCallback(async () => {
    try {
      const response = await reviewsAPI.getAll({ estate: id });
      setReviews(response.data || []);
    } catch (err) {
      console.error('Error loading reviews:', err);
    }
  }, [id]);

  useEffect(() => {
    loadEstate();
    loadReviews();
  }, [loadEstate, loadReviews]);

  useEffect(() => {
    if (estate?.aiAnalysis) {
      setImageAnalysis(estate.aiAnalysis);
    }
  }, [estate]);

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      await reviewsAPI.create({
        ...reviewForm,
        estate: id
      });
      setReviewForm({ rating: 5, text: '' });
      setShowReviewForm(false);
      loadReviews();
    } catch (err) {
      alert(err.response?.data?.message || 'Error submitting review');
    }
  };

  const handleReviewChange = (e) => {
    const { name, value } = e.target;
    setReviewForm(prev => ({
      ...prev,
      [name]: name === 'rating' ? parseInt(value) : value
    }));
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this estate?')) {
      return;
    }

    try {
      await estatesAPI.delete(id);
      navigate('/catalog');
    } catch (err) {
      alert(err.response?.data?.message || 'Error deleting estate');
    }
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
    }
  };

  const handleAnalyzeImage = async (useExisting = false) => {
    if (!isAuthenticated) {
      alert('Please login to analyze images');
      return;
    }

    // If using existing image, check if estate has one
    if (useExisting && !estate.image) {
      alert('This estate has no image to analyze. Please upload an image first.');
      return;
    }

    // If not using existing, check if new image selected
    if (!useExisting && !selectedImage) {
      alert('Please select an image first');
      return;
    }

    setAnalyzingImage(true);
    try {
      // If using existing image, send null, otherwise send the file
      const imageToAnalyze = useExisting ? null : selectedImage;
      const response = await estatesAPI.analyzeImage(id, imageToAnalyze);
      setImageAnalysis(response.data.analysis);
      // Reload estate to get updated data
      await loadEstate();
    } catch (err) {
      alert(err.response?.data?.message || 'Error analyzing image. Make sure Google Vision API key is configured.');
    } finally {
      setAnalyzingImage(false);
      setSelectedImage(null);
      // Reset file input
      const fileInput = document.getElementById('image-analyze-input');
      if (fileInput) fileInput.value = '';
    }
  };

  if (loading) {
    return (
      <div className="container text-center mt-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error || !estate) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger">
          {error || 'Estate not found'}
        </div>
        <Link to="/catalog" className="btn btn-primary">Back to Catalog</Link>
      </div>
    );
  }

  const canEdit = isAuthenticated && 
    (user?.role === 'admin' || estate.createdBy?._id === user?._id);

  return (
    <div className="estate-detail">
      <div className="container">
        <Link to="/catalog" className="btn btn-secondary mb-3">
          ← Back to Catalog
        </Link>

        <div className="row">
          <div className="col-md-8">
            <div className="estate-detail-image">
              {estate.image ? (
                <img src={`http://localhost:3001${estate.image}`} alt={estate.address} />
              ) : (
                <div className="no-image">No Image Available</div>
              )}
            </div>

            {isAuthenticated && (
              <div className="image-analysis-section">
                <h4>AI Image Analysis</h4>
                
                {estate.image ? (
                  <>
                    <p className="text-muted mb-3">Analyze the current estate image with Google Vision AI</p>
                    <button
                      onClick={() => handleAnalyzeImage(true)}
                      className="btn btn-info mb-3"
                      disabled={analyzingImage}
                    >
                      {analyzingImage ? 'Analyzing...' : 'Analyze Current Image'}
                    </button>
                    <p className="text-muted small mb-3">Or upload a different image to analyze:</p>
                  </>
                ) : (
                  <p className="text-muted mb-3">Upload an image to analyze it with Google Vision AI</p>
                )}

                <div className="analysis-upload mb-3">
                  <input
                    type="file"
                    id="image-analyze-input"
                    accept="image/*"
                    onChange={handleImageSelect}
                    className="form-control mb-2"
                    disabled={analyzingImage}
                  />
                  <button
                    onClick={() => handleAnalyzeImage(false)}
                    className="btn btn-secondary"
                    disabled={analyzingImage || !selectedImage}
                  >
                    {analyzingImage ? 'Analyzing...' : 'Analyze Uploaded Image'}
                  </button>
                </div>

                {imageAnalysis && (
                  <div className="analysis-results">
                    <h5>Analysis Results:</h5>
                    
                    {imageAnalysis.labelAnnotations && imageAnalysis.labelAnnotations.length > 0 && (
                      <div className="analysis-section">
                        <h6>Labels Detected:</h6>
                        <ul>
                          {imageAnalysis.labelAnnotations.map((label, idx) => (
                            <li key={idx}>
                              <strong>{label.description}</strong> 
                              {label.score && ` (${(label.score * 100).toFixed(1)}% confidence)`}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {imageAnalysis.localizedObjectAnnotations && imageAnalysis.localizedObjectAnnotations.length > 0 && (
                      <div className="analysis-section">
                        <h6>Objects Detected:</h6>
                        <ul>
                          {imageAnalysis.localizedObjectAnnotations.map((obj, idx) => (
                            <li key={idx}>
                              <strong>{obj.name}</strong>
                              {obj.score && ` (${(obj.score * 100).toFixed(1)}% confidence)`}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {imageAnalysis.textAnnotations && imageAnalysis.textAnnotations.length > 0 && (
                      <div className="analysis-section">
                        <h6>Text Detected:</h6>
                        <p className="text-detected">
                          {imageAnalysis.textAnnotations[0]?.description || 'No text found'}
                        </p>
                      </div>
                    )}

                    {(!imageAnalysis.labelAnnotations || imageAnalysis.labelAnnotations.length === 0) &&
                     (!imageAnalysis.localizedObjectAnnotations || imageAnalysis.localizedObjectAnnotations.length === 0) &&
                     (!imageAnalysis.textAnnotations || imageAnalysis.textAnnotations.length === 0) && (
                      <p className="text-muted">No analysis data available</p>
                    )}
                  </div>
                )}
              </div>
            )}

            <div className="estate-detail-content">
              <h1>{estate.address}</h1>
              
              <div className="estate-info-grid">
                <div className="info-item">
                  <strong>Cost:</strong> ${estate.cost.toLocaleString()}
                </div>
                <div className="info-item">
                  <strong>Area:</strong> {estate.area} m²
                </div>
                {estate.rooms && (
                  <div className="info-item">
                    <strong>Rooms:</strong> {estate.rooms}
                  </div>
                )}
                {estate.floor && (
                  <div className="info-item">
                    <strong>Floor:</strong> {estate.floor}
                    {estate.totalFloors && ` of ${estate.totalFloors}`}
                  </div>
                )}
                <div className="info-item">
                  <strong>Status:</strong> 
                  <span className={`badge bg-${estate.status === 'available' ? 'success' : estate.status === 'reserved' ? 'warning' : 'danger'}`}>
                    {estate.status}
                  </span>
                </div>
                {estate.category && (
                  <div className="info-item">
                    <strong>Category:</strong> {estate.category.name}
                  </div>
                )}
                <div className="info-item">
                  <strong>Cost per m²:</strong> 
                  ${estate.area > 0 ? (estate.cost / estate.area).toFixed(2) : 0}
                </div>
              </div>

              <div className="estate-description">
                <h3>Description</h3>
                <p>{estate.description}</p>
                {estate.aiDescription && (
                  <div className="ai-description">
                    <h5>AI Generated Description:</h5>
                    <p>{estate.aiDescription}</p>
                  </div>
                )}
              </div>

              <div className="estate-dates">
                <DateTimeDisplay label="Created" date={estate.createdAt} />
                {estate.updatedAt && estate.updatedAt !== estate.createdAt && (
                  <DateTimeDisplay label="Updated" date={estate.updatedAt} />
                )}
              </div>

              {canEdit && (
                <div className="estate-actions mt-3">
                  <Link to={`/estates/${id}/edit`} className="btn btn-primary">
                    Edit Estate
                  </Link>
                  <button onClick={handleDelete} className="btn btn-danger">
                    Delete Estate
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="col-md-4">
            <div className="reviews-section">
              <h3>Reviews ({reviews.length})</h3>
              
              {isAuthenticated && !showReviewForm && (
                <button 
                  onClick={() => setShowReviewForm(true)}
                  className="btn btn-primary mb-3"
                >
                  Write a Review
                </button>
              )}

              {showReviewForm && (
                <form onSubmit={handleReviewSubmit} className="review-form mb-4">
                  <div className="form-group">
                    <label>Rating</label>
                    <select
                      name="rating"
                      value={reviewForm.rating}
                      onChange={handleReviewChange}
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
                    <label>Review</label>
                    <textarea
                      name="text"
                      value={reviewForm.text}
                      onChange={handleReviewChange}
                      rows="4"
                      className="form-control"
                      required
                    />
                  </div>
                  <button type="submit" className="btn btn-primary">
                    Submit Review
                  </button>
                  <button 
                    type="button"
                    onClick={() => setShowReviewForm(false)}
                    className="btn btn-secondary"
                  >
                    Cancel
                  </button>
                </form>
              )}

              <div className="reviews-list">
                {reviews.length === 0 ? (
                  <p>No reviews yet. Be the first to review!</p>
                ) : (
                  reviews.map(review => (
                    <div key={review._id} className="review-item">
                      <div className="review-header">
                        <strong>{review.user?.firstName} {review.user?.lastName}</strong>
                        <div className="rating">
                          {'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}
                        </div>
                      </div>
                      <p>{review.text}</p>
                      <small>{formatDateWithTimezone(review.createdAt, 'MMM dd, yyyy')}</small>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EstateDetail;

