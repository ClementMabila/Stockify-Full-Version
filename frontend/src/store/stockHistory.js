// store/stockHistory.js
import http from '../services/http';

export async function fetchStockHistory() {
  try {
    const response = await http.get('/api/stock-history/');
    return response;
  } catch (error) {
    console.error('Failed to fetch stock history:', error);
    throw error;
  }
}
