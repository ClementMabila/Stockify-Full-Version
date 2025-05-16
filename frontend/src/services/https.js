// services/http.js
import { getCSRFToken } from '../store/auth'

export default {
  async post(url, data) {
    try {
      const response = await fetch(`http://localhost:8000${url}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include',
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`HTTP Error ${response.status} for POST ${url}:`, errorText);
        try {
          // Try to parse as JSON to get detailed error message
          const errorJson = JSON.parse(errorText);
          throw new Error(errorJson.error || errorJson.detail || errorText);
        } catch (e) {
          // If parsing fails, use the raw text
          throw new Error(errorText || `HTTP error ${response.status}`);
        }
      }
      
      return response.json();
    } catch (error) {
      console.error('Network or parsing error:', error);
      throw error;
    }
  },
  
  async get(url) {
    try {
      const response = await fetch(`http://localhost:8000${url}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include'
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`HTTP Error ${response.status} for GET ${url}:`, errorText);
        try {
          // Try to parse as JSON to get detailed error message
          const errorJson = JSON.parse(errorText);
          throw new Error(errorJson.error || errorJson.detail || errorText);
        } catch (e) {
          // If parsing fails, use the raw text
          throw new Error(errorText || `HTTP error ${response.status}`);
        }
      }
      
      return response.json();
    } catch (error) {
      console.error('Network or parsing error:', error);
      throw error; 
    }
  },
  
  async patch(url, data) {
    try {
      const response = await fetch(`http://localhost:8000${url}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include',
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`HTTP Error ${response.status} for PATCH ${url}:`, errorText);
        try {
          // Try to parse as JSON to get detailed error message
          const errorJson = JSON.parse(errorText);
          throw new Error(errorJson.error || errorJson.detail || errorText);
        } catch (e) {
          // If parsing fails, use the raw text
          throw new Error(errorText || `HTTP error ${response.status}`);
        }
      }
      
      return response.json();
    } catch (error) {
      console.error('Network or parsing error:', error);
      throw error;
    }
  }
}