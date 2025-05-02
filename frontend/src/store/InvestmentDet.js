import http from '../services/http';

export default {
  getMyInvestment() {
    return http.get('/api/investments/me/');
  },

  getAllMyInvestments() {
    return http.get('/api/fetch-stock-investments/');
  },
  
  investInStock(stockId, amount) {
    return http.post('/api/investments/invest-stock/', {
      stock_id: stockId,
      amount,  // Include this if you're supporting amount in your API
    });
  },

  getInvestableStocks() {
    return http.get('/api/investable-stocks/');
  },
};
