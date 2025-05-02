import http from '../services/http';

export async function fetchInvestmentPerformance() {
  return await http.get('/api/investment-performance/');
}
