<template>
    <div class="investment-dashboard">
      <!-- Main widget container -->
      <div class="investor-widget" :class="{ 'is-fullscreen': isFullScreen }">
        
        <!-- Header section -->
        <div class="widget-header">
          <div class="widget-branding">
            <div class="brand-icon">
                <img src="../assets/images/trolley.png" alt="Export" class="inv-icon"/>
            </div>
            <div class="brand-info">
              <h2 class="widget-title">Investment Opportunities</h2>
              <p class="widget-subtitle">High-potential supplier growth insights</p>
            </div>
          </div>
          
          <div class="widget-controls">
            <div class="segment-control">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                :class="['segment-btn', { active: activeTab === tab.id }]"
                @click="activeTab = tab.id"
              >
                <i :class="tab.icon"></i>
                <span>{{ tab.label }}</span>
              </button>
            </div>
            
            <button @click="toggleFullScreen" class="action-btn">
              <i :class="isFullScreen ? 'fas fa-compress-alt' : 'fas fa-expand-alt'"></i>
            </button>
          </div>
        </div>
        
        <!-- Dashboard metrics summary -->
        <div class="metrics-summary">
          <div class="metric-card">
            <div class="metric-icon">
              <i class="fas fa-rocket"></i>
            </div>
            <div class="metric-data">
              <h3 class="metric-value">{{ getHighGrowthCount() }}</h3>
              <p class="metric-label">High Growth</p>
            </div>
            <div class="metric-trend positive">
              <i class="fas fa-arrow-up"></i>
              <span>12%</span>
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-icon">
              <i class="fas fa-handshake"></i>
            </div>
            <div class="metric-data">
              <h3 class="metric-value">{{ getInvestmentOpportunityCount() }}</h3>
              <p class="metric-label">Open Opportunities</p>
            </div>
            <div class="metric-trend positive">
              <i class="fas fa-arrow-up"></i>
              <span>5%</span>
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-icon">
              <i class="fas fa-chart-pie"></i>
            </div>
            <div class="metric-data">
              <h3 class="metric-value">{{ getAverageROI() }}%</h3>
              <p class="metric-label">Avg. ROI</p>
            </div>
            <div class="metric-trend negative">
              <i class="fas fa-arrow-down"></i>
              <span>2%</span>
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-icon">
              <i class="fas fa-dollar-sign"></i>
            </div>
            <div class="metric-data">
              <h3 class="metric-value">{{ formatCurrency(getTotalInvestmentPotential()) }}</h3>
              <p class="metric-label">Investment Potential</p>
            </div>
            <div class="metric-trend positive">
              <i class="fas fa-arrow-up"></i>
              <span>18%</span>
            </div>
          </div>
        </div>
        
        <!-- Filters & Controls -->
        <div class="controls-bar">
          <div class="search-section">
            <div class="search-field">
              <i class="fas fa-search"></i>
              <input
                type="text"
                v-model="filters.search"
                placeholder="Search suppliers, products, markets..."
                class="search-input"
              />
              <button 
                v-if="filters.search" 
                @click="filters.search = ''"
                class="search-clear"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
            
            <div class="filter-chips">
              <div 
                v-for="(chip, index) in activeFilterChips" 
                :key="index"
                class="filter-chip"
              >
                <span>{{ chip.label }}</span>
                <button @click="removeFilterChip(chip)" class="chip-remove">
                  <i class="fas fa-times"></i>
                </button>
              </div>
              
              <button @click="toggleFilterPanel" class="filter-btn" :class="{ 'active': showFilterPanel }">
                <i class="fas fa-filter"></i>
                <span>Filters</span>
                <span v-if="activeFilterCount > 0" class="filter-badge">{{ activeFilterCount }}</span>
              </button>
            </div>
          </div>
          
          <div class="view-controls">
            <div class="sort-control">
              <span class="sort-label">Sort:</span>
              <select v-model="filters.sortBy" class="sort-select">
                <option value="score">Recommendation Score</option>
                <option value="growthRate">Growth Rate</option>
                <option value="recentSales">Recent Sales</option>
                <option value="roi">ROI Potential</option>
              </select>
              <button @click="toggleSortDirection" class="sort-dir-btn">
                <i :class="filters.sortDirection === 'desc' ? 'fas fa-sort-amount-down' : 'fas fa-sort-amount-up'"></i>
              </button>
            </div>
            
            <div class="view-toggle">
              <button 
                :class="['view-btn', { active: viewMode === 'card' }]" 
                @click="viewMode = 'card'"
              >
                <i class="fas fa-th-large"></i>
              </button>
              <button 
                :class="['view-btn', { active: viewMode === 'list' }]" 
                @click="viewMode = 'list'"
              >
                <i class="fas fa-list"></i>
              </button>
              <button 
                :class="['view-btn', { active: viewMode === 'grid' }]" 
                @click="viewMode = 'grid'"
              >
                <i class="fas fa-th"></i>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Filter Panel -->
        <div :class="['filter-panel', { 'open': showFilterPanel }]">
          <div class="panel-header">
            <h3>Advanced Filters</h3>
            <button @click="toggleFilterPanel" class="panel-close">
              <i class="fas fa-times"></i>
            </button>
          </div>
          
          <div class="filter-sections">
            <div class="filter-section">
              <h4>Investment Status</h4>
              <div class="switch-container">
                <label class="switch-label">
                  <span>Open for Investment</span>
                  <div class="toggle-switch">
                    <input type="checkbox" v-model="filters.openForInvestment">
                    <span class="switch-slider"></span>
                  </div>
                </label>
                
                <label class="switch-label">
                  <span>With Existing Investment</span>
                  <div class="toggle-switch">
                    <input type="checkbox" v-model="filters.hasExistingInvestment">
                    <span class="switch-slider"></span>
                  </div>
                </label>
              </div>
            </div>
            
            <div class="filter-section">
              <h4>Growth Rate <span class="selected-value">{{ filters.minGrowthRate || 0 }}%+</span></h4>
              <div class="slider-container">
                <input 
                  type="range" 
                  min="0" 
                  max="50"
                  step="5"
                  v-model="filters.minGrowthRate" 
                  class="range-slider"
                >
                <div class="slider-labels">
                  <span>0%</span>
                  <span>25%</span>
                  <span>50%+</span>
                </div>
              </div>
            </div>
            
            <div class="filter-section">
              <h4>Recommendation Score</h4>
              <div class="radio-group">
                <label v-for="(option, i) in scoreOptions" :key="i" class="radio-option">
                  <input 
                    type="radio" 
                    :value="option.value" 
                    v-model="filters.minScore"
                    name="scoreFilter"
                  >
                  <span class="radio-mark"></span>
                  <span class="radio-label">{{ option.label }}</span>
                </label>
              </div>
            </div>
            
            <div class="filter-section">
              <h4>Recent Sales</h4>
              <div class="radio-group">
                <label v-for="(option, i) in salesOptions" :key="i" class="radio-option">
                  <input 
                    type="radio" 
                    :value="option.value" 
                    v-model="filters.minSales"
                    name="salesFilter"
                  >
                  <span class="radio-mark"></span>
                  <span class="radio-label">{{ option.label }}</span>
                </label>
              </div>
            </div>
            
            <div class="filter-section">
              <h4>Market Sector</h4>
              <div class="checkbox-grid">
                <label v-for="(sector, i) in marketSectors" :key="i" class="checkbox-option">
                  <input 
                    type="checkbox" 
                    v-model="filters.sectors" 
                    :value="sector.value"
                  >
                  <span class="checkbox-mark"></span>
                  <span class="checkbox-label">{{ sector.label }}</span>
                </label>
              </div>
            </div>
          </div>
          
          <div class="panel-footer">
            <button @click="resetFilters" class="btn btn-text">Reset All</button>
            <button @click="applyFilters" class="btn btn-primary">Apply Filters</button>
          </div>
        </div>
        
        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="spinner">
            <i class="fas fa-circle-notch fa-spin"></i>
          </div>
          <div class="loading-text">Loading investment opportunities...</div>
        </div>
        
        <!-- Error State -->
        <div v-else-if="error" class="error-state">
          <div class="error-icon">
            <i class="fas fa-exclamation-triangle"></i>
          </div>
          <div class="error-message">{{ error }}</div>
          <button @click="loadSuppliers" class="btn btn-primary">
            <i class="fas fa-redo"></i>
            Try Again
          </button>
        </div>
        
        <!-- Empty State -->
        <div v-else-if="filteredSuppliers.length === 0" class="empty-state">
          <div class="empty-illustration">
            <i class="fas fa-search"></i>
          </div>
          <div class="empty-title">No Suppliers Found</div>
          <div class="empty-message">
            Try adjusting your filters or search criteria
          </div>
          <button @click="resetFilters" class="btn btn-outline">
            Reset Filters
          </button>
        </div>
        
        <!-- Card View -->
        <div v-else-if="viewMode === 'card'" class="card-view">
          <div class="card-grid">
            <div 
              v-for="supplier in filteredSuppliers" 
              :key="supplier.id"
              class="supplier-card"
              @click="viewSupplierDetails(supplier.id)"
            >
              <div class="card-header">
                <div class="card-badges">
                  <div 
                    v-if="supplier.is_open_for_investment"
                    class="badge investment-badge"
                  >
                    <i class="fas fa-dollar-sign"></i>
                    <span>Open Investment</span>
                  </div>
                  <div 
                    v-if="supplier.growth_rate > 20"
                    class="badge growth-badge"
                  >
                    <i class="fas fa-rocket"></i>
                    <span>High Growth</span>
                  </div>
                </div>
                
                <div class="score-indicator" :class="getScoreClass(supplier.score)">
                  {{ Math.round(supplier.score) }}
                </div>
              </div>
              
              <div class="card-content">
                <h3 class="supplier-name">{{ supplier.name }}</h3>
                
                <div class="sector-tags">
                  <span v-for="(sector, idx) in getSupplierSectors(supplier)" :key="idx" class="sector-tag">
                    {{ sector }}
                  </span>
                </div>
                
                <div class="metrics-grid">
                  <div class="metric-item">
                    <div class="metric-label">
                      <i class="fas fa-chart-line"></i>
                      <span>Recent Sales</span>
                    </div>
                    <div class="metric-value">{{ formatCurrency(supplier.recent_sales) }}</div>
                  </div>
                  
                  <div class="metric-item">
                    <div class="metric-label">
                      <i class="fas fa-percent"></i>
                      <span>Growth Rate</span>
                    </div>
                    <div :class="['metric-value', getGrowthClass(supplier.growth_rate)]">
                      {{ supplier.growth_rate }}%
                    </div>
                  </div>
                  
                  <div class="metric-item">
                    <div class="metric-label">
                      <i class="fas fa-box"></i>
                      <span>Products</span>
                    </div>
                    <div class="metric-value">{{ supplier.products_count }}</div>
                  </div>
                  
                  <div class="metric-item">
                    <div class="metric-label">
                      <i class="fas fa-coins"></i>
                      <span>Current Investment</span>
                    </div>
                    <div class="metric-value">{{ formatCurrency(supplier.total_amount_invested) }}</div>
                  </div>
                </div>
              </div>
              
              <div class="card-chart">
                <div class="chart-header">
                  <span>Performance Trend (6mo)</span>
                  <span :class="['chart-trend', supplier.trend > 0 ? 'positive' : 'negative']">
                    <i :class="supplier.trend > 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
                    {{ Math.abs(supplier.trend) }}%
                  </span>
                </div>
                <div class="mini-chart">
                  <!-- This would be a small chart visualization -->
                  <div class="chart-placeholder" :class="getChartClass(supplier)"></div>
                </div>
              </div>
              
              <div class="card-footer">
                <div class="recommendation-meter">
                  <div class="meter-label">Recommendation Score</div>
                  <div class="meter-bar">
                    <div 
                      :class="['meter-fill', getScoreClass(supplier.score)]"
                      :style="`width: ${Math.min(100, supplier.score)}%`"
                    ></div>
                  </div>
                </div>
                
                <button class="view-details-btn">
                  <i class="fas fa-eye"></i>
                  <span>View Details</span>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Grid View (Compact) -->
        <div v-else-if="viewMode === 'grid'" class="grid-view">
          <div class="compact-grid">
            <div 
              v-for="supplier in filteredSuppliers" 
              :key="supplier.id"
              class="compact-card"
              @click="viewSupplierDetails(supplier.id)"
            >
              <div class="compact-header">
                <div class="compact-badges">
                  <div v-if="supplier.is_open_for_investment" class="micro-badge investment">
                    <i class="fas fa-dollar-sign"></i>
                  </div>
                  <div v-if="supplier.growth_rate > 20" class="micro-badge growth">
                    <i class="fas fa-rocket"></i>
                  </div>
                </div>
                <div class="compact-score" :class="getScoreClass(supplier.score)">
                  {{ Math.round(supplier.score) }}
                </div>
              </div>
              
              <div class="compact-content">
                <h4 class="compact-name">{{ supplier.name }}</h4>
                <div class="compact-metrics">
                  <div class="compact-metric">
                    <i class="fas fa-chart-line"></i>
                    <span>{{ formatCurrency(supplier.recent_sales, true) }}</span>
                  </div>
                  <div class="compact-metric">
                    <i class="fas fa-rocket"></i>
                    <span :class="getGrowthClass(supplier.growth_rate)">{{ supplier.growth_rate }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- List View -->
        <div v-else class="list-view">
          <table class="data-table">
            <thead>
              <tr>
                <th class="col-score">Score</th>
                <th class="col-supplier">Supplier</th>
                <th class="col-sector">Sector</th>
                <th class="col-sales">Sales</th>
                <th class="col-growth">Growth</th>
                <th class="col-products">Products</th>
                <th class="col-investment">Investment</th>
                <th class="col-actions">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="supplier in filteredSuppliers" 
                :key="supplier.id"
                class="data-row"
                @click="viewSupplierDetails(supplier.id)"
              >
                <td>
                  <div class="table-score" :class="getScoreClass(supplier.score)">
                    {{ Math.round(supplier.score) }}
                  </div>
                </td>
                <td>
                  <div class="table-supplier">
                    <div class="supplier-name">{{ supplier.name }}</div>
                    <div class="supplier-badges">
                      <span 
                        v-if="supplier.is_open_for_investment"
                        class="micro-badge investment"
                        title="Open for Investment"
                      >
                        <i class="fas fa-dollar-sign"></i>
                      </span>
                      <span 
                        v-if="supplier.growth_rate > 20"
                        class="micro-badge growth"
                        title="High Growth"
                      >
                        <i class="fas fa-rocket"></i>
                      </span>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="table-sectors">
                    <span class="sector-pill" v-for="(sector, idx) in getSupplierSectors(supplier)" :key="idx">
                      {{ sector }}
                    </span>
                  </div>
                </td>
                <td>{{ formatCurrency(supplier.recent_sales) }}</td>
                <td>
                  <div :class="['growth-indicator', getGrowthClass(supplier.growth_rate)]">
                    <i :class="supplier.growth_rate >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
                    <span>{{ supplier.growth_rate }}%</span>
                  </div>
                </td>
                <td>{{ supplier.products_count }}</td>
                <td>{{ formatCurrency(supplier.total_amount_invested) }}</td>
                <td>
                  <div class="action-buttons">
                    <button 
                      class="table-action view-btn"
                      title="View Details"
                    >
                      <i class="fas fa-eye"></i>
                    </button>
                    <button 
                      class="table-action invest-btn"
                      title="Investment Options"
                      v-if="supplier.is_open_for_investment"
                    >
                      <i class="fas fa-hand-holding-usd"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div class="pagination-controls">
          <div class="page-info">
            Showing <span class="current-range">{{ paginationRange }}</span> of <span class="total-count">{{ suppliers.length }}</span> suppliers
          </div>
          
          <div class="pagination">
            <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">
              <i class="fas fa-chevron-left"></i>
            </button>
            
            <button 
              v-for="pageNum in displayedPages" 
              :key="pageNum"
              :class="['page-num', { 'current': currentPage === pageNum }]"
              @click="goToPage(pageNum)"
            >
              {{ pageNum }}
            </button>
            
            <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
          
          <div class="page-size">
            <select v-model="pageSize" class="page-size-select">
              <option value="10">10 per page</option>
              <option value="20">20 per page</option>
              <option value="50">50 per page</option>
              <option value="100">100 per page</option>
            </select>
          </div>
        </div>
        
      </div>
    </div>
  </template>
  
  <script>
  import { fetchRecommendedSuppliers, filterSuppliers } from '../store/recommendedSupplier';
  
  export default {
    name: 'InvestmentDashboard',
    
    data() {
      return {
        suppliers: [],
        loading: true,
        error: null,
        showFilterPanel: false,
        isFullScreen: false,
        viewMode: 'card',
        activeTab: 'all',
        currentPage: 1,
        pageSize: 20,
        
        tabs: [
          { id: 'all', label: 'All Suppliers', icon: 'fas fa-th-large' },
          { id: 'investment', label: 'Open Investments', icon: 'fas fa-hand-holding-usd' },
          { id: 'highGrowth', label: 'High Growth', icon: 'fas fa-rocket' },
          { id: 'topRated', label: 'Top Rated', icon: 'fas fa-star' }
        ],
        
        scoreOptions: [
          { label: 'Any Score', value: null },
          { label: 'Good (40+)', value: 40 },
          { label: 'Great (70+)', value: 70 },
          { label: 'Excellent (90+)', value: 90 }
        ],
        
        salesOptions: [
          { label: 'Any Amount', value: null },
          { label: '$50K+', value: 50000 },
          { label: '$100K+', value: 100000 },
          { label: '$500K+', value: 500000 }
        ],
        
        marketSectors: [
          { label: 'Technology', value: 'tech' },
          { label: 'Manufacturing', value: 'manufacturing' },
          { label: 'Healthcare', value: 'healthcare' },
          { label: 'Finance', value: 'finance' },
          { label: 'Retail', value: 'retail' },
          { label: 'Energy', value: 'energy' }
        ],
        
        // Filter state
        filters: {
          search: '',
          openForInvestment: false,
          hasExistingInvestment: false,
          minGrowthRate: null,
          minScore: null,
          minSales: null,
          sectors: [],
          sortBy: 'score',
          sortDirection: 'desc'
        },
        
        // Cached copy of filters before opening drawer
        filterBackup: null
      };
    },
    
    computed: {
      filteredSuppliers() {
        let suppliers = [...this.suppliers];
        
        // Add random trend data if it doesn't exist (for demo purposes)
        suppliers = suppliers.map(s => {
          if (!s.trend) {
            s.trend = Math.floor(Math.random() * 41) - 20; // -20 to +20
          }
          return s;
        });
        
        // Apply tab filters first
        if (this.activeTab === 'investment') {
          suppliers = suppliers.filter(s => s.is_open_for_investment);
        } else if (this.activeTab === 'highGrowth') {
          suppliers = suppliers.filter(s => s.growth_rate >= 15);
        } else if (this.activeTab === 'topRated') {
          suppliers = suppliers.filter(s => s.score >= 70);
        }
        
        // Then apply the rest of the filters
        suppliers = filterSuppliers(suppliers, this.filters);
        
        // Apply pagination
        return suppliers;
      },
      
      paginatedSuppliers() {
        const start = (this.currentPage - 1) * this.pageSize;
        const end = start + this.pageSize;
        return this.filteredSuppliers.slice(start, end);
      },
      
      totalPages() {
        return Math.ceil(this.filteredSuppliers.length / this.pageSize);
      },
      
      displayedPages() {
        const pages = [];
        const maxDisplayedPages = 5;
        
        if (this.totalPages <= maxDisplayedPages) {
          // Show all pages if there are fewer than maxDisplayedPages
          for (let i = 1; i <= this.totalPages; i++) {
            pages.push(i);
          }
        } else {
          // Always include first and last page, and some pages around current page
          if (this.currentPage <= 3) {
            // Start of pagination
            for (let i = 1; i <= 4; i++) {
              pages.push(i);
            }
            pages.push(this.totalPages);
          } else if (this.currentPage >= this.totalPages - 2) {
            // End of pagination
            pages.push(1);
            for (let i = this.totalPages - 3; i <= this.totalPages; i++) {
              pages.push(i);
            }
          } else {
            // Middle of pagination
            pages.push(1);
            for (let i = this.currentPage - 1; i <= this.currentPage + 1; i++) {
              pages.push(i);
            }
            pages.push(this.totalPages);
          }
        }
        
        return pages;
      },
      
      paginationRange() {
        const start = (this.currentPage - 1) * this.pageSize + 1;
        const end = Math.min(start + this.pageSize - 1, this.filteredSuppliers.length);
        return `${start}-${end}`;
      },
      
      activeFilterCount() {
        let count = 0;
        if (this.filters.openForInvestment) count++;
        if (this.filters.hasExistingInvestment) count++;
        if (this.filters.minGrowthRate) count++;
        if (this.filters.minScore) count++;
        if (this.filters.minSales) count++;
        if (this.filters.sectors.length > 0) count++;
        return count;
      },
      
      activeFilterChips() {
        const chips = [];
        
        if (this.filters.openForInvestment) {
          chips.push({ 
            label: 'Open for Investment', 
            type: 'openForInvestment'
          });
        }
        
        if (this.filters.hasExistingInvestment) {
          chips.push({ 
            label: 'With Existing Investment', 
            type: 'hasExistingInvestment'
          });
        }
        
        if (this.filters.minGrowthRate) {
          chips.push({ 
            label: `Growth Rate: ≥${this.filters.minGrowthRate}%`, 
            type: 'minGrowthRate'
          });
        }
        
        if (this.filters.minScore) {
          const option = this.scoreOptions.find(o => o.value === this.filters.minScore);
          chips.push({ 
            label: `Score: ${option.label}`, 
            type: 'minScore'
          });
        }
        
        if (this.filters.minSales) {
          const option = this.salesOptions.find(o => o.value === this.filters.minSales);
          chips.push({ 
            label: `Sales: ${option.label}`, 
            type: 'minSales'
          });
        }
        
        if (this.filters.sectors.length > 0) {
          chips.push({
            label: `Sectors: ${this.filters.sectors.length} selected`,
            type: 'sectors'
          });
        }
        
        return chips;
      }
    },
    
    created() {
      this.loadSuppliers();
    },
    
    methods: {
      // The previous code in methods: starts with the loadSuppliers() method
// Let's continue with the remaining methods:

async loadSuppliers() {
        this.loading = true;
        this.error = null;
        
        try {
          this.suppliers = await fetchRecommendedSuppliers();
          // Add mock sector data for demo
          this.suppliers = this.suppliers.map(s => {
            const sectorCount = Math.floor(Math.random() * 3) + 1;
            const sectors = [];
            const allSectors = this.marketSectors.map(s => s.value);
            
            for (let i = 0; i < sectorCount; i++) {
              const randomIndex = Math.floor(Math.random() * allSectors.length);
              const sector = allSectors[randomIndex];
              if (!sectors.includes(sector)) {
                sectors.push(sector);
              }
            }
            
            return {
              ...s,
              sectors
            };
          });
        } catch (err) {
          console.error('Error loading suppliers:', err);
          this.error = 'Failed to load investment opportunities. Please try again.';
        } finally {
          this.loading = false;
        }
      },
      
      toggleFilterPanel() {
        if (!this.showFilterPanel) {
          // Store backup of filters when opening
          this.filterBackup = JSON.parse(JSON.stringify(this.filters));
        }
        this.showFilterPanel = !this.showFilterPanel;
      },
      
      toggleFullScreen() {
        this.isFullScreen = !this.isFullScreen;
      },
      
      resetFilters() {
        this.filters = {
          search: '',
          openForInvestment: false,
          hasExistingInvestment: false,
          minGrowthRate: null,
          minScore: null,
          minSales: null,
          sectors: [],
          sortBy: 'score',
          sortDirection: 'desc'
        };
        this.currentPage = 1;
      },
      
      applyFilters() {
        // Just close the filter panel, since filters are applied reactively
        this.showFilterPanel = false;
        this.currentPage = 1; // Reset to first page when filters change
      },
      
      toggleSortDirection() {
        this.filters.sortDirection = this.filters.sortDirection === 'asc' ? 'desc' : 'asc';
      },
      
      removeFilterChip(chip) {
        if (chip.type === 'sectors') {
          this.filters.sectors = [];
        } else {
          this.filters[chip.type] = chip.type === 'minGrowthRate' ? null : false;
        }
      },
      
      viewSupplierDetails(supplierId) {
        // Navigate to supplier details page or open modal
        console.log('View supplier details:', supplierId);
        this.$emit('view-supplier', supplierId);
      },
      
      goToPage(pageNum) {
        this.currentPage = pageNum;
      },
      
      formatCurrency(value, short = false) {
        if (value === null || value === undefined) return '$0';
        
        if (short) {
          if (value >= 1000000) {
            return `$${(value / 1000000).toFixed(1)}M`;
          } else if (value >= 1000) {
            return `$${(value / 1000).toFixed(1)}K`;
          } else {
            return `$${value}`;
          }
        }
        
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          maximumFractionDigits: 0
        }).format(value);
      },
      
      getSupplierSectors(supplier) {
        if (!supplier.sectors || supplier.sectors.length === 0) {
          return ['Uncategorized'];
        }
        
        return supplier.sectors.map(sectorCode => {
          const sector = this.marketSectors.find(s => s.value === sectorCode);
          return sector ? sector.label : sectorCode;
        });
      },
      
      getScoreClass(score) {
        if (score >= 90) return 'excellent';
        if (score >= 70) return 'great';
        if (score >= 40) return 'good';
        return 'average';
      },
      
      getGrowthClass(growth) {
        if (growth >= 20) return 'growth-excellent';
        if (growth >= 10) return 'growth-good';
        if (growth >= 0) return 'growth-average';
        return 'growth-negative';
      },
      
      getChartClass(supplier) {
        if (supplier.trend > 10) return 'trend-up-strong';
        if (supplier.trend > 0) return 'trend-up';
        if (supplier.trend > -10) return 'trend-down';
        return 'trend-down-strong';
      },
      
      getHighGrowthCount() {
        return this.suppliers.filter(s => s.growth_rate >= 15).length;
      },
      
      getInvestmentOpportunityCount() {
        return this.suppliers.filter(s => s.is_open_for_investment).length;
      },
      
      getAverageROI() {
        if (this.suppliers.length === 0) return 0;
        
        const totalROI = this.suppliers.reduce((sum, supplier) => {
          return sum + (supplier.roi || 0);
        }, 0);
        
        return Math.round(totalROI / this.suppliers.length);
      },
      
      getTotalInvestmentPotential() {
        return this.suppliers.reduce((sum, supplier) => {
          if (supplier.is_open_for_investment) {
            return sum + (supplier.investment_potential || 0);
          }
          return sum;
        }, 0);
      }
    }
  };
  </script>
  
  <style>
  .investment-dashboard {
    font-family: 'Inter', 'Segoe UI', Roboto, Arial, sans-serif;
    color: #333;
    background-color: #f9fafb;
    min-height: 100vh;
    padding: 2rem;
  }
  
  /* Widget Container */
  .investor-widget {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    min-height: calc(100vh - 4rem);
    position: relative;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
  }
  
  .is-fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 1000;
    border-radius: 0;
    padding: 1rem;
  }
  
  /* Header Section */
  .widget-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    border-bottom: 1px solid #eff2f5;
  }
  
  .widget-branding {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .brand-icon {
    background: white;
    color: white;
    height: 20px;
    width: 20px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    border: 1px solid #7C3AED;
    padding: 20px;
  }
  
  .widget-title {
    font-size: 12px;
    font-weight: 600;
    margin: 0;
    color: #1e293b;
  }
  
  .widget-subtitle {
    color: #64748b;
    font-size: 10px;
    margin: 2px 0 0;
  }
  
  .widget-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .segment-control {
    display: flex;
    background-color: transparent;
    border-radius: 8px;
    overflow: hidden;
  }
  
  .segment-btn {
    padding: 0.75rem 1.25rem;
    border-radius: 10px;
    border: 1px solid #4444;
    background: white;
    color:#7C3AED;
    font-size: 11px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-right: 5px;
  }
  
  .segment-btn.active {
    background-color: #fff;
    color: #7C3AED;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    border: 1px solid #7C3AED;
    border-radius: 10px;
    font-size: 11px;
  }
  
  .segment-btn i {
    font-size: 14px;
  }
  
  .action-btn {
    border: none;
    background-color: #f3f4f6;
    color: #64748b;
    border-radius: 8px;
    height: 38px;
    width: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .action-btn:hover {
    background-color: #e5e7eb;
    color: #4f46e5;
  }
  
  /* Metrics Summary */
  .metrics-summary {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    padding: 1.5rem 2rem;
    background-color: #f8fafc;
    border-bottom: 1px solid #eff2f5;
  }
  
  .metric-card {
    background-color: #fff;
    border-radius: 10px;
    padding: 1.25rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    display: flex;
    align-items: center;
    gap: 1rem;
    position: relative;
  }
  
  .metric-icon {
    background: linear-gradient(135deg, #f0f9ff, #dbeafe);
    color: #2563eb;
    height: 40px;
    width: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .metric-card:nth-child(2) .metric-icon {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    color: #3b82f6;
  }
  
  .metric-card:nth-child(3) .metric-icon {
    background: linear-gradient(135deg, #ecfdf5, #d1fae5);
    color: #059669;
  }
  
  .metric-card:nth-child(4) .metric-icon {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
    color: #7c3aed;
  }
  
  .metric-data {
    flex: 1;
  }
  
  .metric-value {
    font-size: 20px;
    font-weight: 600;
    color: #1e293b;
    margin: 0;
  }
  
  .metric-label {
    color: #64748b;
    font-size: 13px;
    margin: 4px 0 0;
  }
  
  .metric-trend {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    font-size: 12px;
    font-weight: 500;
    padding: 4px 8px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  
  .metric-trend.positive {
    background-color: #ecfdf5;
    color: #059669;
  }
  
  .metric-trend.negative {
    background-color: #fef2f2;
    color: #dc2626;
  }
  
  /* Controls Bar */
  .controls-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #fff;
    border-bottom: 1px solid #eff2f5;
  }
  
  .search-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 60%;
  }
  
  .search-field {
    display: flex;
    align-items: center;
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 0 0.75rem;
    width: 100%;
  }
  
  .search-field i {
    color: #9ca3af;
    margin-right: 0.75rem;
  }
  
  .search-input {
    border: none;
    background-color: transparent;
    padding: 0.75rem 0;
    width: 100%;
    font-size: 14px;
  }
  
  .search-input:focus {
    outline: none;
  }
  
  .search-clear {
    background: none;
    border: none;
    color: #9ca3af;
    cursor: pointer;
    padding: 0;
  }
  
  .filter-chips {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  
  .filter-chip {
    background-color: #f3f4f6;
    border-radius: 20px;
    padding: 0.35rem 0.75rem;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #4b5563;
  }
  
  .chip-remove {
    border: none;
    background: none;
    padding: 0;
    color: #9ca3af;
    cursor: pointer;
    display: flex;
    align-items: center;
  }
  
  .filter-btn {
    background-color: #f3f4f6;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 0.35rem 0.75rem;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #4b5563;
    cursor: pointer;
    position: relative;
  }
  
  .filter-btn.active {
    background-color: #eff6ff;
    border-color: #93c5fd;
    color: #2563eb;
  }
  
  .filter-badge {
    background-color: #4f46e5;
    color: white;
    border-radius: 10px;
    padding: 0 6px;
    font-size: 10px;
    min-width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .view-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .sort-control {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .sort-label {
    color: #64748b;
    font-size: 13px;
  }
  
  .sort-select {
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    font-size: 13px;
    color: #4b5563;
    cursor: pointer;
  }
  
  .sort-dir-btn {
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 0.5rem;
    color: #4b5563;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .view-toggle {
    display: flex;
    background-color: #f3f4f6;
    border-radius: 6px;
    overflow: hidden;
  }
  
  .view-btn {
    border: none;
    background: transparent;
    padding: 0.5rem 0.75rem;
    color: #64748b;
    cursor: pointer;
  }
  
  .view-btn.active {
    background-color: #fff;
    color: #4f46e5;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  }
  
  /* Filter Panel */
  .filter-panel {
    position: absolute;
    top: 0;
    right: -400px;
    width: 380px;
    height: 100%;
    background-color: #fff;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.05);
    z-index: 1000;
    display: flex;
    flex-direction: column;
    transition: right 0.3s ease;
    overflow-y: auto;
  }
  
  .filter-panel.open {
    right: 0;
  }
  
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #eff2f5;
  }
  
  .panel-header h3 {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
    color: #1e293b;
  }
  
  .panel-close {
    background: none;
    border: none;
    color: #64748b;
    cursor: pointer;
    font-size: 16px;
    padding: 0;
  }
  
  .filter-sections {
    flex: 1;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .filter-section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .filter-section h4 {
    font-size: 15px;
    font-weight: 600;
    margin: 0;
    color: #334155;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .selected-value {
    font-size: 13px;
    color: #4f46e5;
    font-weight: 500;
  }
  
  .switch-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .switch-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
  }
  
  .toggle-switch {
    position: relative;
    width: 40px;
    height: 22px;
  }
  
  .toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }
  
  .switch-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #e5e7eb;
    border-radius: 34px;
    transition: .3s;
  }
  
  .switch-slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 2px;
    bottom: 2px;
    background-color: white;
    border-radius: 50%;
    transition: .3s;
  }
  
  input:checked + .switch-slider {
    background-color: #4f46e5;
  }
  
  input:checked + .switch-slider:before {
    transform: translateX(18px);
  }
  
  .slider-container {
    padding: 0.5rem 0;
  }
  
  .range-slider {
    width: 100%;
    height: 4px;
    border-radius: 10px;
    background: #e5e7eb;
    outline: none;
    -webkit-appearance: none;
  }
  
  .range-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #4f46e5;
    cursor: pointer;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .slider-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 0.5rem;
    color: #64748b;
    font-size: 12px;
  }
  
  .radio-group {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .radio-option, .checkbox-option {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    cursor: pointer;
    font-size: 14px;
    color: #4b5563;
  }
  
  .radio-option input, .checkbox-option input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
  }
  
  .radio-mark {
    height: 18px;
    width: 18px;
    border-radius: 50%;
    border: 2px solid #d1d5db;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }
  
  .radio-option input:checked ~ .radio-mark {
    border-color: #4f46e5;
  }
  
  .radio-option input:checked ~ .radio-mark:after {
    content: "";
    position: absolute;
    height: 10px;
    width: 10px;
    border-radius: 50%;
    background-color: #4f46e5;
  }
  
  .checkbox-mark {
    height: 18px;
    width: 18px;
    border-radius: 4px;
    border: 2px solid #d1d5db;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }
  
  .checkbox-option input:checked ~ .checkbox-mark {
    background-color: #4f46e5;
    border-color: #4f46e5;
  }
  
  .checkbox-option input:checked ~ .checkbox-mark:after {
    content: "✓";
    position: absolute;
    color: white;
    font-size: 12px;
  }
  
  .checkbox-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
  
  .panel-footer {
    padding: 1.5rem;
    border-top: 1px solid #eff2f5;
    display: flex;
    justify-content: space-between;
  }
  
  .btn {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .btn-text {
    background: none;
    border: none;
    color: #64748b;
  }
  
  .btn-primary {
    background-color: #4f46e5;
    color: white;
    border: none;
  }
  
  .btn-outline {
    background-color: white;
    border: 1px solid #e5e7eb;
    color: #4b5563;
  }
  
  /* Card View */
  .card-view {
    flex: 1;
    padding: 1.5rem 2rem;
    overflow-y: auto;
  }
  
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }
  
  .supplier-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    transition: all 0.2s;
    cursor: pointer;
    border: 1px solid #f1f5f9;
  }
  
  .supplier-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
    border-color: #cbd5e1;
  }
  
  .card-header {
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid #f1f5f9;
  }
  
  .card-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .badge {
    font-size: 11px;
    padding: 0.35rem 0.5rem;
    border-radius: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
    font-weight: 500;
  }
  
  .investment-badge {
    background-color: #f0f9ff;
    color: #0369a1;
  }
  
  .growth-badge {
    background-color: #ecfdf5;
    color: #059669;
  }
  
  .score-indicator {
    height: 36px;
    width: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 14px;
  }
  
  .excellent {
    background-color: #10b981;
    color: white;
  }
  
  .great {
    background-color: #3b82f6;
    color: white;
  }
  
  .good {
    background-color: #f59e0b;
    color: white;
  }
  
  .average {
    background-color: #6b7280;
    color: white;
  }
  
  .card-content {
    padding: 1rem;
  }
  
  .supplier-name {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 0.5rem;
    color: #1e293b;
  }
  
  .sector-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  
  .sector-tag {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 0.25rem 0.5rem;
    font-size: 11px;
    color: #64748b;
  }
  
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .metric-item {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }
  
  .metric-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #64748b;
    font-size: 12px;
  }
  
  .metric-value {
    font-weight: 600;
    color: #334155;
    font-size: 14px;
  }
  
  .growth-excellent {
    color: #059669;
  }
  
  .growth-good {
    color: #0369a1;
  }
  
  .growth-average {
    color: #334155;
  }
  
  .growth-negative {
    color: #dc2626;
  }
  
  .card-chart {
    padding: 1rem;
    background-color: #f8fafc;
    border-top: 1px solid #f1f5f9;
  }
  
  .chart-header {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    margin-bottom: 0.5rem;
    color: #64748b;
  }
  
  .chart-trend {
    display: flex;
    align-items: center;
    gap: 4px;
    font-weight: 500;
  }
  
  .chart-trend.positive {
    color: #059669;
  }
  
  .chart-trend.negative {
    color: #dc2626;
  }
  
  .mini-chart {
    height: 40px;
    width: 100%;
  }
  
  .chart-placeholder {
    height: 100%;
    width: 100%;
    border-radius: 4px;
    position: relative;
    overflow: hidden;
  }
  
  .chart-placeholder::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.05) 20%, rgba(0,0,0,0.1) 40%, rgba(0,0,0,0.05) 60%, rgba(0,0,0,0.1) 80%, rgba(0,0,0,0.05))
  }

  .inv-icon {
    width: 20px;
    height: 20px;
  }
  </style>