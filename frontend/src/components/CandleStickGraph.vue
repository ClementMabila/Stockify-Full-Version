<template>
  <div class="p-6 bg-gray-50 rounded-xl shadow-lg">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-800 heading-style">Stock Investment Analytics</h2>
      <div class="flex space-x-3">
        <button 
          @click="activeTimeframe = 'daily'" 
          class="px-3 py-1.5 rounded-md transition-colors button-style" 
          :class="activeTimeframe === 'daily' ? 'bg-blue-600' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
        >
          Daily
        </button>
        <button 
          @click="activeTimeframe = 'monthly'" 
          class="px-3 py-1.5 rounded-md transition-colors button-style-black" 
          :class="activeTimeframe === 'monthly' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
        >
          Monthly
        </button>
      </div>
    </div>

    <div class="bg-white p-4 rounded-lg shadow-sm mb-6 card-added-style">
      <div class="flex justify-between items-center mb-3">
        <div>
          <span class="text-gray-500 text-sm font-inc-style">Current Price</span>
          <div class="text-2xl font-bold text-gray-900 curr-price-style">{{ currentPrice }}</div>
        </div>
        <div :class="priceChange >= 0 ? 'text-green-600' : 'text-red-600'" class="flex items-center">
          <span class="text-2xl font-semibold black-button-style">{{ priceChange >= 0 ? '+' : '' }}{{ priceChange }}%</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" :class="priceChange >= 0 ? 'rotate-0' : 'rotate-180'">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
          </svg>
        </div>
      </div>

      <div class="flex space-x-4 flex-styled">
        <div class="text-sm">
          <span class="text-gray-500 font-inc-style">Open</span>
          <div class="font-medium text-gray-800 styled-curr-stats">{{ currentOpen }}</div>
        </div>
        <div class="text-sm">
          <span class="text-gray-500 font-inc-style">High</span>
          <div class="font-medium text-gray-800 styled-curr-stats">{{ currentHigh }}</div>
        </div>
        <div class="text-sm">
          <span class="text-gray-500 font-inc-style">Low</span>
          <div class="font-medium text-gray-800 styled-curr-stats-sec">{{ currentLow }}</div>
        </div>
        <div class="text-sm">
          <span class="text-gray-500 font-inc-style">Volume</span>
          <div class="font-medium text-gray-800 styled-curr-stats-sec">{{ formattedVolume }}</div>
        </div>
      </div>
    </div>

    <div class="mb-4">
      <div class="flex items-center space-x-2 mb-4">
        <div class="h-3 w-3 rounded-full bg-blue-600"></div>
        <h3 class="text-lg font-semibold text-gray-800 heading-style">{{ activeTimeframe === 'daily' ? 'Daily' : 'Monthly' }} Performance</h3>
      </div>
      <div class="chart-container bg-white rounded-lg shadow-sm p-4">
        <div v-if="loading" class="flex items-center justify-center h-full">
          <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600"></div>
        </div>
        <div v-else-if="error" class="flex items-center justify-center h-full text-red-500">
          {{ error }}
        </div>
        <canvas v-else id="stockChart"></canvas>
      </div>
    </div>

    <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 flexed-style-bottom">
      <div class="p-4 rounded-lg shadow-sm styled-banners">
        <h4 class="text-sm font-medium banner-texts-bottom mb-1">Market Cap</h4>
        <p class="text-lg font-bold text-gray-800">$4.85B</p>
      </div>
      <div class="styled-banners-a p-4 rounded-lg shadow-sm">
        <h4 class="text-sm font-medium banner-texts-bottom mb-1">52W Range</h4>
        <p class="text-lg font-bold text-gray-800">$125.30 - $298.76</p>
      </div>
      <div class="styled-banners-aa p-4 rounded-lg shadow-sm">
        <h4 class="text-sm font-medium banner-texts-bottom mb-1" style="color: #444;">Avg. Volume</h4>
        <p class="text-lg font-bold text-gray-800">1.2M</p>
      </div>
    </div>
  </div>
</template>

