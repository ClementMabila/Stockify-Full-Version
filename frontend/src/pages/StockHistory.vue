<template>
  <div class="stock-history-container">
    <h4 class="history-heading">Recent Purchases</h4>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Transaction Date</th>
            <th>Category</th>
            <th>Product</th>
            <th>Uruantial Revenue</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="history in latestStockHistory" :key="history.id">
            <td>{{ formatDate(history.transaction_date) }}</td>
            <td>{{ history.transaction_type }}</td>
            <td>{{ history.product }}</td>
            <td>${{ parseFloat(history.total_revenue).toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { fetchStockHistory } from "../store/stockHistory";

export default {
  data() {
    return {
      stockHistory: [],
    };
  },
  async created() {
    try {
      const data = await fetchStockHistory();
      this.stockHistory = data;
    } catch (error) {
      console.error("Error fetching stock history:", error);
      alert("You are not authorized to view stock history or you are not logged in.");
    }
  },
  computed: {
    latestStockHistory() {
      return this.stockHistory.slice(0, 2);
    },
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
  },
};
</script>

<style src="../assets/css/dashboard.css"></style>
