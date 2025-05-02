// services/http.js
import { getCSRFToken } from '../store/auth'

export default {
  async post(url, data) {
    const response = await fetch(`http://localhost:8000${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      credentials: 'include',
      body: JSON.stringify(data)
    })
    
    if (!response.ok) throw new Error(await response.text())
    return response.json()
  },
  async get(url) {
    const response = await fetch(`http://localhost:8000${url}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(), // Include CSRF token if your backend needs it
      },
      credentials: 'include'
    });

    if (!response.ok) throw new Error(await response.text());
    return response.json();
  },
  async patch(url, data) {
    const response = await fetch(`http://localhost:8000${url}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      credentials: 'include',
      body: JSON.stringify(data)
    });

    if (!response.ok) throw new Error(await response.text());
    return response.json();
  }
}