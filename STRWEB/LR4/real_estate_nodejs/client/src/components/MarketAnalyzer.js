import React, { Component } from 'react';
import { estatesAPI } from '../services/api';
import '../styles/MarketAnalyzer.css';

class MarketAnalyzer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      estates: [],
      analysis: null,
      loading: false,
      error: null
    };
  }

  componentDidMount() {
    this.loadEstates();
  }

  loadEstates = async () => {
    this.setState({ loading: true, error: null });
    try {
      const response = await estatesAPI.getAll({
        limit: 100
      });
      
      const estates = response.data.estates || [];
      this.setState({ estates });
      this.analyzeMarket(estates);
    } catch (error) {
      this.setState({ error: error.message });
    } finally {
      this.setState({ loading: false });
    }
  };

  analyzeMarket = (estates) => {
    if (estates.length === 0) {
      this.setState({ analysis: null });
      return;
    }

    const totalEstates = estates.length;
    const avgCost = estates.reduce((sum, e) => sum + e.cost, 0) / totalEstates;
    const avgArea = estates.reduce((sum, e) => sum + e.area, 0) / totalEstates;
    const avgCostPerSqm = avgCost / avgArea;
    
    const byStatus = estates.reduce((acc, e) => {
      acc[e.status] = (acc[e.status] || 0) + 1;
      return acc;
    }, {});

    const costRange = {
      min: Math.min(...estates.map(e => e.cost)),
      max: Math.max(...estates.map(e => e.cost))
    };

    const areaRange = {
      min: Math.min(...estates.map(e => e.area)),
      max: Math.max(...estates.map(e => e.area))
    };

    this.setState({
      analysis: {
        totalEstates,
        avgCost: avgCost.toFixed(2),
        avgArea: avgArea.toFixed(2),
        avgCostPerSqm: avgCostPerSqm.toFixed(2),
        byStatus,
        costRange,
        areaRange
      }
    });
  };

  handleAnalyze = () => {
    this.loadEstates();
  };

  render() {
    const { analysis, loading, error } = this.state;

    return (
      <div className="market-analyzer">
        <h3>Market Analysis</h3>
        
        <div className="analyzer-controls">
          <button 
            onClick={this.handleAnalyze}
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Refresh Analysis'}
          </button>
        </div>

        {error && (
          <div className="alert alert-danger">{error}</div>
        )}

        {analysis && (
          <div className="analysis-results">
            <div className="stat-card">
              <h5>Total Estates</h5>
              <p>{analysis.totalEstates}</p>
            </div>
            <div className="stat-card">
              <h5>Average Cost</h5>
              <p>${parseFloat(analysis.avgCost).toLocaleString()}</p>
            </div>
            <div className="stat-card">
              <h5>Average Area</h5>
              <p>{analysis.avgArea} m²</p>
            </div>
            <div className="stat-card">
              <h5>Avg Cost per m²</h5>
              <p>${analysis.avgCostPerSqm}</p>
            </div>
            <div className="stat-card">
              <h5>Cost Range</h5>
              <p>${analysis.costRange.min.toLocaleString()} - ${analysis.costRange.max.toLocaleString()}</p>
            </div>
            <div className="stat-card">
              <h5>Area Range</h5>
              <p>{analysis.areaRange.min} - {analysis.areaRange.max} m²</p>
            </div>
            <div className="stat-card full-width">
              <h5>By Status</h5>
              <div className="status-breakdown">
                {Object.entries(analysis.byStatus).map(([status, count]) => (
                  <span key={status} className="status-item">
                    {status}: {count}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }
}

export default MarketAnalyzer;

