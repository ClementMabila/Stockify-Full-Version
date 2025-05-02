<template>
    <div class="p-4 bg-white rounded-lg shadow-md" style="width: 400px; height: 310px; margin-top: 20px; margin-right: 100px;">
 
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg bar-title font-semibold" style="font-weight: bold;">Distributions</h2>
        <select v-model="selectedYear" class="border p-2 rounded">
          <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
        </select>
      </div>

      <div class="pie-container">
        <canvas ref="chartCanvas"></canvas>
      </div>

      <div class="flex flex-wrap justify-center mt-4">
        <div v-for="(category, index) in categories" :key="index" class="flex items-center mx-2 my-1">
          <div class="w-4 h-4 rounded-sm mr-2" :style="{ backgroundColor: colors[index] }"></div>
          <span class="text-sm">{{ category }}</span>
        </div>
      </div>

      <div class="flex justify-center mt-4">
        <button v-for="(action, index) in actions" :key="index" class="bg-gray-200 p-2 rounded mx-1 text-xs"
          @click="action.handler(chart)">
          {{ action.name }}
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, onMounted } from "vue";
  import Chart from "chart.js/auto";
  
  export default defineComponent({
    setup() {
      const chartCanvas = ref(null);
      const chart = ref(null);
      const selectedYear = ref("2024");

      const salesData = {
        2024: { Gear: 3000, Lighting: 2500, Screens: 1800, Electronics: 2200, "Tire & Wheels": 2700 },
        2023: { Gear: 2800, Lighting: 2400, Screens: 1700, Electronics: 2000, "Tire & Wheels": 2600 },
      };
  
      const categories = ["Gear", "Lighting", "Screens", "Electronics", "Tire & Wheels"];
      const colors = ["#4a4a4a", "#6d6d6d", "#8a8a8a", "#b0b0b0", "#d3d3d3"];
  
      const data = ref({
        labels: categories,
        datasets: [
          {
            label: "Dataset 1",
            data: categories.map((category) => salesData[selectedYear.value][category]),
            backgroundColor: colors,
          },
        ],
      });
  
      const config = ref({
        type: "doughnut",
        data: data.value,
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false, 
            },
            tooltip: {
              enabled: true,
            },
            title: {
              display: true,
              text: "Sales Distribution",
            },
          },
        },
      });

      const actions = [
        {
          name: "Randomize",
          handler(chart) {
            chart.data.datasets.forEach((dataset) => {
              dataset.data = categories.map(() => Math.floor(Math.random() * 100));
            });
            chart.update();
          },
        },
        {
          name: "Add Dataset",
          handler(chart) {
            const newDataset = {
              label: `Dataset ${chart.data.datasets.length + 1}`,
              backgroundColor: colors,
              data: categories.map(() => Math.floor(Math.random() * 100)),
            };
            chart.data.datasets.push(newDataset);
            chart.update();
          },
        },
        {
          name: "Remove Dataset",
          handler(chart) {
            chart.data.datasets.pop();
            chart.update();
          },
        },
      ];
  
      onMounted(() => {
        chart.value = new Chart(chartCanvas.value, config.value);
      });
  
      return {
        chartCanvas,
        selectedYear,
        availableYears: Object.keys(salesData),
        categories,
        colors,
        actions,
        chart,
      };
    },
  });
  </script>
  
  <style scoped>
  .pie-container {
    width: 150px;
    height: 150px;
    margin: auto;
    margin-bottom: -90px;
  }
  </style>
  