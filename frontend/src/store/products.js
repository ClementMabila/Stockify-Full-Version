// stores/products.js
import { defineStore } from 'pinia'; // Import defineStore from Pinia
import http from '../services/http';

export const useProductsStore = defineStore('products', {
  actions: {
    async addProduct(productData) {
      try {
        return await http.post('/api/inventory/', productData);
      } catch (error) {
        console.error('Product addition failed:', error);
        throw error;
      }
    },

    async fetchProducts() {
      try {
        const response = await fetch('http://localhost:8000/api/inventory/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
        });

        if (!response.ok) throw new Error(await response.text());
        const data = await response.json();
        this.products = data;
        return data;
      } catch (error) {
        console.error('Error fetching products:', error);
        throw error;
      }
    },
    async updateProduct(productId, updateData) {
      try {
        return await http.patch(`/api/inventory/${productId}/`, updateData);
      } catch (error) {
        console.error('Error updating product:', error);
        throw error;
      }
    }
  },
});