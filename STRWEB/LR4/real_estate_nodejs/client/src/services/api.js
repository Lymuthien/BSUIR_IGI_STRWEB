import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Don't redirect if already on login/register page or if it's an auth endpoint
      const currentPath = window.location.pathname;
      const isAuthEndpoint = error.config?.url?.includes('/auth/');
      
      if (!isAuthEndpoint && currentPath !== '/login' && currentPath !== '/register') {
        // Only redirect if not already on auth pages
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me'),
  googleAuth: () => window.location.href = `${API_BASE_URL}/auth/google`
};

// Estates API
export const estatesAPI = {
  getAll: (params) => api.get('/estates', { params }),
  getById: (id) => api.get(`/estates/${id}`),
  create: (data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      if (key === 'image' && data[key]) {
        formData.append('image', data[key]);
      } else if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    return api.post('/estates', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  update: (id, data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      if (key === 'image' && data[key]) {
        formData.append('image', data[key]);
      } else if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    return api.put(`/estates/${id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  delete: (id) => api.delete(`/estates/${id}`),
  analyzeImage: (id, imageFile) => {
    const formData = new FormData();
    // If imageFile is null, we're analyzing existing image, so don't append anything
    if (imageFile) {
      formData.append('image', imageFile);
    }
    return api.post(`/estates/${id}/analyze-image`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  }
};

// Reviews API
export const reviewsAPI = {
  getAll: (params) => api.get('/reviews', { params }),
  getById: (id) => api.get(`/reviews/${id}`),
  create: (data) => api.post('/reviews', data),
  update: (id, data) => api.put(`/reviews/${id}`, data),
  delete: (id) => api.delete(`/reviews/${id}`)
};

// Services API
export const servicesAPI = {
  getAll: () => api.get('/services'),
  getById: (id) => api.get(`/services/${id}`),
  getCategories: () => api.get('/services/categories')
};

// Sales API
export const salesAPI = {
  getAll: (params) => api.get('/sales', { params }),
  getMySales: () => api.get('/sales/my-sales'),
  getById: (id) => api.get(`/sales/${id}`),
  create: (data) => api.post('/sales', data),
  updateStatus: (id, status) => api.patch(`/sales/${id}`, { status })
};

export default api;

