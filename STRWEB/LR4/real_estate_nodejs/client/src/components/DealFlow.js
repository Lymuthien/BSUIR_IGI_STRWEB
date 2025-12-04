import React, { Component } from 'react';
import { salesAPI } from '../services/api';
import { formatDateWithTimezone } from '../utils/dateUtils';
import '../styles/DealFlow.css';

// Классовый компонент для управления потоком сделок
class DealFlow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sales: [],
      loading: false,
      error: null,
      filterStatus: '',
      sortBy: 'dateOfSale',
      sortOrder: 'desc'
    };
  }

  componentDidMount() {
    this.loadSales();
  }

  loadSales = async () => {
    this.setState({ loading: true, error: null });
    try {
      const params = {};
      if (this.state.filterStatus) {
        params.status = this.state.filterStatus;
      }

      const response = await salesAPI.getAll(params);
      let sales = response.data || [];

      // Client-side sorting
      sales.sort((a, b) => {
        let aValue = a[this.state.sortBy];
        let bValue = b[this.state.sortBy];

        if (aValue instanceof Date || typeof aValue === 'string') {
          aValue = new Date(aValue);
          bValue = new Date(bValue);
        }

        if (this.state.sortOrder === 'asc') {
          return aValue > bValue ? 1 : -1;
        } else {
          return aValue < bValue ? 1 : -1;
        }
      });

      this.setState({ sales, loading: false });
    } catch (error) {
      this.setState({ error: error.message, loading: false });
    }
  };

  handleStatusFilterChange = (e) => {
    this.setState({ filterStatus: e.target.value }, () => {
      this.loadSales();
    });
  };

  handleSortChange = (e) => {
    const { name, value } = e.target;
    if (name === 'sortBy') {
      this.setState({ sortBy: value }, () => {
        this.loadSales();
      });
    } else {
      this.setState({ sortOrder: value }, () => {
        this.loadSales();
      });
    }
  };

  handleStatusUpdate = async (saleId, newStatus) => {
    try {
      await salesAPI.updateStatus(saleId, newStatus);
      this.loadSales();
    } catch (error) {
      alert('Error updating sale status: ' + error.message);
    }
  };

  render() {
    const { sales, loading, error, filterStatus, sortBy, sortOrder } = this.state;

    return (
      <div className="deal-flow">
        <h3>Deal Flow Management</h3>

        <div className="deal-flow-controls">
          <select
            value={filterStatus}
            onChange={this.handleStatusFilterChange}
            className="form-select"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>

          <select
            name="sortBy"
            value={sortBy}
            onChange={this.handleSortChange}
            className="form-select"
          >
            <option value="dateOfSale">Date of Sale</option>
            <option value="dateOfContract">Date of Contract</option>
            <option value="totalCost">Total Cost</option>
          </select>

          <select
            name="sortOrder"
            value={sortOrder}
            onChange={this.handleSortChange}
            className="form-select"
          >
            <option value="desc">Descending</option>
            <option value="asc">Ascending</option>
          </select>

          <button onClick={this.loadSales} className="btn btn-primary">
            Refresh
          </button>
        </div>

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
          <div className="deal-flow-list">
            {sales.length === 0 ? (
              <p>No sales found.</p>
            ) : (
              sales.map(sale => (
                <div key={sale._id} className="deal-item">
                  <div className="deal-header">
                    <h5>{sale.estate?.address || 'Unknown Address'}</h5>
                    <span className={`status-badge status-${sale.status}`}>
                      {sale.status}
                    </span>
                  </div>
                  
                  <div className="deal-info">
                    <div className="info-row">
                      <span>Client:</span>
                      <strong>{sale.client?.firstName} {sale.client?.lastName}</strong>
                    </div>
                    <div className="info-row">
                      <span>Employee:</span>
                      <strong>{sale.employee?.firstName} {sale.employee?.lastName}</strong>
                    </div>
                    <div className="info-row">
                      <span>Estate Cost:</span>
                      <strong>${sale.estateCost?.toLocaleString()}</strong>
                    </div>
                    <div className="info-row">
                      <span>Service Cost:</span>
                      <strong>${sale.serviceCost?.toLocaleString()}</strong>
                    </div>
                    <div className="info-row">
                      <span>Total Cost:</span>
                      <strong className="total-cost">${sale.totalCost?.toLocaleString()}</strong>
                    </div>
                    <div className="info-row">
                      <span>Date of Contract:</span>
                      <strong>{formatDateWithTimezone(sale.dateOfContract, 'MMM dd, yyyy')}</strong>
                    </div>
                    <div className="info-row">
                      <span>Date of Sale:</span>
                      <strong>{formatDateWithTimezone(sale.dateOfSale, 'MMM dd, yyyy')}</strong>
                    </div>
                  </div>

                  {sale.status === 'pending' && (
                    <div className="deal-actions">
                      <button
                        onClick={() => this.handleStatusUpdate(sale._id, 'completed')}
                        className="btn btn-success btn-sm"
                      >
                        Complete
                      </button>
                      <button
                        onClick={() => this.handleStatusUpdate(sale._id, 'cancelled')}
                        className="btn btn-danger btn-sm"
                      >
                        Cancel
                      </button>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}
      </div>
    );
  }
}

export default DealFlow;

