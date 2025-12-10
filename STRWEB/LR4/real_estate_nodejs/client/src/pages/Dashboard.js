import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Navigate, useNavigate } from 'react-router-dom';
import DealFlow from '../components/DealFlow';
import SaleForm from '../components/SaleForm';
import DateTimeDisplay from '../components/DateTimeDisplay';
import { salesAPI } from '../services/api';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const { isAuthenticated, isEmployee, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [showSaleForm, setShowSaleForm] = useState(false);

  if (!isAuthenticated || (!isEmployee && !isAdmin)) {
    return <Navigate to="/login" replace />;
  }

  const handleCreateSale = async (formData) => {
    try {
      await salesAPI.create(formData);
      alert('Sale created successfully!');
      setShowSaleForm(false);
      window.location.reload(); // Reload to refresh DealFlow
    } catch (error) {
      throw error;
    }
  };

  return (
    <div className="dashboard-page">
      <div className="container">
        <h1>Employee Dashboard</h1>
        <DateTimeDisplay label="Dashboard Load Time" />
        
        <div className="dashboard-actions mb-4">
          <button 
            onClick={() => setShowSaleForm(!showSaleForm)}
            className="btn btn-primary"
          >
            {showSaleForm ? 'Cancel' : 'Create New Sale'}
          </button>
        </div>

        {showSaleForm && (
          <div className="sale-form-container mb-4">
            <h3>Create New Sale</h3>
            <SaleForm 
              onSubmit={handleCreateSale}
              onCancel={() => setShowSaleForm(false)}
            />
          </div>
        )}

        <div className="dashboard-content">
          <DealFlow />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

