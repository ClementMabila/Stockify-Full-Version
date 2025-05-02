import http from '../services/http';

export default {
  async getCandlestickData() {
    return await http.get('/api/stock-candlestick-data/')
  }
}
