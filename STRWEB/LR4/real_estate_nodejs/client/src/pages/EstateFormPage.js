import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { estatesAPI } from '../services/api';
import EstateForm from '../components/EstateForm';
import { useAuth } from '../context/AuthContext';

// Функциональный компонент для страницы создания/редактирования
const EstateFormPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated, isEmployee, isAdmin } = useAuth();
  const [estate, setEstate] = useState(null);
  const [loading, setLoading] = useState(!!id);

  const loadEstate = useCallback(async () => {
    try {
      const response = await estatesAPI.getById(id);
      setEstate(response.data);
    } catch (error) {
      alert('Error loading estate: ' + error.message);
      navigate('/catalog');
    } finally {
      setLoading(false);
    }
  }, [id, navigate]);

  useEffect(() => {
    if (!isAuthenticated || (!isEmployee && !isAdmin)) {
      navigate('/login');
      return;
    }

    if (id) {
      loadEstate();
    }
  }, [id, isAuthenticated, isEmployee, isAdmin, navigate, loadEstate]);

  const handleSubmit = async (formData) => {
    try {
      if (id) {
        await estatesAPI.update(id, formData);
      } else {
        await estatesAPI.create(formData);
      }
      navigate('/catalog');
    } catch (error) {
      throw error;
    }
  };

  const handleCancel = () => {
    navigate('/catalog');
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

  return (
    <div className="container mt-4">
      <h1>{id ? 'Edit Estate' : 'Add New Estate'}</h1>
      <EstateForm 
        estate={estate}
        onSubmit={handleSubmit}
        onCancel={handleCancel}
      />
    </div>
  );
};

export default EstateFormPage;