<script>
import {
  Chart,
  TimeScale,
  LinearScale,
  Tooltip,
  Title,
  Legend,
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { CandlestickController, CandlestickElement } from 'chartjs-chart-financial';
import StockCandlestickService from '../store/candleSticks.js';

Chart.register(
  TimeScale,
  LinearScale,
  Tooltip,
  Title,
  Legend,
  CandlestickController,
  CandlestickElement
);

export default {
  name: 'EnhancedStockChart',
  data() {
    return {
      chart: null,
      dailyData: [],
      monthlyData: [],
      loading: true,
      error: null,
      activeTimeframe: 'daily',
      currentPrice: '$0.00',
      currentOpen: '$0.00',
      currentHigh: '$0.00',
      currentLow: '$0.00',
      priceChange: 0,
      volume: 0
    };
  },
  computed: {
    formattedVolume() {
      if (this.volume > 1000000) {
        return `${(this.volume / 1000000).toFixed(1)}M`;
      } else if (this.volume > 1000) {
        return `${(this.volume / 1000).toFixed(1)}K`;
      }
      return this.volume.toLocaleString();
    }
  },
  watch: {
    activeTimeframe() {
      this.updateChart();
    }
  },
  async mounted() {
    await this.fetchData();
    this.updateChart();
  },
  methods: {
    async fetchData() {
      try {
        const data = await StockCandlestickService.getCandlestickData();
        console.log('Raw API data:', data);

        if (!data) {
          throw new Error('No data returned from API');
        }

        // Helper to simulate OHLC from total_amount
        const withOHLC = (entry) => {
          const base = parseFloat(entry.total_amount);
          const swing = base * 0.07; // 7% swing for realism
          
          // Generate more realistic price movements
          const open = base * (1 + (Math.random() * 0.02 - 0.01));
          const close = base * (1 + (Math.random() * 0.03 - 0.015));
          
          // High and low should logically relate to open/close
          const high = Math.max(open, close) * (1 + Math.random() * 0.01);
          const low = Math.min(open, close) * (1 - Math.random() * 0.01);
          
          // Generate realistic volume
          const volume = Math.floor(base * 100 * (Math.random() * 3 + 0.5));

          return {
            x: new Date(entry.day || entry.month).getTime(),
            o: parseFloat(open.toFixed(2)),
            h: parseFloat(high.toFixed(2)),
            l: parseFloat(low.toFixed(2)),
            c: parseFloat(close.toFixed(2)),
            v: volume
          };
        };

        this.monthlyData = data.monthly_data?.map(withOHLC) || [];
        this.dailyData = data.daily_data?.map(withOHLC) || [];

        if (this.dailyData.length > 0) {
          const latest = this.dailyData[this.dailyData.length - 1];
          const previous = this.dailyData[this.dailyData.length - 2] || latest;
          
          this.currentPrice = `$${latest.c.toFixed(2)}`;
          this.currentOpen = `$${latest.o.toFixed(2)}`;
          this.currentHigh = `$${latest.h.toFixed(2)}`;
          this.currentLow = `$${latest.l.toFixed(2)}`;
          this.volume = latest.v;
          
          // Calculate percent change
          this.priceChange = ((latest.c - previous.c) / previous.c * 100).toFixed(2);
        }

        this.loading = false;
      } catch (error) {
        console.error('Failed to load candlestick data', error);
        this.error = error.message;
        this.loading = false;
      }
    },
    updateChart() {
      const ctx = document.getElementById('stockChart');
      if (!ctx) return;

      if (this.chart) {
        this.chart.destroy();
      }

      const chartData = this.activeTimeframe === 'daily' ? this.dailyData : this.monthlyData;
      
      if (chartData.length === 0) {
        this.error = `No ${this.activeTimeframe} data available`;
        return;
      }

      // Create line data from closing prices
      const lineData = chartData.map(entry => ({
        x: entry.x,
        y: entry.c
      }));

      // Calculate moving average
      const movingAvgPeriod = this.activeTimeframe === 'daily' ? 5 : 3;
      const movingAvgData = [];
      
      for (let i = 0; i < chartData.length; i++) {
        if (i >= movingAvgPeriod - 1) {
          let sum = 0;
          for (let j = 0; j < movingAvgPeriod; j++) {
            sum += chartData[i - j].c;
          }
          movingAvgData.push({
            x: chartData[i].x,
            y: parseFloat((sum / movingAvgPeriod).toFixed(2))
          });
        }
      }

      // Create gradient for line area
      const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
      gradient.addColorStop(0, 'rgba(37, 99, 235, 0.2)');
      gradient.addColorStop(1, 'rgba(37, 99, 235, 0)');

      this.chart = new Chart(ctx.getContext('2d'), {
        data: {
          datasets: [
            {
              label: this.activeTimeframe === 'daily' ? 'Daily OHLC' : 'Monthly OHLC',
              data: chartData,
              type: 'candlestick',
              color: {
                up: '#10B981',
                down: '#EF4444',
                unchanged: '#6B7280',
              },
              borderColor: {
                up: '#10B981',
                down: '#EF4444',
                unchanged: '#6B7280'
              }
            },
            {
              label: 'Closing Price',
              data: lineData,
              type: 'line',
              borderColor: '#2563EB',
              backgroundColor: gradient,
              borderWidth: 2,
              pointRadius: 0,
              fill: true,
              tension: 0.2,
              order: 1
            },
            {
              label: `${movingAvgPeriod}-Period MA`,
              data: movingAvgData,
              type: 'line',
              borderColor: '#6D28D9',
              borderWidth: 1.5,
              pointRadius: 0,
              borderDash: [3, 3],
              fill: false,
              tension: 0.1,
              order: 0
            }
          ]
        },
        options: this.getChartOptions()
      });
    },
    getChartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            top: 20,
            right: 20,
            bottom: 10,
            left: 10
          }
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: this.activeTimeframe === 'daily' ? 'day' : 'month',
              tooltipFormat: 'PPP',
              displayFormats: {
                day: 'MMM d',
                month: 'MMM yyyy'
              }
            },
            grid: {
              display: true,
              color: 'rgba(226, 232, 240, 0.8)'
            },
            ticks: {
              color: '#64748B',
              font: {
                size: 11,
                family: "'Inter', sans-serif"
              },
              maxRotation: 0
            }
          },
          y: {
            position: 'right',
            grid: {
              display: true,
              color: 'rgba(226, 232, 240, 0.8)',
              drawBorder: false
            },
            ticks: {
              callback: function(value) {
                return '$' + value.toLocaleString();
              },
              color: '#64748B',
              font: {
                size: 11,
                family: "'Inter', sans-serif"
              }
            }
          }
        },
        plugins: {
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            titleColor: '#1F2937',
            bodyColor: '#374151',
            borderColor: '#E5E7EB',
            borderWidth: 1,
            cornerRadius: 6,
            padding: 10,
            boxPadding: 4,
            usePointStyle: true,
            titleFont: {
              size: 14,
              weight: 'bold',
              family: "'Inter', sans-serif"
            },
            bodyFont: {
              size: 12,
              family: "'Inter', sans-serif"
            },
            callbacks: {
              label: function(context) {
                if (context.datasetIndex === 0) {
                  const { o, h, l, c } = context.raw;
                  return [
                    `Open: $${o.toFixed(2)}`,
                    `High: $${h.toFixed(2)}`,
                    `Low: $${l.toFixed(2)}`,
                    `Close: $${c.toFixed(2)}`
                  ];
                } else {
                  return `${context.dataset.label}: $${context.parsed.y.toFixed(2)}`;
                }
              }
            }
          },
          legend: {
            display: true,
            position: 'top',
            align: 'end',
            labels: {
              color: '#64748B',
              boxWidth: 12,
              usePointStyle: true,
              pointStyle: 'circle',
              font: {
                size: 11,
                family: "'Inter', sans-serif"
              }
            }
          },
          title: {
            display: false
          }
        },
        interaction: {
          mode: 'index',
          intersect: false
        },
        animation: {
          duration: 1000,
          easing: 'easeOutQuart'
        }
      };
    }
  },
  beforeUnmount() {
    if (this.chart) this.chart.destroy();
  }
};
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}

