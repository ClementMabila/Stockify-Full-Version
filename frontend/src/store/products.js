// stores/products.js
import { defineStore } from 'pinia'; // Import defineStore from Pinia
import http from '../services/http';
import http_file_uplad from '../services/http_file_uplad';

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

export const useStockUploadStore = defineStore('stockUpload', {
  state: () => ({
    isUploading: false,
    uploadProgress: 0,
    uploadResults: null,
    analysisData: null,
    isAnalyzing: false,
    uploadError: null,
    fileColumns: [],
    mappedColumns: {},
    supportedFormats: ['csv', 'xlsx', 'xls', 'json', 'txt'],
  }),
  
  actions: {
    async uploadStockFile(file, columnMappings = null) {
      this.isUploading = true;
      this.uploadProgress = 0;
      this.uploadError = null;
      
      try {
        const formData = new FormData();
        formData.append('file', file);

        console.log(...formData);  // This will log the key-value pairs of the formData object.

        
        // If column mappings are provided, include them
        if (columnMappings) {
          formData.append('column_mappings', JSON.stringify(columnMappings));
        }
        
        const response = await http_file_uplad.post('/api/stock/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            this.uploadProgress = percentCompleted;
          }
        });
        
        this.uploadResults = response.data;
        return this.uploadResults;
      } catch (error) {
        this.uploadError = error.response?.data?.error || 'Failed to upload file';
        throw error;
      } finally {
        this.isUploading = false;
      }
    },
    
    async getStockAnalysis() {
      this.isAnalyzing = true;
      
      try {
        const response = await http_file_uplad.get('/api/stock/analysis/');
        this.analysisData = response.data;
        return this.analysisData;
      } catch (error) {
        console.error('Error fetching stock analysis:', error);
        throw error;
      } finally {
        this.isAnalyzing = false;
      }
    },
    
    async downloadTemplate(format = 'csv') {
      try {
        // Direct download approach using window.location
        window.location.href = `${http_file_uplad.defaults.baseURL}/api/stock/template/?format=${format}`;
        return true;
      } catch (error) {
        console.error('Error downloading template:', error);
        throw error;
      }
    },
    
    async exportStockData(format = 'csv') {
      try {
        // Direct download approach
        window.location.href = `${http_file_uplad.defaults.baseURL}/api/stock/export/?format=${format}`;
        return true;
      } catch (error) {
        console.error('Error exporting stock data:', error);
        throw error;
      }
    },
    
    resetUploadState() {
      this.isUploading = false;
      this.uploadProgress = 0;
      this.uploadResults = null;
      this.uploadError = null;
      this.fileColumns = [];
      this.mappedColumns = {};
    }
  }
});