import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Navigate } from 'react-router-dom';
import DealFlow from '../components/DealFlow';
import DateTimeDisplay from '../components/DateTimeDisplay';
import '../styles/Dashboard.css';

// Страница дашборда для сотрудников
const Dashboard = () => {
  const { isAuthenticated, isEmployee, isAdmin } = useAuth();

  if (!isAuthenticated || (!isEmployee && !isAdmin)) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="dashboard-page">
      <div className="container">
        <h1>Employee Dashboard</h1>
        <DateTimeDisplay label="Dashboard Load Time" />
        <div className="dashboard-content">
          <DealFlow />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

