<template>
    <div class="investments-dashboard">
      <!-- Dashboard Header -->
      <div class="dashboard-header">
        <h2>Investments Statistics</h2>
        <div class="dashboard-actions" v-if="!loading && investments.length > 0">
            <button class="btn-export">
            <img src="../assets/images/upload48.png" alt="Export" class="icon-export" />
            Export
            </button>
        </div>
      </div>
  
      <!-- Summary Cards -->
      <div class="summary-cards" v-if="!loading && investments.length > 0">
        <div class="summary-card">
          <div class="summary-icon-a">
            <img src="../assets/images/stocks-icon.png" alt="Export" class="icon-export" />
          </div>
          <div class="summary-content">
            <p class="summary-label">Total Invested</p>
            <p class="summary-value">${{ formatNumber(getTotalInvested()) }}</p>
          </div>
        </div>
        
        <div class="summary-card">
          <div class="summary-icon-b">
            <img src="../assets/images/wallet-white.png" alt="Export" class="icon-export" />
          </div>
          <div class="summary-content">
            <p class="summary-label">Total Returns</p>
            <p class="summary-value">${{ formatNumber(getTotalReturns()) }}</p>
          </div>
        </div>
        
        <div class="summary-card">
          <div class="summary-icon-b" :class="{'profit-positive': getTotalProfit() >= 0, 'profit-negative': getTotalProfit() < 0}">
            <img src="../assets/images/graph-profit.png" alt="Export" class="icon-export" />
          </div>
          <div class="summary-content">
            <p class="summary-label">Total Profit</p>
            <p class="summary-value" :class="{'profit-positive': getTotalProfit() >= 0, 'profit-negative': getTotalProfit() < 0}">
              ${{ formatNumber(getTotalProfit()) }}
              <span class="percentage">({{ calculateTotalProfitPercentage() }}%)</span>
            </p>
          </div>
        </div>
      </div>
  
      <!-- Filters Section -->
      <div class="filters-section" v-if="!loading && investments.length > 0">
        <div class="search-container">
          <img src="../assets/images/search.png" alt="Export" class="icon-search" />
          <input 
            type="text" 
            v-model="filters.search" 
            placeholder="Search by supplier name..." 
            class="search-input"
          />
        </div>
        
        <div class="filters-container">
          <div class="filter-group">
            <label>Sort By</label>
            <select v-model="filters.sortBy" class="filter-select">
              <option value="supplier_name">Supplier Name</option>
              <option value="amount">Amount</option>
              <option value="date_invested">Date</option>
              <option value="profit_amount">Profit</option>
              <option value="total_return">Total Return</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>Order</label>
            <select v-model="filters.sortOrder" class="filter-select">
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>Performance</label>
            <select v-model="filters.performance" class="filter-select">
              <option value="all">All</option>
              <option value="profit">Profitable</option>
              <option value="loss">Loss</option>
            </select>
          </div>
          
          <button class="btn-filter" @click="resetFilters">
            <img src="../assets/images/reset.png" alt="Export" class="icon-reset" /> Reset
          </button>
        </div>
      </div>
  
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading your investments...</p>
      </div>
  
      <!-- Empty State -->
      <div v-else-if="investments.length === 0" class="empty-state">
        <div class="empty-icon">
          <i class="icon-empty"></i>
        </div>
        <p>You have no investments yet.</p>
        <button class="btn-primary">Add Your First Investment</button>
      </div>
  
      <!-- Data Table -->
      <div v-else class="table-container">
        <table class="investments-table">
          <thead>
            <tr>
              <th @click="sortBy('supplier_name')" class="sortable">
                Supplier
                <i class="sort-icon" :class="getSortIconClass('supplier_name')"></i>
              </th>
              <th @click="sortBy('amount')" class="sortable">
                Invested Amount
                <i class="sort-icon" :class="getSortIconClass('amount')"></i>
              </th>
              <th @click="sortBy('total_return')" class="sortable">
                Total Return
                <i class="sort-icon" :class="getSortIconClass('total_return')"></i>
              </th>
              <th @click="sortBy('profit_amount')" class="sortable">
                Profit
                <i class="sort-icon" :class="getSortIconClass('profit_amount')"></i>
              </th>
              <th @click="sortBy('percentage_profit')" class="sortable">
                % Profit
                <i class="sort-icon" :class="getSortIconClass('percentage_profit')"></i>
              </th>
              <th @click="sortBy('date_invested')" class="sortable">
                Date Invested
                <i class="sort-icon" :class="getSortIconClass('date_invested')"></i>
              </th>
              <th>Linked Stock</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="investment in filteredInvestments" :key="investment.id">
              <td>{{ investment.supplier_name }}</td>
              <td>${{ formatNumber(investment.amount) }}</td>
              <td>${{ formatNumber(investment.total_return) }}</td>
              <td :class="{'profit-positive': investment.profit_amount >= 0, 'profit-negative': investment.profit_amount < 0}">
                ${{ formatNumber(investment.profit_amount) }}
              </td>
              <td :class="{'profit-positive': investment.percentage_profit >= 0, 'profit-negative': investment.percentage_profit < 0}">
                {{ investment.percentage_profit }}%
              </td>
              <td>{{ formatDate(investment.date_invested) }}</td>
              <td>
                <div class="stocks-container">
                  <div v-for="stockInvestment in investment.stock_investments" :key="stockInvestment.id" class="stock-chip">
                    <span class="stock-span" v-if="stockInvestment.stock?.product?.name">
                      {{ stockInvestment.stock.product.name }} ({{ stockInvestment.stock.quantity }})
                    </span>
                    <span v-else>Stock data missing</span>
                  </div>
                </div>
              </td>
              <td>
                <div class="action-buttons">
                  <button class="btn-icon" title="View Details">
                    <img src="../assets/images/preview.png" alt="Export" class="icon-eye" />
                  </button>
                  <button class="btn-icon" title="Edit">
                    <img src="../assets/images/edit.png" alt="Export" class="icon-edit" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div class="pagination" v-if="investments.length > 0">
          <button class="btn-page" :disabled="currentPage === 1" @click="currentPage--">
            <img src="../assets/images/right-icon.png" alt="Export" class="icon-left" />
          </button>
          <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
          <button class="btn-page" :disabled="currentPage === totalPages" @click="currentPage++">
            <img src="../assets/images/left-icon.png" alt="Export" class="icon-right" />
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex';
  import InvestmentsService from '../store/InvestmentDet';
  
  export default {
    data() {
      return {
        investments: [],
        loading: true,
        currentPage: 1,
        itemsPerPage: 10,
        filters: {
          search: '',
          sortBy: 'date_invested',
          sortOrder: 'desc',
          performance: 'all'
        }
      };
    },
  
    created() {
      this.fetchMyInvestments();
    },
  
    computed: {
      filteredInvestments() {
        // First filter by search and performance
        let filtered = this.investments.filter(inv => {
          const matchesSearch = inv.supplier_name.toLowerCase().includes(this.filters.search.toLowerCase());
          const matchesPerformance = 
            this.filters.performance === 'all' ||
            (this.filters.performance === 'profit' && inv.profit_amount >= 0) ||
            (this.filters.performance === 'loss' && inv.profit_amount < 0);
          
          return matchesSearch && matchesPerformance;
        });
  
        // Then sort
        filtered = filtered.sort((a, b) => {
          let aValue = a[this.filters.sortBy];
          let bValue = b[this.filters.sortBy];
          
          // Handle dates specially
          if (this.filters.sortBy === 'date_invested') {
            aValue = new Date(aValue);
            bValue = new Date(bValue);
          }
          
          // Handle numeric values
          if (typeof aValue === 'string' && !isNaN(aValue)) {
            aValue = parseFloat(aValue);
            bValue = parseFloat(bValue);
          }
          
          if (this.filters.sortOrder === 'asc') {
            return aValue > bValue ? 1 : -1;
          } else {
            return aValue < bValue ? 1 : -1;
          }
        });
        
        // Apply pagination
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        return filtered.slice(startIndex, startIndex + this.itemsPerPage);
      },
      
      totalPages() {
        return Math.ceil(this.investments.length / this.itemsPerPage);
      }
    },
  
    methods: {
      ...mapActions({
        setInvestments: 'setInvestments',
      }),
  
      async fetchMyInvestments() {
        try {
          const response = await InvestmentsService.getAllMyInvestments();
          console.log("Raw response: ", response);
          console.log("Data response: ", response.data);
          this.investments = response.data || [];
          console.log("Found Investments: ", this.investments);
        } catch (error) {
          console.error("Failed to fetch investments:", error);
          this.investments = [];
        } finally {
          this.loading = false;
        }
      },
      
      sortBy(column) {
        if (this.filters.sortBy === column) {
          // Toggle sort order if clicking the same column
          this.filters.sortOrder = this.filters.sortOrder === 'asc' ? 'desc' : 'asc';
        } else {
          this.filters.sortBy = column;
          this.filters.sortOrder = 'asc';
        }
      },
      
      getSortIconClass(column) {
        if (this.filters.sortBy !== column) return 'icon-sort';
        return this.filters.sortOrder === 'asc' ? 'icon-sort-up' : 'icon-sort-down';
      },
      
      resetFilters() {
        this.filters = {
          search: '',
          sortBy: 'date_invested',
          sortOrder: 'desc',
          performance: 'all'
        };
        this.currentPage = 1;
      },
      
      formatNumber(value) {
        if (typeof value === 'string') {
          value = parseFloat(value);
        }
        return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
      },
      
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        });
      },
      
      getTotalInvested() {
        return this.investments.reduce((sum, inv) => {
          return sum + parseFloat(inv.amount);
        }, 0);
      },
      
      getTotalReturns() {
        return this.investments.reduce((sum, inv) => {
          return sum + parseFloat(inv.total_return);
        }, 0);
      },
      
      getTotalProfit() {
        return this.investments.reduce((sum, inv) => {
          return sum + parseFloat(inv.profit_amount);
        }, 0);
      },
      
      calculateTotalProfitPercentage() {
        const totalInvested = this.getTotalInvested();
        const totalProfit = this.getTotalProfit();
        
        if (totalInvested === 0) return 0;
        
        return ((totalProfit / totalInvested) * 100).toFixed(2);
      }
    },
  };
  </script>
  
  <style scoped>
  /* Dashboard Layout */
  .investments-dashboard {
    padding: 24px;
    background-color: #f9fafc;
    border-radius: 12px;
    font-family: 'Inter', 'Helvetica', sans-serif;
    color: #1a202c;
    width: 1040px;
    padding-left: 50px;
  }
  
  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }
  
  .dashboard-header h2 {
    font-size: 24px;
    font-weight: 600;
    margin: 0;
    color: #1a202c;
  }
  
  .dashboard-actions {
    display: flex;
    gap: 12px;
  }
  
  /* Summary Cards */
  .summary-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 24px;
  }
  
  .summary-card {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    display: flex;
    align-items: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .summary-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .summary-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background-color: #ebf5ff;
    color: #3182ce;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 16px;
    font-size: 20px;
  }

  .summary-icon-b {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background-color: #b2d430;
    color: #3182ce;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 16px;
    font-size: 20px;
  }

  .summary-icon-a {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background-color: #d59bf6;
    color: #3182ce;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 16px;
    font-size: 20px;
  }
  
  .summary-content {
    flex: 1;
  }
  
  .summary-label {
    font-size: 11px;
    color: #718096;
    margin: 0 0 4px 0;
  }
  
  .summary-value {
    font-size: 11px;
    font-weight: 600;
    margin: 0;
  }
  
  .percentage {
    font-size: 11px;
    margin-left: 4px;
  }
  
  /* Filters */
  .filters-section {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 24px;
    background-color: white;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .search-container {
    position: relative;
    flex: 1;
    min-width: 200px;
  }
  
  .icon-search {
    position: absolute;
    left: 12px;
    top: 70%;
    transform: translateY(-50%);
    color: #a0aec0;
  }
  
  .search-input {
    width: 100%;
    padding: 10px 12px 10px 36px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 11px;
    transition: border-color 0.2s;
    margin-top: 25px;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #3182ce;
    box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1);
  }
  
  .filters-container {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: flex-end;
  }
  
  .filter-group {
    display: flex;
    flex-direction: column;
  }
  
  .filter-group label {
    font-size: 10px;
    color: #718096;
    margin-bottom: 4px;
  }
  
  .filter-select {
    padding: 8px 12px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    background-color: white;
    font-size: 11px;
    min-width: 120px;
  }
  
  .filter-select:focus {
    outline: none;
    border-color: #3182ce;
    box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1);
  }
  
  /* Table Styles */
  .table-container {
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .investments-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
  }
  
  .investments-table th {
    background-color: #328bc6;
    padding: 16px;
    text-align: left;
    font-weight: lighter;
    color: white;
    border-bottom: 1px solid #e2e8f0;
    position: relative;
    font-size: 11px;
  }
  
  .investments-table th.sortable {
    cursor: pointer;
    padding-right: 24px;
  }
  
  .sort-icon {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    color: #a0aec0;
    font-size: 12px;
  }
  
  .investments-table td {
    padding: 16px;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: middle;
    font-size: 10px;
    padding-bottom: 6px;
    padding-top: 8px;
  }
  
  .investments-table tr:last-child td {
    border-bottom: none;
  }
  
  .investments-table tr:hover {
    background-color: #f7fafc;
  }
  
  /* Stocks display */
  .stocks-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .stock-chip {
    background-color: #d59bf6;
    padding: 4px 8px;
    border-radius: 10px;
    font-size: 10px;
    color: white;
  }

  .stock-span {
    font-size: 8px;
  }
  
  /* Action buttons */
  .action-buttons {
    display: flex;
    gap: 8px;
  }
  
  .btn-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    border: none;
    background-color: white;
    color: #4a5568;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
    border: 1px solid #444;
  }
  
  .btn-icon:hover {
    background-color: #edf2f7;
    color: #3182ce;
  }
  
  /* Loading state */
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 64px;
    color: #4a5568;
  }
  
  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e2e8f0;
    border-top: 4px solid #3182ce;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* Empty state */
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 64px;
    text-align: center;
    color: #718096;
  }
  
  .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
    color: #cbd5e0;
  }
  
  /* Buttons */
  .btn-primary {
    background-color: #3182ce;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .btn-primary:hover {
    background-color: #2c5282;
  }
  
  .btn-export, .btn-filter {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    font-size: 11px;
    transition: all 0.2s;
  }
  
  .btn-export {
    background-color: white;
    border: 1px solid #e2e8f0;
    color: #4a5568;
  }
  
  .btn-export:hover {
    background-color: #f7fafc;
    border-color: #cbd5e0;
  }
  
  .btn-filter {
    background-color: #d59bf6;
    border: none;
    color: white;
  }
  
  .btn-filter:hover {
    background-color: black;
  }
  
  /* Pagination */
  .pagination {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    border-top: 1px solid #e2e8f0;
  }
  
  .btn-page {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    background-color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
  }

  .icon-export {
    width: 20px;
    height: 20px;
  }
  
  .btn-page:hover:not(:disabled) {
    background-color: #f7fafc;
    border-color: #cbd5e0;
  }
  
  .btn-page:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .page-info {
    margin: 0 16px;
    font-size: 10px;
    color: #4a5568;
  }
  
  .profit-positive {
    color: #c1f880;
  }
  
  .profit-negative {
    color: #ff5959;
  }
  
  /* Icons */
  /* Note: You'll need to replace these with actual icons from your icon library */
  .icon-dollar, .icon-chart, .icon-trending, .icon-search, 
  .icon-reset, .icon-sort, .icon-sort-up, .icon-sort-down,
  .icon-eye, .icon-edit, .icon-left, .icon-right, .icon-download, .icon-empty {
    /* Using a placeholder for icons */
    display: inline-block;
    width: 1em;
    height: 1em;
  }
  
  /* Responsiveness */
  @media (max-width: 768px) {
    .summary-cards {
      grid-template-columns: 1fr;
    }
    
    .filters-section {
      flex-direction: column;
    }
    
    .table-container {
      overflow-x: auto;
    }
    
    .investments-table {
      min-width: 800px;
    }
    
  }
  </style>