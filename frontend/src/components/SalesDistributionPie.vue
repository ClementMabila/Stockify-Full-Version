<template>
  <div class="p-4 bg-white rounded-lg shadow-md" style="width: 400px; height: 310px; margin-top: 20px; margin-right: 100px;">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg bar-title font-semibold" style="font-weight: bold;"><span class="main-span">Inventory</span> Distribution</h2>
      <div v-if="isLoading" class="text-sm text-gray-500">Loading...</div>
      <select v-model="selectedView" class="border p-2 rounded">
        <option value="category">By Category</option>
        <option value="supplier">By Supplier</option>
      </select>
    </div>

    <div v-if="error" class="text-center text-red-500 py-6">
      {{ error }}
    </div>
    
    <div v-else class="pie-container">
      <canvas ref="chartCanvas"></canvas>
    </div>

    <div
      v-if="!isLoading && !error"
      class="relative mt-4 flex justify-center"
    >
      <div
        class="transition-all duration-500 ease-in-out h-10 w-full flex flex-col items-center overflow-hidden"
      >
        <transition-group name="fade" tag="div">
          <div
            v-for="(label, index) in visibleLabels"
            :key="label"
            class="flex items-center mx-2 my-1"
          >
            <div
              class="w-4 h-4 rounded-sm mr-2"
              :style="{ backgroundColor: colors[index % colors.length] }"
            ></div>
            <span class="text-sm">{{ label }}</span>
          </div>
        </transition-group>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, computed, watch } from "vue";
import Chart from "chart.js/auto";
import http from "../services/http";

export default defineComponent({
  setup() {
    const chartCanvas = ref(null);
    const chart = ref(null);
    const isLoading = ref(true);
    const error = ref(null);
    const analytics = ref(null);
    const selectedView = ref("category");

    // Chart colors - extended to handle more categories if needed
    const colors = [
       "#d59bf6", "#8a8a8a", "#cbf078", "#edb1f1",
    ];

    const currentLabels = computed(() => {
      if (!analytics.value) return [];
      
      if (selectedView.value === "category") {
        return Object.keys(analytics.value.categories);
      } else {
        return Object.keys(analytics.value.suppliers);
      }
    });
    
    const visibleLabels = ref([]);
    let startIndex = 0;
    const displayCount = 5;

    const updateVisibleLabels = () => {
      const labels = currentLabels.value;
      if (labels.length === 0) {
        visibleLabels.value = [];
        return;
      }

      const endIndex = startIndex + displayCount;
      visibleLabels.value = labels.slice(startIndex, endIndex);

      startIndex = endIndex >= labels.length ? 0 : startIndex + displayCount;
    };

    // Automatically scroll labels every 5 seconds
    onMounted(() => {
      fetchAnalytics();
      setInterval(updateVisibleLabels, 5000);
    });

    watch(currentLabels, () => {
      startIndex = 0;
      updateVisibleLabels();
    });

    const currentData = computed(() => {
      if (!analytics.value) return [];
      
      if (selectedView.value === "category") {
        return Object.values(analytics.value.categories);
      } else {
        return Object.values(analytics.value.suppliers);
      }
    });

    const fetchAnalytics = async () => {
      isLoading.value = true;
      error.value = null;
      
      try {
        analytics.value = await http.get("/api/stock/analysis/");
        updateChart();
      } catch (err) {
        error.value = "Failed to load analytics data. Please try again.";
        console.error("Error fetching analytics:", err);
      } finally {
        isLoading.value = false;
      }
    };

    const createChart = () => {
      const ctx = chartCanvas.value.getContext("2d");
      
      chart.value = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: currentLabels.value,
          datasets: [
            {
              data: currentData.value,
              backgroundColor: colors.slice(0, currentLabels.value.length),
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              enabled: true,
              callbacks: {
                label: function(context) {
                  const value = context.raw;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = Math.round((value / total) * 100);
                  return `${context.label}: ${value} (${percentage}%)`;
                }
              }
            },
            title: {
              display: true,
              text: selectedView.value === "category" ? "Category Distribution" : "Supplier Distribution",
            },
          },
        },
      });
    };

    const updateChart = () => {
      if (chart.value) {
        chart.value.destroy();
      }
      
      if (chartCanvas.value) {
        createChart();
      }
    };

    const refreshData = () => {
      fetchAnalytics();
    };

    watch(selectedView, () => {
      if (chart.value) {
        chart.value.data.labels = currentLabels.value;
        chart.value.data.datasets[0].data = currentData.value;
        chart.value.options.plugins.title.text = 
          selectedView.value === "category" ? "Category Distribution" : "Supplier Distribution";
        chart.value.update();
      }
    });

    onMounted(() => {
      fetchAnalytics();
    });

    return {
      chartCanvas,
      isLoading,
      error,
      selectedView,
      colors,
      currentLabels,
      refreshData,
      visibleLabels,
    };
  },
});
</script>

<style scoped>
.pie-container {
  width: 150px;
  height: 150px;
  margin: auto;
  margin-bottom: -80px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.main-span {
  background: linear-gradient(to right, #edb1f1 70%, #d59bf6 30%);
  -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

</style>