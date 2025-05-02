<template>
  <div class="p-4 bg-white rounded-lg shadow-md" style="margin-top: 20px;">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg bar-title font-semibold" style="font-weight: bold;">Sales & Stock Comparison</h2>
      <select v-model="selectedYear" class="border p-2 rounded">
        <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
      </select>
    </div>

    <div class="flex gap-4 mb-2">
      <div class="flex items-center">
        <div class="w-4 h-4 bg-black rounded-sm mr-2"></div>
        <span class="text-sm">Sales</span>
      </div>
      <div class="flex items-center">
        <div class="w-4 h-4 bg-gray-500 rounded-sm mr-2"></div>
        <span class="text-sm">Stock</span>
      </div>
    </div>

    <div class="chart-container">
      <canvas id="myChart"></canvas>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, computed, onMounted, watch, nextTick } from "vue";
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from "chart.js";
import axios from "axios";

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default defineComponent({
  setup() {
    const selectedYear = ref("2022");
    const salesData = ref({});
    const chartInstance = ref(null);

    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/sales-stock/");
        salesData.value = response.data;
        renderChart(); 
      } catch (error) {
        console.error("Error fetching chart data:", error);
      }
    };

    const renderChart = async () => {
      await nextTick(); 

      const chartContainer = document.querySelector(".chart-container");
      chartContainer.innerHTML = '<canvas id="myChart"></canvas>';

      if (!selectedYear.value || !salesData.value[selectedYear.value]) return;

      const yearData = salesData.value[selectedYear.value];
      const ctx = document.getElementById("myChart").getContext("2d");

      const chartData = {
        labels: yearData.map((d) => d.month),
        datasets: [
          {
            label: "Sales",
            data: yearData.map((d) => d.Sales),
            backgroundColor: "black",
            barThickness: 20,
            maxBarThickness: 20,
            borderRadius: 2,
          },
          {
            label: "Stock",
            data: yearData.map((d) => d.Stock),
            backgroundColor: "gray",
            barThickness: 20,
            maxBarThickness: 20,
            borderRadius: 2,
          },
        ],
      };

      const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: {
            grid: { display: false },
            categoryPercentage: 0.8,
            barPercentage: 0.5,
          },
          y: {
            beginAtZero: true,
            grid: { color: "#e0e0e0" },
          },
        },
      };

      if (chartInstance.value) {
        chartInstance.value.destroy(); 
      }

      chartInstance.value = new Chart(ctx, {
        type: "bar",
        data: chartData,
        options: chartOptions,
      });
    };

    watch(selectedYear, renderChart);

    onMounted(() => {
      fetchData().then(() => {
        const years = Object.keys(salesData.value);
        if (years.length > 0) {
          selectedYear.value = years[years.length - 1];
        }
      });
    });

    return {
      selectedYear,
      availableYears: computed(() => Object.keys(salesData.value)),
    };
  },
});
</script>

<style scoped>
.chart-container {
  height: 170px;
  width: 100%;
}
</style>