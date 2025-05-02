<template>
  <div class="p-6 max-w-3xl mx-auto bg-white shadow rounded-xl" style="border-radius: 10px; width: 350px; height: 220px; margin-left: -250px;">
    <h2 class="Investment-det-heading">Investment Details</h2>

    <div v-if="loading">
      <p>Loading investment details...</p>
    </div>

    <div v-else-if="error">
      <p class="text-red-600">Error: {{ error }}</p>
    </div>
    
    <div v-else-if="investment">
      <div class="mb-4 flex items-center" style="margin-top: -4px;">
        <h4 class="text-xl font-bold mr-2" style="margin-top: -4px;">
          <span><img src="../assets/images/info-icon.png" alt="Info" class="image-info" /></span>
          {{ investment.supplier_name || 'N/A' }}
        </h4>
      </div>

      <div class="Investment-det-data" style="padding: 10px; height: auto; margin-top: -60px;">
        <div class="metrics-grid">
          <div>
            <p class="label">Amount</p>
            <p class="value">${{ investment.amount ?? '0.00' }}</p>
          </div>
          <div>
            <p class="label">Growth Rate</p>
            <p class="value">{{ investment.performance?.growth_rate ?? '0' }}%</p>
          </div>
          <div>
            <p class="label-below">Profit Amount</p>
            <p class="value" style="color: #c1f880;" >${{ investment.profit_amount ?? '0.00' }}</p>
          </div>
          <div>
            <p class="label-below">Total Return</p>
            <p class="value" style="color: #c1f880;">${{ investment.total_return ?? '0.00' }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <p>No investment data available.</p>
    </div>

    <div class="buttons-section">
      <button @click="goTo('InvestmentPerformance')" class="bt-sec-btn" style="background-color: #a1f480;">
        <img src="../assets/images/stocks-1.png" alt="Investment" class="icon" />
        <span>Investment</span>
      </button>
      <button @click="goTo('InvestmentHistory')" class="bt-sec-btn blue" style="background-color: #d59bf6;">
        <img src="../assets/images/chart-1.png" alt="Chart" class="icon" />
        <span>Analytics</span>
      </button>
      <button @click="openInvestModal" class="bt-sec-btn purple" style="border: 1px solid #4444; color: #4444;">
        <img src="../assets/images/Deposit.png" alt="Deposit" class="icon" />
        <span>Deposit</span>
      </button>
      <button @click="goTo('InvestmentDetails')" class="bt-sec-btn purple" style="border: 1px solid #4444; color: #4444;">
        <img src="../assets/images/withdraw.png" alt="Withdraw" class="icon" />
        <span>Withdraw</span>
      </button>
    </div>

    <!-- Investment Modal -->
    <div v-if="showInvestModal" class="modal-overlay" @click.self="closeInvestModal">
      <div class="modal-content">
        <button class="close-btn" @click="closeInvestModal">✕</button>
        <h4 class="Invest-in-heading">Open Stocks</h4>
        <p class="Inv-message">
          <span><img src="../assets/images/info-icon.png" alt="Info" class="image-info" /></span>
          Select a stock from the table below to view its details and proceed with your investment.
          Click the "Show reviews" link to read what other investors are saying.
        </p>
        <div v-if="stocks.length" class="overflow-x-auto">
          <table class="min-w-full bg-white rounded shadow">
            <thead>
              <tr class="bg-gray-100 text-left">
                <th class="p-3">Stock</th>
                <th class="p-3">Organization</th>
                <th class="p-3">Supplier</th>
                <th class="p-3">Product</th>
                <th class="p-3">Quantity</th>
                <th class="p-3">Investors</th>
                <th class="p-3">Reviews</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(stock, index) in stocks"
                :key="stock.id"
                @click="selectStock(stock)"
                class="cursor-pointer hover:bg-gray-50"
              >
                <td class="p-3">{{ index + 1 }}</td>
                <td class="p-3">{{ stock.organization }}</td>
                <td class="p-3">{{ stock.supplier }}</td>
                <td class="p-3">{{ stock.product }}</td>
                <td class="p-3">{{ stock.quantity }}</td>
                <td class="p-3">{{ stock.number_of_investors }}</td>
                <td class="p-3 text-blue-600 underline">
                  <a class="reviews-links" @click.stop.prevent="viewReviews(stock.id)">Show reviews</a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else>
          <p>No investable stocks available.</p>
        </div>
      </div>
    </div>

<div v-if="showStockDetailsModal" class="modal-overlay" style="margin-top: 20px;" @click.self="closeStockDetailsModal">
  <div class="modal-content p-4 bg-white rounded-xl shadow-lg max-w-md mx-auto relative">
    <button class="close-btn" @click="closeStockDetailsModal">✕</button>
    <h4 class="Invest-in-heading"> {{ selectedStock.organization }} Stock Details</h4>
    
    <div class="investment-heading">
      <h2 class="text-xl font-semibold mb-2">Welcome to Your Investment Dashboard</h2>
      <p class="small-top">
        Explore a curated selection of investment opportunities tailored to your financial goals. Track stock performance, monitor investor activity, and make informed decisions backed by real-time insights. Whether you're a seasoned investor or just getting started, this platform helps you invest confidently and strategically.
      </p>
    </div>
     
    <div class="stock-banner-container">
    <div class="stock-banner">
    <div class="stock-header">
      <img src="../assets/images/stocks007.png" alt="Google Icon" class="icon-profile" />
      <div class="stock-info">
        <p class="stock-name">{{ selectedStock.product }}</p>
        <p class="organization-name">{{ selectedStock.organization }}</p>
      </div>
    </div>

    <div class="stock-footer">
      <div class="investors">
        <p class="label">Stock Total Fundings</p>
        <p class="value">{{ selectedStock.number_of_investors }}</p>
      </div>
      <div class="growth-badge">+12.5%</div>
    </div>
  </div>

  <div class="stock-banner" style="margin-left: -0.5px; background-color: #ff847c;">
    <div class="stock-header">
      <div class="stock-info">
        <p class="stock-info-heading">Stock Information</p>
        <p class="organization-name">Supplier: {{ selectedStock.supplier }}</p>
        <p class="show-reviews-banner" @click="viewReviews(selectedStock.id)">Show Reviews</p>
      </div>
    </div>

    <div class="stock-footer">
      <div class="investors">
        <p class="label">Org Stocks Available</p>
        <p class="value">{{ selectedStock.quantity }}</p>
      </div>
      <div class="growth-badge">+22.90%</div>
    </div>
  </div>
</div>

    <!-- Buy/Sell Buttons -->
    <div class="button-group">
      <button
        class="buy-btn"
        @click="investInStock(selectedStock.id, selectedStock.amount)"
      >
  <span class="buttons-span">
    <img src="../assets/images/buy.png" alt="Info" class="image-info" />
  </span>
  Invest Stock
</button>

      <button class="sell-btn"><span class="buttons-span"><img src="../assets/images/sell.png" alt="Info" class="image-info" /></span>Trade Stock</button>
      <input
      type="number"
      v-model.number="selectedStock.amount"
      placeholder="Amount to invest"
      class="amount-invest-input"
    />
    </div>
    <hr class="section-divider"/>
    <div class="stocks-news">
    <p class="stock-news-heading">
      <span>
        <img src="../assets/images/feed2.png" alt="Info" class="image-info" />
      </span>
      Stock Insights
    </p>
    <p class="news-info"><span><img src="../assets/images/feed1.png" alt="Info" class="image-info" /></span>{{ currentMessage }}</p>
  </div>
  <div class="stocks-news" style="margin-top: -10px;">
    <p class="stock-news-heading">
      <span>
        <img src="../assets/images/info-icon.png" alt="Info" class="image-info" />
      </span>
      Suppliers
    </p>
    <p class="news-info"><span><img src="../assets/images/info-icon.png" alt="Info" class="image-info" /></span>This stock is being supplied from <strong>{{ selectedStock.supplier }}</strong></p>
  </div>
  <div class="candle-stick-display">
    <section class="candle-stick-display-sec" >
      <CandleStickGraph/>
    </section>
  </div>
    
  </div>
</div>

  </div>
</template>


<script>
import InvestmentsService from '../store/InvestmentDet';
import CandleStickGraph from './CandleStickGraph.vue';

export default {
  name: 'InvestmentDetails',
  components: {
    CandleStickGraph,
  },
  data() {
    return {
      investment: null,
      loading: true,
      error: null,
      showInvestModal: false,
      showStockDetailsModal: false,
      stocks: [],
      selectedStock: null,
      investmentAmount: null,
      stockMessages: [], 
      messageIndex: 0,
      intervalId: null, 
    };
  },
  computed: {
    currentMessage() {
      // Return the current message based on the messageIndex
      return this.stockMessages[this.messageIndex] || '';
    },
  },
  async created() {
    try {
      const data = await InvestmentsService.getMyInvestment();
      this.investment = data;
    } catch (err) {
      console.error('Failed to fetch investment details:', err);
      this.error = err.message || JSON.stringify(err);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    goTo(page) {
      this.$router.push({ name: page });
    },
    openInvestModal() {
      this.showInvestModal = true;
      this.fetchInvestableStocks();
    },
    closeInvestModal() {
      this.showInvestModal = false;
    },
    closeStockDetailsModal() {
      // Stop rotating messages and reset modal state
      clearInterval(this.intervalId);
      this.showStockDetailsModal = false;
      this.selectedStock = null;
      this.investmentAmount = null;
    },
    async fetchInvestableStocks() {
      try {
        const stocks = await InvestmentsService.getInvestableStocks();
        this.stocks = stocks;
      } catch (error) {
        console.error('Failed to fetch investable stocks:', error);
      }
    },
    selectStock(stock) {
      // Set the selected stock and generate messages
      this.selectedStock = stock;
      this.stockMessages = this.generateMessages();
      this.messageIndex = Math.floor(Math.random() * this.stockMessages.length); // Randomize starting message
      this.rotateMessages(); // Start rotating messages
      this.showStockDetailsModal = true;
    },
    viewReviews(stockId) {
      console.log("Go to reviews for stock:", stockId);
      // You could also do: this.$router.push({ name: 'StockReviews', params: { id: stockId } })
    },
    async investInStock(stockId, amount) {
      if (!amount || amount <= 0) {
        alert('Please enter a valid amount.');
        return;
      }

      try {
        await InvestmentsService.investInStock(stockId, amount);
        alert(`Successfully invested $${amount} in stock #${stockId}`);
        this.closeStockDetailsModal();
        this.closeInvestModal();
      } catch (error) {
        console.error('Investment failed:', error);
        alert('Failed to invest in stock.');
      }
    },
    generateMessages() {
      // Generate dynamic messages based on the selected stock
      const s = this.selectedStock;
      if (!s) return [];
      return [
        `${s.organization} has caught investor attention with ${s.number_of_investors} active investors. Managed by ${s.supplier}, currently ${s.quantity} units available.`,
        `Stocks in ${s.organization} are becoming limited, with only ${s.quantity} units left. Already ${s.number_of_investors} investors are in.`,
        `Momentum is growing around ${s.organization}. With ${s.number_of_investors} investors and ${s.quantity} units still open, this could be a smart entry.`,
        `Join ${s.number_of_investors} others investing in ${s.organization}. Powered by ${s.supplier}, limited stock remains.`,
      ];
    },
    rotateMessages() {
      // Rotate messages every 10 seconds
      this.intervalId = setInterval(() => {
        this.messageIndex = (this.messageIndex + 1) % this.stockMessages.length;
      }, 10000); // Change every 10 seconds
    },
  },
  mounted() {
    // Initialize stock messages if a stock is pre-selected
    if (this.selectedStock) {
      this.stockMessages = this.generateMessages();
      this.messageIndex = Math.floor(Math.random() * this.stockMessages.length);
      this.rotateMessages();
    }
  },
  beforeUnmount() {
    // Clear the interval when the component is destroyed
    clearInterval(this.intervalId);
  },
};
</script>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
}
.metrics-grid > div {
  padding: 1rem;
}

.metrics-grid > div:nth-child(-n+2) {
  border-bottom: 1px solid #e2e8f0;
}

.label {
  font-size: 10px;
  text-transform: uppercase;
  color: #4a5568;
  margin-bottom: 17px;
}

.label-below {
  font-size: 10px;
  text-transform: uppercase;
  color: #4a5568;
  margin-bottom: 17px;
  margin-top: -20px;
}

.value {
  font-size: 11px;
  font-weight: 600;
  margin-top: -10px;
  margin-bottom: -5px;
}
.image-info {
  width: 14px;
  height: 14px;
  margin-right: 5px;
  margin-left: 17px;
  margin-bottom: 2px;
}

h4 {
  font-size: 12px;
  color: #444;
  font-weight: 400;
  text-transform: uppercase;
}

.Investment-det-heading {
  font-size: 11px;
  color: #444;
  font-weight: lighter;
  margin-bottom: 20px;
  text-transform: uppercase;
  margin-top: 20px;
}

.buttons-section {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  padding: 7px;
  border-radius: 10px;
  margin-top: -20px;
}
.buttons-section button {
  flex: 1;
  margin: 0 5px;
  padding: 7px;
  font-size: 11px;
  font-weight: lighter;
  border-radius: 5px;
  cursor: pointer;
  width: 70px;
}

.bt-sec-btn {
  background-color: white; 
  color: white;
  transition: background-color 0.3s ease;
}

.bt-sec-btn:hover {
  border: 1px solid white;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(6px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  margin-top: -40px;
}
.modal-content {
  background: white;
  width: 90%;
  max-width: 810px;
  max-height: 80%;
  overflow-y: auto;
  padding: 2rem;
  border-radius: 1rem;
  position: relative;
}
.close-btn {
  position: absolute;
  bottom: 12rem;
  right: 1rem;
  font-size: 11px;
  background: #4444;
  border: none;
  cursor: pointer;
  border-radius: 10px;
}

.Invest-in-heading {
  font-size: 10px;
  color: #444;;
  margin-bottom: 10px;
  text-transform: uppercase;
  margin-top: -10px;
}

.Inv-message {
  font-size: 10px;
  color: #444;
  margin-left: -42px;
  margin-top: 10px;
}

.reviews-links {
  font-size: 10px;
  color: white;
  background-color: #4444;
  border-radius: 10px;
  cursor: pointer;
  padding: 8px;
  text-decoration: none;
}

.stock-profile {
  background-color: #b2d430;
  padding: 20px;
  width: 350px; 
  margin-top: 50px;
  height: 550px; 
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 200px;
  margin-bottom: 45px;
  border: 1px solid #444; /* blue-500 */
}

.button-group {
  display: flex;
  justify-content: flex-start;
  gap: 15px; /* adjust as needed */
  margin-bottom: 1rem;
  margin-left: 55px;
  border-radius: 10px;
  padding: 5px;
}

.buy-btn {
  background-color: black; /* blue-500 */
  color: white;
  border-radius: 10px;
  border-radius: 10px;
  width: 150px;
  font-size: 11px;
  font-weight: lighter;
  font-family: Arial, Helvetica, sans-serif;
  height: 40px;
}

.buy-btn:hover {
  border-color: #4444; /* blue-600 */
}

.sell-btn {
  background: white; /* light transparent white */
  backdrop-filter: blur(10px); /* blur for glass effect */
  -webkit-backdrop-filter: blur(10px); /* Safari support */
  color: #444;
  border-radius: 10px;
  width: 150px;
  font-size: 11px;
  border: 1px solid black; /* subtle border for the frosted look */
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); /* optional shadow */
  font-weight: lighter;
  font-family: Arial, Helvetica, sans-serif;
  height: 40px;
  text-align: center;
  align-items: center;
}


.sell-btn:hover {
  border-color: #4444; /* blue-600 */
}

.banner-row {
  display: flex;
  justify-content: center; /* center the items */
  gap: 16px; /* space between banners */
  margin-bottom: 16px;
}

.banner {
  width: 200px; /* fixed width */
  background-color: white;
  padding: 5px;
  text-align: center;
  border-radius: 12px;
  border: 1px solid #4444;
  height: 70px;
}


.label-banner{
  font-size: 11px;
  color: #444;
  margin-bottom: 4px;
  font-weight: lighter;
  text-align: center;
  margin-left: 40px;
}

.value {
  font-size: 11px;
  font-weight: lighter;
  color: #444;
}

.stock-info-wrapper {
  display: flex;
  justify-content: center; /* center the child horizontally */
  margin-bottom: 16px;
}

.stock-info-banner {
  background-color: white; /* Tailwind blue-50 */
  border: 1px solid #4444;  /* Tailwind blue-200 */
  border-radius: 12px;
  padding: 16px;
  width: 100%;
  max-width: 412px; /* or any size you prefer */
}

.stock-banner {
  width: 45%;
  max-width: 420px;
  background-color: #b2d430;
  border-radius: 16px;
  border: 1px solid #ccc;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  margin-left: 50px;
  margin-top: 30px;
  margin-bottom: 10px;
}

.stock-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-profile {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: fill;
  border: 2px solid #ccc;
}

.stock-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stock-name {
  font-weight: lighter;
  font-size: 11px;
  margin-bottom: 6px;
  text-transform: uppercase;
  color: white;
}

.organization-name {
  font-size: 11px;
  color: white;
  font-weight: lighter;
  margin-right: 35px;
}

.stock-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.investors {
  font-size: 11px;
  color: white;
}

.growth-badge {
  background-color: black;
  color: white;
  font-weight: lighter;
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 10px;
  text-transform: uppercase;
}

.investors {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.investors .label {
  font-size: 7px;
  color: white;
  margin-bottom: 1px;
  margin-left: -3px;
}

.investors .value {
  font-size: 11px;
  font-weight: bold;
  color: white;
}

.buttons-span {
  margin-left: -15px;
}

.section-divider {
  height: 1px;
  background-color: #444; /* or #444, or anything you prefer */
  margin: 16px 0;
  width: 70%;
  margin-left: 60px;
}

.stocks-news {
  background-color: black;
  border-left: 4px solid #b2d430;
  padding: 5px 5px;
  border-radius: 10px;
  margin: 16px 0;
  font-size: 9px;
  color: white;
  height: 45px;
  align-items: start;
  text-align: start;
}

.stock-news-heading {
  display: flex;
  align-items: center;
  margin-bottom: 3px;
  color: white;
  font-size: 10px;
}

.small-top {
  font-size: 9px;
  color: #4444;
}

.investment-heading {
  margin-bottom: -15px;
}

.stock-banner-container {
  display: flex;
  gap: 15px; /* space between the two banners */
  justify-content: start; /* center them horizontally */
  flex-wrap: wrap; /* allows them to stack on smaller screens */
  margin-bottom: 1rem;
}

.stock-banner {
  width: 300px; /* adjust as needed */
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.stock-info-heading {
  font-size: 11px;
  color: #444;
  margin-bottom: 4px;
  font-weight: bold;
  text-transform: uppercase;
}

.show-reviews-banner {
  margin-bottom: -20px;
  margin-top: -12px;
  font-size: 10px;
  color: white;
  background-color: #444;
  border-radius: 10px;
  font-weight: bold;
  padding: 4px;
}

.amount-invest-input {
  width: 27%;
  padding: 19px;
  border-radius: 10px;
  border: 1px solid black;
  margin-top: -10px;
  font-size: 11px;
  font-weight: lighter;
  margin-top: 0.5px;
}

.candle-stick-display {
  border-radius: 10px;
  margin-bottom: 20px;
}

.icon {
  width: 20px;
  height: 20px;
}
</style>
