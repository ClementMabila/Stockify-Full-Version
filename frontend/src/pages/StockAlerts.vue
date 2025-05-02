<template>
  <div class="stock-alerts">
    <h2 class="history-heading">Stock Alerts</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Request Date</th>
            <th>Product</th>
            <th>Requested Quantity</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alert in latestAlerts" :key="alert.request_date">
            <td>{{ formatDate(alert.request_date) }}</td>
            <td>{{ alert.product }}</td>
            <td>{{ alert.requested_quantity }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { fetchRestockAlerts } from "../store/restockRequest";

export default {
  data() {
    return {
      stockAlerts: [],
    };
  },
  computed: {
    latestAlerts() {
      return this.stockAlerts.slice(0, 4);
    }
  },
  async created() {
    try {
      const data = await fetchRestockAlerts();
      this.stockAlerts = data.reverse();  // Keep your original display logic
    } catch (error) {
      console.error('Error fetching stock alerts:', error);
      alert("You are not authorized to view restock alerts or you are not logged in.");
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      return dateString.split('T')[0];
    }
  }
};
</script>