button {
  font-size: 14px;
  font-weight: 500;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

.loading {
  animation: pulse 1.5s infinite;
}

.button-style {
  background-color: white;
  color: #444;
  border: 1px solid #444;
  font-size: 13px;
  border-radius: 10px;
  margin-right: 8px;
}

.button-style-black {
  border-radius: 10px;
  font-size: 13px;
  margin-right: 6px;
  background-color: #d59bf6;
  color: white;
}

.heading-style {
  padding: 10px;
  margin-right: 180px;
  color: black;
}

.card-added-style {
  border-radius: 10px;
}

.flex-styled {
  display: flex;
}

.styled-curr-stats {
  background-color: white;
  border-radius: 10px;
  margin-right: 5px;
  padding: 10px;
  font-size: 9px;
  color: #b2d430;
}

.styled-curr-stats-sec {
  background-color: white;
  border-radius: 10px;
  margin-right: 5px;
  padding: 10px;
  font-size: 9px;
  color: #b2d430;
  border: 1px solid transparent;
  font-family: Arial, Helvetica, sans-serif;
}
.font-inc-style {
  font-size: 11px;
  color: #4444;
  margin-right: 10px;
  font-family: Arial, Helvetica, sans-serif;
}

.curr-price-style {
  font-size: 11px;
  background-color: white;
  border: 1px solid #d59bf6;
  border-radius: 10px;
  padding: 10px;
  font-family: Arial, Helvetica, sans-serif;
}

.black-button-style{
  margin-bottom: -24px;
  font-size: 11px;
  background-color: #d59bf6;
  color: white;
  padding: 10px;
  border-radius: 10px;
  font-family: Arial, Helvetica, sans-serif;
}

.flexed-style-bottom {
  display: flex;
}

.styled-banners {
  background-color: #d59bf6;
  margin-left: 10px;
  margin-bottom: 10px;
  color: white;
  font-size: 12px;
  font-weight: bold;
  font-family: Arial, Helvetica, sans-serif;
  height: 70px;
}

.banner-texts-bottom {
  color: white;
  font-family: Arial, Helvetica, sans-serif;
}

.styled-banners-a {
  background-color: #b2d430;
  margin-left: 10px;
  margin-bottom: 10px;
  color: white;
  font-size: 12px;
  font-weight: bold;
  font-family: Arial, Helvetica, sans-serif;
  height: 70px;
}

.styled-banners-aa {
  background-color: white;
  border: 1px solid black;
  border-radius: 10px;
  margin-left: 10px;
  margin-bottom: 10px;
  color: #444;
  font-size: 12px;
  font-weight: bold;
  font-family: Arial, Helvetica, sans-serif;
  height: 68px;
  align-items: center;
  text-align: center;
}
</style>