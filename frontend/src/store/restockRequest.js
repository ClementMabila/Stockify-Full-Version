// store/restockRequest.js
import http from '../services/http';

export async function fetchRestockAlerts() {
  try {
    const response = await http.get('/api/stock-alerts/');
    return response;
  } catch (error) {
    console.error('Failed to fetch restock alerts:', error);
    throw error;
  }
}
