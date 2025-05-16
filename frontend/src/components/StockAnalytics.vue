<template>
  <div class="stock-analytics-panel">
    <h4 class="analytics-title">Stock Analytics</h4>

    <div v-if="stockUploadStore.isAnalyzing" class="loading-analytics">
      <div class="spinner"></div>
      <p>Loading analytics data...</p>
    </div>

    <div v-else-if="!analytics" class="no-analytics">
      <p>No analytics data available</p>
      <button @click="loadAnalytics" class="analytics-button">Load Analytics</button>
    </div>

    <div v-else class="analytics-content">
      <div class="analytics-summary">
        <div class="analytics-card total-items">
          <div class="card-value">{{ analytics.total_items }}</div>
          <div class="card-label">Total Products</div>
        </div>

        <div class="analytics-card total-value">
          <div class="card-value">${{ formatCurrency(analytics.total_value) }}</div>
          <div class="card-label">Inventory Value</div>
        </div>

        <div class="analytics-card low-stock">
          <div class="card-value">{{ analytics.low_stock_items }}</div>
          <div class="card-label">Low Stock Items</div>
        </div>
      </div>

      <div class="analytics-details">
        <div class="analytics-section">
          <h5>Categories</h5>
          <div class="pie-chart">
            <StockPieChart
              v-if="analytics.categories"
              :chart-data="formatCategoriesForChart(analytics.categories)"
              chart-id="categories-chart"
            />
          </div>
          <div class="analytics-table">
            <table>
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Count</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(count, category) in analytics.categories" :key="category">
                  <td>{{ category }}</td>
                  <td>{{ count }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="analytics-section">
          <h5>Suppliers</h5>
          <div class="pie-chart">
            <StockPieChart
              v-if="analytics.suppliers"
              :chart-data="formatSuppliersForChart(analytics.suppliers)"
              chart-id="suppliers-chart"
            />
          </div>
          <div class="analytics-table">
            <table>
              <thead>
                <tr>
                  <th>Supplier</th>
                  <th>Count</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(count, supplier) in analytics.suppliers" :key="supplier">
                  <td>{{ supplier }}</td>
                  <td>{{ count }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="high-value-items">
        <h5>Top Value Items</h5>
        <div class="analytics-table">
          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>Unit Price</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in analytics.top_value_items" :key="index">
                <td>{{ item.name }}</td>
                <td>${{ formatCurrency(item.unit_price) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="analytics-actions">
        <button @click="refreshAnalytics" class="refresh-button">
          Refresh Analytics
        </button>
        <button @click="exportData" class="export-button">
          Export Stock Data
        </button>
      </div>

      <!-- Export Format Selector (shows when export button clicked) -->
      <div v-if="showExportOptions" class="export-options">
        <h5>Select Export Format</h5>
        <div class="format-buttons">
          <button @click="exportInFormat('csv')" class="format-button">CSV</button>
          <button @click="exportInFormat('xlsx')" class="format-button">Excel</button>
          <button @click="exportInFormat('json')" class="format-button">JSON</button>
          <button @click="hideExportOptions" class="cancel-button">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useStockUploadStore } from '../store/products';
import StockPieChart from './StockPieChart.vue';

export default {
  name: 'StockAnalytics',
  components: {
    StockPieChart
  },
  
  setup() {
    const stockUploadStore = useStockUploadStore();
    const analytics = ref(null);
    const showExportOptions = ref(false);

    // Load analytics data from the store
    const loadAnalytics = async () => {
      try {
        const data = await stockUploadStore.getStockAnalysis();
        analytics.value = data;
      } catch (error) {
        console.error('Failed to load analytics:', error);
      }
    };

    // Refresh analytics data
    const refreshAnalytics = () => {
      analytics.value = null;
      loadAnalytics();
    };

    // Show export options
    const exportData = () => {
      showExportOptions.value = true;
    };

    // Hide export options
    const hideExportOptions = () => {
      showExportOptions.value = false;
    };

    // Export data in selected format
    const exportInFormat = (format) => {
      stockUploadStore.exportStockData(format);
      showExportOptions.value = false;
    };

    // Format currency
    const formatCurrency = (value) => {
      return value.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };

    // Format categories for chart component
    const formatCategoriesForChart = (categories) => {
      return {
        labels: Object.keys(categories),
        datasets: [{
          data: Object.values(categories),
          backgroundColor: generateColors(Object.keys(categories).length)
        }]
      };
    };

    // Format suppliers for chart component
    const formatSuppliersForChart = (suppliers) => {
      return {
        labels: Object.keys(suppliers),
        datasets: [{
          data: Object.values(suppliers),
          backgroundColor: generateColors(Object.keys(suppliers).length)
        }]
      };
    };

    // Generate colors for chart
    const generateColors = (count) => {
      const colors = [
        '#4CAF50', '#2196F3', '#FF9800', '#F44336', '#9C27B0',
        '#00BCD4', '#FFEB3B', '#795548', '#607D8B', '#E91E63'
      ];
      
      // If we need more colors than we have, repeat the colors
      const result = [];
      for (let i = 0; i < count; i++) {
        result.push(colors[i % colors.length]);
      }
      return result;
    };

    onMounted(() => {
      loadAnalytics();
    });

    return {
      stockUploadStore,
      analytics,
      showExportOptions,
      loadAnalytics,
      refreshAnalytics,
      exportData,
      hideExportOptions,
      exportInFormat,
      formatCurrency,
      formatCategoriesForChart,
      formatSuppliersForChart
    };
  }
};
</script>

<style scoped>
.stock-analytics-panel {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.analytics-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #333;
}

.loading-analytics {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-analytics {
  text-align: center;
  padding: 30px;
}

.analytics-button {
  padding: 8px 16px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.analytics-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 15px;
  margin-bottom: 25px;
}

.analytics-card {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.analytics-card.total-items {
  background-color: #e3f2fd;
}

.analytics-card.total-value {
  background-color: #e8f5e9;
}

.analytics-card.low-stock {
  background-color: #ffebee;
}

.card-value {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 5px;
}

.card-label {
  font-size: 14px;
  color: #666;
}

.analytics-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 25px;
}

@media (max-width: 768px) {
  .analytics-details {
    grid-template-columns: 1fr;
  }
}

.analytics-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
}

.analytics-section h5 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.pie-chart {
  height: 200px;
  margin-bottom: 15px;
}

.analytics-table table {
  width: 100%;
  border-collapse: collapse;
}

.analytics-table th, .analytics-table td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.analytics-table th {
  font-weight: 600;
  color: #555;
}

.high-value-items {
  margin-bottom: 25px;
}

.high-value-items h5 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.analytics-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.refresh-button, .export-button {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.refresh-button {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  color: #333;
}

.export-button {
  background-color: #4CAF50;
  color: white;
  border: none;
}

.export-options {
  margin-top: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
}

.export-options h5 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.format-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.format-button, .cancel-button {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.format-button {
  background-color: #2196F3;
  color: white;
  border: none;
}

.cancel-button {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  color: #333;
}
</style>