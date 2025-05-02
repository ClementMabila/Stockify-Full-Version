<template>
  <BaseLayout>
  <div class="sales-entrie-container">
    <h4 class="history-heading">Stock History</h4>
    <div class="sales-actions">
        <div class="search-field-fields">
          <img src="../assets/images/search.png" alt="Search" class="search-icon">
          <input type="text" placeholder="Search stock..." />
        </div>
        <div class="header-entry-icons">
          <button class="entry-icon-button" @click="toggleFilter">
            <img src="../assets/images/filter.png" alt="Search" class="entry-icons">
            <span> Filter</span>
          </button>
          <button class="entry-icon-button-black" @click="showModal = true">
          <img src="../assets/images/upload1.png" alt="Add" class="csv-icon">
          <span> Upload CSV</span>
        </button>
        <div class="csv-modal-overlay">
        <div v-if="showModal">
          <div class="csv-modal-content">
            <input type="file" @change="handleFileUpload" accept=".csv" class="csv-input"/>
            <button class="csv-buttons" @click="submitCSV">Submit CSV</button>
            <button class="csv-buttons" @click="showModal = false">Close</button>
      </div>
        </div>
      </div>
        </div>
    </div>
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
          <tr v-for="history in stockHistory" :key="history.id">
            <td>{{ formatDate(history.transaction_date) }}</td>
            <td>{{ history.transaction_type }}</td>
            <td>{{ history.product }}</td>
            <td>${{ parseFloat(history.total_revenue).toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</BaseLayout>
</template>

<script>
import BaseLayout from "../components/BaseLayout.vue";
import { fetchStockHistory } from "../store/stockHistory";

export default {
  name: "StockHistoryPage",
  components: {
    BaseLayout,
  },
  data() {
    return {
      stockHistory: [],
      showModal: false,
      csvFile: null,
    };
  },
  async created() {
    try {
      this.stockHistory = await fetchStockHistory();
    } catch (error) {
      console.error("Failed to fetch stock history:", error);
      alert("You are not authorized to view this data or you are not logged in.");
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    handleFileUpload(event) {
      this.csvFile = event.target.files[0];
    },
    async submitCSV() {
      if (!this.csvFile) {
        alert("Please select a CSV file first!");
        return;
      }

      const formData = new FormData();
      formData.append("csv_file", this.csvFile);

      try {
        const response = await fetch("http://127.0.0.1:8000/api/upload-csv/", {
          method: "POST",
          body: formData,
          credentials: "include",
        });

        if (!response.ok) throw new Error("Upload failed");
        alert("CSV uploaded successfully");
        this.showModal = false;
        this.csvFile = null;
      } catch (error) {
        console.error("Error uploading CSV:", error);
        alert("Failed to upload CSV");
      }
    },
  },
};
</script>

<style src="../assets/css/dashboard.css"></style>
