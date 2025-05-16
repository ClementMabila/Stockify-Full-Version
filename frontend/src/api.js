import axios from 'axios';

// Create a base axios instance with common configuration
const api = axios.create({
  // Use window.location.origin as default base URL if no environment variable is defined
  baseURL: (window._env && window._env.API_BASE_URL) || '',
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  },
  withCredentials: true  // Important for cookies/session authentication
});

// Add a request interceptor to include CSRF token if needed
api.interceptors.request.use(config => {
  // Get CSRF token from cookie or meta tag
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
  
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  
  return config;
});

// Add a response interceptor to handle common errors
api.interceptors.response.use(
  response => response,
  error => {
    // Handle authentication errors
    if (error.response && error.response.status === 401) {
      // Redirect to login page or show login modal
      console.error('Authentication error');
      // window.location.href = '/login';
    }
    
    // Handle permission errors
    if (error.response && error.response.status === 403) {
      console.error('Permission denied');
    }
    
    return Promise.reject(error);
  }
);

export default api;