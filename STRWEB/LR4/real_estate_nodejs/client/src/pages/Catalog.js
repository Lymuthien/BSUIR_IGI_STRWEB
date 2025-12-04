import React, { useEffect, useReducer, useCallback } from 'react';
import { estatesAPI } from '../services/api';
import EstateCard from '../components/EstateCard';
import DateTimeDisplay from '../components/DateTimeDisplay';
import '../styles/Catalog.css';

// useReducer для управления состоянием каталога
const catalogReducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ESTATES':
      return { ...state, estates: action.payload, loading: false };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    case 'SET_FILTERS':
      return { ...state, filters: { ...state.filters, ...action.payload } };
    case 'SET_SORT':
      return { ...state, sortBy: action.sortBy, sortOrder: action.sortOrder };
    case 'SET_PAGE':
      return { ...state, page: action.payload };
    default:
      return state;
  }
};

// Функциональный компонент с useReducer хук
const Catalog = () => {
  const [state, dispatch] = useReducer(catalogReducer, {
    estates: [],
    loading: false,
    error: null,
    filters: {
      search: '',
      minCost: '',
      maxCost: '',
      minArea: '',
      maxArea: '',
      status: ''
    },
    sortBy: 'createdAt',
    sortOrder: 'desc',
    page: 1,
    totalPages: 1
  });

  const loadEstates = useCallback(async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const params = {
        page: state.page,
        limit: 12,
        sortBy: state.sortBy,
        sortOrder: state.sortOrder
      };

      if (state.filters.search) params.search = state.filters.search;
      if (state.filters.minCost) params.minCost = state.filters.minCost;
      if (state.filters.maxCost) params.maxCost = state.filters.maxCost;
      if (state.filters.minArea) params.minArea = state.filters.minArea;
      if (state.filters.maxArea) params.maxArea = state.filters.maxArea;
      if (state.filters.status) params.status = state.filters.status;

      const response = await estatesAPI.getAll(params);
      dispatch({ 
        type: 'SET_ESTATES', 
        payload: response.data.estates || [] 
      });
      if (response.data.pagination) {
        dispatch({ 
          type: 'SET_PAGE', 
          payload: response.data.pagination.totalPages 
        });
      }
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
    }
  }, [state.filters, state.sortBy, state.sortOrder, state.page]);

  useEffect(() => {
    loadEstates();
  }, [loadEstates]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    dispatch({ 
      type: 'SET_FILTERS', 
      payload: { [name]: value } 
    });
    dispatch({ type: 'SET_PAGE', payload: 1 });
  };

  const handleSortChange = (e) => {
    const { name, value } = e.target;
    if (name === 'sortBy') {
      dispatch({ type: 'SET_SORT', sortBy: value, sortOrder: state.sortOrder });
    } else {
      dispatch({ type: 'SET_SORT', sortBy: state.sortBy, sortOrder: value });
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadEstates();
  };

  const handleClearFilters = () => {
    dispatch({
      type: 'SET_FILTERS',
      payload: {
        search: '',
        minCost: '',
        maxCost: '',
        minArea: '',
        maxArea: '',
        status: ''
      }
    });
    dispatch({ type: 'SET_PAGE', payload: 1 });
  };

  return (
    <div className="catalog-page">
      <div className="container">
        <h1>Property Catalog</h1>
        <DateTimeDisplay label="Catalog Load Time" />

        <div className="catalog-filters">
          <form onSubmit={handleSearch} className="filter-form">
            <div className="filter-row">
              <input
                type="text"
                name="search"
                value={state.filters.search}
                onChange={handleFilterChange}
                placeholder="Search by address or description..."
                className="form-control"
              />
              <button type="submit" className="btn btn-primary">
                Search
              </button>
            </div>

            <div className="filter-row">
              <input
                type="number"
                name="minCost"
                value={state.filters.minCost}
                onChange={handleFilterChange}
                placeholder="Min Cost"
                className="form-control"
              />
              <input
                type="number"
                name="maxCost"
                value={state.filters.maxCost}
                onChange={handleFilterChange}
                placeholder="Max Cost"
                className="form-control"
              />
              <input
                type="number"
                name="minArea"
                value={state.filters.minArea}
                onChange={handleFilterChange}
                placeholder="Min Area"
                className="form-control"
              />
              <input
                type="number"
                name="maxArea"
                value={state.filters.maxArea}
                onChange={handleFilterChange}
                placeholder="Max Area"
                className="form-control"
              />
              <select
                name="status"
                value={state.filters.status}
                onChange={handleFilterChange}
                className="form-control"
              >
                <option value="">All Status</option>
                <option value="available">Available</option>
                <option value="reserved">Reserved</option>
                <option value="sold">Sold</option>
              </select>
            </div>

            <div className="filter-row">
              <select
                name="sortBy"
                value={state.sortBy}
                onChange={handleSortChange}
                className="form-control"
              >
                <option value="cost">Cost</option>
                <option value="area">Area</option>
                <option value="createdAt">Date</option>
              </select>
              <select
                name="sortOrder"
                value={state.sortOrder}
                onChange={handleSortChange}
                className="form-control"
              >
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
              <button type="button" onClick={handleClearFilters} className="btn btn-secondary">
                Clear Filters
              </button>
            </div>
          </form>
        </div>

        {state.loading && (
          <div className="text-center">
            <div className="spinner-border" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        )}

        {state.error && (
          <div className="alert alert-danger">{state.error}</div>
        )}

        {!state.loading && !state.error && (
          <>
            <div className="estates-grid">
              {state.estates.map(estate => (
                <EstateCard key={estate._id} estate={estate} />
              ))}
            </div>

            {state.estates.length === 0 && (
              <div className="text-center mt-5">
                <p>No properties found. Try adjusting your filters.</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Catalog;

