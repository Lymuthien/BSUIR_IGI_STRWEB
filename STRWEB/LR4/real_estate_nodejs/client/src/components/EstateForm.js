import React, { useState, useEffect } from 'react';
import { servicesAPI } from '../services/api';
import '../styles/EstateForm.css';

const EstateForm = ({ estate, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    address: '',
    cost: '',
    area: '',
    description: '',
    category: '',
    rooms: '',
    floor: '',
    totalFloors: '',
    status: 'available',
    image: null
  });
  const [services, setServices] = useState([]);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);

  useEffect(() => {
    loadServices();
    if (estate) {
      setFormData({
        address: estate.address || '',
        cost: estate.cost || '',
        area: estate.area || '',
        description: estate.description || '',
        category: estate.category?._id || estate.category || '',
        rooms: estate.rooms || '',
        floor: estate.floor || '',
        totalFloors: estate.totalFloors || '',
        status: estate.status || 'available',
        image: null
      });
      if (estate.image) {
        setImagePreview(`http://localhost:3001${estate.image}`);
      }
    }
  }, [estate]);

  const loadServices = async () => {
    try {
      const response = await servicesAPI.getAll();
      setServices(response.data || []);
    } catch (error) {
      console.error('Error loading services:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleFocus = (e) => {
    const { name } = e.target;
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleBlur = (e) => {
    const { name, value } = e.target;
    const newErrors = { ...errors };
    if (name === 'address' && !value.trim()) {
      newErrors.address = 'Address is required';
    } else if (name === 'cost' && (!value || parseFloat(value) <= 0)) {
      newErrors.cost = 'Valid cost is required';
    } else if (name === 'area' && (!value || parseFloat(value) <= 0)) {
      newErrors.area = 'Valid area is required';
    } else if (name === 'description' && !value.trim()) {
      newErrors.description = 'Description is required';
    } else if (name === 'category' && !value) {
      newErrors.category = 'Category is required';
    } else {
      delete newErrors[name];
    }
    setErrors(newErrors);
  };

  const handleKeyPress = (e) => {
    if (e.target.tagName === 'TEXTAREA' && e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData(prev => ({
        ...prev,
        image: file
      }));
      
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const validate = () => {
    const newErrors = {};
    
    if (!formData.address.trim()) {
      newErrors.address = 'Address is required';
    }
    if (!formData.cost || parseFloat(formData.cost) <= 0) {
      newErrors.cost = 'Valid cost is required';
    }
    if (!formData.area || parseFloat(formData.area) <= 0) {
      newErrors.area = 'Valid area is required';
    }
    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }
    if (!formData.category) {
      newErrors.category = 'Category is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    setLoading(true);
    try {
      const submitData = {
        ...formData,
        cost: parseFloat(formData.cost),
        area: parseFloat(formData.area),
        rooms: formData.rooms ? parseInt(formData.rooms) : undefined,
        floor: formData.floor ? parseInt(formData.floor) : undefined,
        totalFloors: formData.totalFloors ? parseInt(formData.totalFloors) : undefined
      };

      if (onSubmit) {
        await onSubmit(submitData);
      }
    } catch (error) {
      setErrors({ submit: error.message });
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="estate-form">
      <div className="form-row">
        <div className="form-group">
          <label>Address *</label>
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleChange}
            onFocus={handleFocus}
            onBlur={handleBlur}
            onKeyPress={handleKeyPress}
            className={`form-control ${errors.address ? 'is-invalid' : ''}`}
          />
          {errors.address && <div className="invalid-feedback">{errors.address}</div>}
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Cost ($) *</label>
          <input
            type="number"
            name="cost"
            value={formData.cost}
            onChange={handleChange}
            step="0.01"
            min="0.01"
            className={`form-control ${errors.cost ? 'is-invalid' : ''}`}
            onFocus={handleFocus}
            onBlur={handleBlur}
            onKeyPress={handleKeyPress}
          />
          {errors.cost && <div className="invalid-feedback">{errors.cost}</div>}
        </div>

        <div className="form-group">
          <label>Area (m²) *</label>
          <input
            type="number"
            name="area"
            value={formData.area}
            onChange={handleChange}
            step="0.01"
            min="0.01"
            className={`form-control ${errors.area ? 'is-invalid' : ''}`}
            onFocus={handleFocus}
            onBlur={handleBlur}
            onKeyPress={handleKeyPress}
          />
          {errors.area && <div className="invalid-feedback">{errors.area}</div>}
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Category *</label>
          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
            onFocus={handleFocus}
            onBlur={handleBlur}
            className={`form-control ${errors.category ? 'is-invalid' : ''}`}
          >
            <option value="">Select category</option>
            {services.map(service => (
              <option key={service._id} value={service._id}>
                {service.category?.name} - {service.name}
              </option>
            ))}
          </select>
          {errors.category && <div className="invalid-feedback">{errors.category}</div>}
        </div>

        <div className="form-group">
          <label>Status</label>
          <select
            name="status"
            value={formData.status}
            onChange={handleChange}
            className="form-control"
          >
            <option value="available">Available</option>
            <option value="reserved">Reserved</option>
            <option value="sold">Sold</option>
          </select>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Rooms</label>
          <input
            type="number"
            name="rooms"
            value={formData.rooms}
            onChange={handleChange}
            min="0"
            className="form-control"
          />
        </div>

        <div className="form-group">
          <label>Floor</label>
          <input
            type="number"
            name="floor"
            value={formData.floor}
            onChange={handleChange}
            className="form-control"
          />
        </div>

        <div className="form-group">
          <label>Total Floors</label>
          <input
            type="number"
            name="totalFloors"
            value={formData.totalFloors}
            onChange={handleChange}
            className="form-control"
          />
        </div>
      </div>

      <div className="form-group">
        <label>Description *</label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onKeyPress={handleKeyPress}
          rows="5"
          className={`form-control ${errors.description ? 'is-invalid' : ''}`}
        />
        {errors.description && <div className="invalid-feedback">{errors.description}</div>}
      </div>

      <div className="form-group">
        <label>Image</label>
        <input
          type="file"
          name="image"
          onChange={handleFileChange}
          accept="image/*"
          className="form-control"
        />
        {imagePreview && (
          <div className="image-preview">
            <img src={imagePreview} alt="Preview" />
          </div>
        )}
      </div>

      {errors.submit && (
        <div className="alert alert-danger">{errors.submit}</div>
      )}

      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Saving...' : estate ? 'Update' : 'Create'}
        </button>
        <button type="button" onClick={handleCancel} className="btn btn-secondary">
          Cancel
        </button>
      </div>
    </form>
  );
};

export default EstateForm;

