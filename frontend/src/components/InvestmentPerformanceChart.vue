<template>
  <div class="p-4 bg-white rounded-lg shadow-md" style="width: auto; height: 247px;">
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
  </template>
  
  <script>
  import { ref, onMounted, watch } from 'vue'

  import {
    Chart,
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    Tooltip,
    CategoryScale,
  } from 'chart.js'
  import { fetchInvestmentPerformance } from '../store/InvestmentsPerformance'
  
  Chart.register(
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    Tooltip,
    CategoryScale
  )
  
  export default {
    name: 'InvestmentPerformanceChart',
    setup(props, { emit }) {
      const chartCanvas = ref(null)
      const performanceData = ref([])
      const currentValue = ref(0)
      let chartInstance = null
  
      const createChart = () => {
      if (!performanceData.value.length) return;
      if (chartInstance) chartInstance.destroy();

      const ctx = chartCanvas.value.getContext('2d');
      const gradient = ctx.createLinearGradient(0, 0, 0, 230);
      gradient.addColorStop(0, '#7dd87d'); 
      gradient.addColorStop(0.1, '#c2ebc2');
      gradient.addColorStop(0.79, '#ffffff');


      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: performanceData.value.map((item) => item.label),
          datasets: [
            {
              label: 'Investment Growth',
              data: performanceData.value.map((item) => item.value),
              borderColor: '#7dd87d',
              backgroundColor: gradient,
              pointBackgroundColor: '#7dd87d',
              tension: 0.4,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => `Value: ${ctx.raw.toLocaleString()}`,
              },
            },
          },
          scales: {
            y: {
            position: 'right',
            beginAtZero: true,
            ticks: {
              stepSize: 2000,
              callback: (val) => `${val / 1000}k`,
              padding: 10,
              display: true,
            },
            grid: {
            drawTicks: false,
            drawBorder: false,
            color: '#eeeeee',
            borderDash: [4, 4],
            lineWidth: 1,
            z: 1, 
            display: true,
            drawOnChartArea: true,
          },
          },
            x: {
              grid: {
                drawOnChartArea: false,
              },
            },
          },
        },
      });
    };

  
      onMounted(async () => {
      try {
        const data = await fetchInvestmentPerformance()
        performanceData.value = data.performance

        if (performanceData.value.length >= 2) {
          const start = performanceData.value[0].value
          const end = performanceData.value[performanceData.value.length - 1].value
          const isRising = end > start
          const percentageChange = ((end - start) / start) * 100

          emit('trendSignal', {
            direction: isRising ? 'up' : 'down',
            percentage: Math.abs(percentageChange.toFixed(2))
          })
        }

        currentValue.value = data.current_value
        createChart()
      } catch (error) {
        console.error('Error loading performance:', error)
      }
    })
  
      watch(performanceData, () => {
        createChart()
      })
  
      return { chartCanvas }
    },
  }
  </script>
  
  <style scoped>
  .chart-container {
    height: 210px;
    width: 470px;
    position: relative;
  }
  </style>
