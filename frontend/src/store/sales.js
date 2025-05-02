import { defineStore } from 'pinia';
import http from '../services/http';

export const useSalesStore = defineStore('sales', {
  actions: {
    async fetchSales() {
      try {
        const response = await fetch('http://localhost:8000/api/sales-entries/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
        });

        if (!response.ok) {
          throw new Error(await response.text());
        }

        return await response.json();
      } catch (error) {
        console.error('Error fetching sales:', error);
        throw error;
      }
    },

    async addSale(saleData) {
      try {
        return await http.post('/api/sales-entries/', saleData);
      } catch (error) {
        console.error('Sale addition failed:', error);
        throw error;
      }
    }
  }
});
