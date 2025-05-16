<template>
  <BaseLayout>
    <div class="sales-entrie-container">
      <h4 class="history-heading">Stockify <span class="history-heading-span">Inventory</span></h4>

      <div class="header-entry-icons-inventory">
        <div class="search-container">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search inventory..."
            class="search-input"
            @input="filterInventory"
          />
        </div>
        <button class="entry-icon-button" @click="toggleFilter">
          <img src="../assets/images/filter.png" alt="Filter" class="entry-icons">
          <span> Filter</span>
        </button>
        <button class="entry-icon-button" @click="showAddProductModal = true">
          <img src="../assets/images/add.png" alt="Add" class="entry-icons">
          <span> Add Product</span>
        </button>
        <button class="entry-icon-button-black" style="margin-right: 4px;" @click="downloadCSV">
          <img src="../assets/images/upload1.png" alt="Download" class="csv-icon">
          <span> Download CSV</span>
        </button>
        <button class="entry-icon-button-black" @click="showUploadCSVModal = true">
          <img src="../assets/images/upload1.png" alt="Upload" class="csv-icon">
          <span> Upload CSV</span>
        </button>

        <!-- Modal -->
        <div v-if="showUploadCSVModal" class="modal-overlay">
          <div class="modal-content">
            <!-- Close button -->
            <button class="close-btn" @click="showUploadCSVModal = false">×</button>
            <StockUploader />
          </div>
        </div>

        <div v-if="showAddProductModal" class="modal-overlay">
          <div class="modal-content">
            <form @submit.prevent="addProduct">
              <label class="prod-label">Product Name</label>
              <input v-model="newProduct.name" type="text" placeholder="Product Name" required />
              <label class="prod-label">Category</label>
              <input v-model="newProduct.category" type="text" placeholder="Category" required />
              <label class="prod-label">SKU</label>
              <input v-model="newProduct.sku" type="text" placeholder="SKU" required />
              <label class="prod-label">Unit Price</label>
              <input v-model="newProduct.unit_price" type="number" placeholder="Unit Price" required />
              <label class="prod-label">Available size</label>
              <input v-model="newProduct.available_size" type="text" placeholder="Available Size" />
              <label class="prod-label">Location</label>
              <input v-model="newProduct.location" type="text" placeholder="Location" />
              <label class="prod-label">Reorder level</label>
              <input v-model="newProduct.reorder_level" type="number" placeholder="Reorder Level" required />
              <label class="prod-label">Supplier</label>
              <select v-model="newProduct.supplier_id" required>
                <option value="" disabled>Select Supplier</option>
                <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">
                  {{ supplier.name }}
                </option>
              </select>
              <div class="modal-actions" style="margin-bottom: 40px; margin-left: 60px;">
                <button class="modal-buttons" type="submit">Add</button>
                <button class="modal-buttons" type="button" @click="showAddProductModal = false">Cancel</button>
              </div>
            </form>
          </div>
        </div>

        <!-- Filter Dropdown -->
        <div v-if="showFilter" class="filter-dropdown">
          <div class="filter-header">
            <h5>Filter Options</h5>
            <button class="close-filter-btn" @click="toggleFilter">×</button>
          </div>
          <form @submit.prevent="applyFilters">
            <div class="filter-group">
              <label>Category:</label>
              <select v-model="filters.category">
                <option value="">All Categories</option>
                <option v-for="category in uniqueCategories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>

            <div class="filter-group">
              <label>Location:</label>
              <select v-model="filters.location">
                <option value="">All Locations</option>
                <option v-for="location in uniqueLocations" :key="location" :value="location">
                  {{ location }}
                </option>
              </select>
            </div>

            <div class="filter-group">
              <label>Supplier:</label>
              <select v-model="filters.supplier_id">
                <option value="">All Suppliers</option>
                <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">
                  {{ supplier.name }}
                </option>
              </select>
            </div>

            <div class="filter-group">
              <label>Price Range:</label>
              <div class="price-range">
                <input v-model.number="filters.minPrice" type="number" placeholder="Min" min="0" />
                <span>to</span>
                <input v-model.number="filters.maxPrice" type="number" placeholder="Max" min="0" />
              </div>
            </div>

            <div class="filter-group">
              <label>Stock Level:</label>
              <select v-model="filters.stockStatus">
                <option value="">All</option>
                <option value="low">Low Stock</option>
                <option value="normal">Normal</option>
                <option value="high">High Stock</option>
              </select>
            </div>

            <div class="filter-actions">
              <button type="submit" class="apply-filter-btn">Apply Filters</button>
              <button type="button" @click="resetFilters" class="reset-filter-btn">Reset</button>
            </div>
          </form>
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th @click="sortTable('name')">
              Product
              <span class="sort-icon" v-if="sortKey === 'name'">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th @click="sortTable('category')">
              Category
              <span class="sort-icon" v-if="sortKey === 'category'">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th @click="sortTable('sku')">
              SKU
              <span class="sort-icon" v-if="sortKey === 'sku'">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th>Available Size</th>
            <th @click="sortTable('unit_price')">
              Unit Price
              <span class="sort-icon" v-if="sortKey === 'unit_price'">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th @click="sortTable('location')">
              Location
              <span class="sort-icon" v-if="sortKey === 'location'">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th @click="sortTable('total_revenue')">
              Total Revenue
              <span class="sort-icon" v-if="sortKey === 'total_revenue'">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th @click="sortTable('reorder_level')">
              Reorder Level
              <span class="sort-icon" v-if="sortKey === 'reorder_level'">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
            <th @click="sortTable('supplier.name')">
              Supplier
              <span class="sort-icon" v-if="sortKey === 'supplier.name'">
                {{ sortOrder === 'asc' ? '▲' : '▼' }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in paginatedInventory" :key="product.id">
            <td>{{ product.name }}</td>
            <td class="category-cell"
              @dblclick="enableEdit(product.id, 'category')"
              @blur="saveEdit(product, 'category', $event)"
              :contenteditable="editingCell.id === product.id && editingCell.field === 'category'"
              suppress-contenteditable-warning >
              {{ product.category }}
            </td>
            <td class="sku-cell">{{ product.sku }}</td>
            <td
              @dblclick="enableEdit(product.id, 'available_size')"
              @blur="saveEdit(product, 'available_size', $event)"
              :contenteditable="editingCell.id === product.id && editingCell.field === 'available_size'"
            >
              {{ product.available_size }}
            </td>
            <td>${{ product.unit_price }}</td>
            <td>{{ product.location }}</td>
            <td>${{ product.total_revenue }}</td>
            <td
              @dblclick="enableEdit(product.id, 'reorder_level')"
              @blur="saveEdit(product, 'reorder_level', $event)"
              :contenteditable="editingCell.id === product.id && editingCell.field === 'reorder_level'"
            >
              {{ product.reorder_level }}
            </td>
            <td>{{ getSupplierName(product.supplier.id) }}</td>
          </tr>
          <tr v-if="paginatedInventory.length === 0">
            <td colspan="9" class="no-results">No products match your search criteria</td>
          </tr>
        </tbody>
      </table>
      
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1" class="pg-button">Previous</button>

        <button class="button"
          v-for="page in totalPages" 
          :key="page" 
          @click="goToPage(page)"
          :class="{ active: currentPage === page }"
        >
          {{ page }}
        </button>

        <button @click="nextPage" :disabled="currentPage === totalPages" class="pg-button">Next</button>
      </div>

    </div>
  </BaseLayout>
</template>

<script>
import axios from 'axios';
import BaseLayout from "../components/BaseLayout.vue";
import { useAuthStore, getCSRFToken } from "../store/auth";
import { useProductsStore } from '../store/products'
import StockUploader from '../components/StockUploader.vue';

export default {
  components: {
    BaseLayout,
    StockUploader,
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 9,
      inventory: [],
      filteredInventory: [],
      suppliers: [],
      showAddProductModal: false,
      showUploadCSVModal: false,
      showFilter: false,
      searchQuery: '',
      sortKey: 'name',
      sortOrder: 'asc',
      filters: {
        category: '',
        location: '',
        supplier_id: '',
        minPrice: null,
        maxPrice: null,
        stockStatus: '',
      },
      newProduct: {
        name: '',
        category: '',
        sku: '',
        unit_price: '',
        available_size: '',
        location: '',
        reorder_level: 10,
        supplier_id: ''
      },
      csvFile: null,
      editingCell: { id: null, field: null },
      user: null, // this will be set by fetchUser()
    };
  },
  computed: {
    userRole() {
      return this.user?.role || '';
    },
    paginatedInventory() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredInventory.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredInventory.length / this.itemsPerPage);
    },
    uniqueCategories() {
      return [...new Set(this.inventory.map(item => item.category))];
    },
    uniqueLocations() {
      return [...new Set(this.inventory.map(item => item.location))];
    }
  },
  watch: {
    searchQuery: {
      handler() {
        this.filterInventory();
      },
      immediate: true
    },
    inventory: {
      handler() {
        this.filterInventory();
      },
      immediate: true
    }
  },
  created() {
    this.fetchInventory();
    this.fetchSuppliers();
    this.fetchUser();
  },
  setup() {
    const auth = useAuthStore(); 
    return { auth };
  },
  methods: {
    fetchInventory() {
      axios
        .get('http://localhost:8000/api/inventory/', {
          withCredentials: true,
        })
        .then(response => {
          console.log("Inventory data:", response.data);
          this.inventory = response.data;
          this.filterInventory();
        })
        .catch(error => {
          console.error('Error fetching inventory:', error);
          alert('Failed to load inventory data');
        });
    },
    fetchUser: async function () {
      const authStore = useAuthStore();
      try {
        const response = await fetch("http://localhost:8000/api/get_user_info", {
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.user = data;
          authStore.user = data;
          authStore.isAuthenticated = true;
          console.log("Logged in user:", data);
        } else {
          this.user = null;
          authStore.user = null;
          authStore.isAuthenticated = false;
        }
      } catch (error) {
        console.error("Failed to fetch user", error);
        this.user = null;
        authStore.user = null;
        authStore.isAuthenticated = false;
      }
      authStore.saveState();
    },
    fetchSuppliers() {
      axios
        .get('http://127.0.0.1:8000/api/suppliers/')
        .then(response => {
          this.suppliers = response.data;
        })
        .catch(error => {
          console.error('Error fetching suppliers:', error);
          alert('Failed to load supplier data');
        });
    },
    getSupplierName(supplierId) {
      const supplier = this.suppliers.find(s => s.id === supplierId);
      return supplier ? supplier.name : 'Unknown Supplier';
    },
    async addProduct() {
      try {
        const productsStore = useProductsStore()
        const newProduct = await productsStore.addProduct(this.newProduct)
        
        // Handle success
        this.inventory.push(newProduct)
        this.showAddProductModal = false
        this.resetNewProduct()
      } catch (error) {
        this.error = error.message
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    goToPage(page) {
      this.currentPage = page;
    },
    resetNewProduct() {
      this.newProduct = {
        name: '',
        category: '',
        sku: '',
        unit_price: '',
        available_size: '',
        location: '',
        reorder_level: 10,
        supplier_id: ''
      };
    },
    handleFileUpload(event) {
      this.csvFile = event.target.files[0];
    },
    submitCSV() {
      if (!this.csvFile) {
        alert('Please select a CSV file first!');
        return;
      }

      const formData = new FormData();
      formData.append('csv_file', this.csvFile);

      axios.post('http://127.0.0.1:8000/api/upload-product-csv/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then(() => {
          alert('CSV uploaded successfully');
          this.showUploadCSVModal = false;
          this.fetchInventory();
          this.csvFile = null;
        })
        .catch(error => {
          console.error('Error uploading CSV:', error);
          alert(error.response?.data?.message || 'Failed to upload CSV');
        });
    },
    downloadCSV() {
      axios
        .get('http://127.0.0.1:8000/api/export_products_to_csv/', {
          responseType: 'blob'
        })
        .then(response => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'products.csv');
          document.body.appendChild(link);
          link.click();
          link.remove();
        })
        .catch(error => {
          console.error('Error downloading CSV:', error);
          alert('Failed to download CSV');
        });
    },
    toggleFilter() {
      this.showFilter = !this.showFilter;
    },
    applyFilters() {
      this.filterInventory();
      // After applying filters, check if we need to reset the current page
      if (this.currentPage > this.totalPages && this.totalPages > 0) {
        this.currentPage = 1;
      }
    },
    resetFilters() {
      this.filters = {
        category: '',
        location: '',
        supplier_id: '',
        minPrice: null,
        maxPrice: null,
        stockStatus: '',
      };
      this.searchQuery = '';
      this.filterInventory();
    },
    filterInventory() {
      let filtered = [...this.inventory];
      
      // Apply search query filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(item => 
          item.name.toLowerCase().includes(query) || 
          item.category.toLowerCase().includes(query) || 
          item.sku.toLowerCase().includes(query) ||
          item.location?.toLowerCase().includes(query) ||
          this.getSupplierName(item.supplier.id).toLowerCase().includes(query)
        );
      }
      
      // Apply category filter
      if (this.filters.category) {
        filtered = filtered.filter(item => item.category === this.filters.category);
      }
      
      // Apply location filter
      if (this.filters.location) {
        filtered = filtered.filter(item => item.location === this.filters.location);
      }
      
      // Apply supplier filter
      if (this.filters.supplier_id) {
        filtered = filtered.filter(item => item.supplier.id === this.filters.supplier_id);
      }
      
      // Apply price range filter
      if (this.filters.minPrice !== null && this.filters.minPrice !== '') {
        filtered = filtered.filter(item => parseFloat(item.unit_price) >= this.filters.minPrice);
      }
      
      if (this.filters.maxPrice !== null && this.filters.maxPrice !== '') {
        filtered = filtered.filter(item => parseFloat(item.unit_price) <= this.filters.maxPrice);
      }
      
      // Apply stock status filter
      if (this.filters.stockStatus) {
        switch(this.filters.stockStatus) {
          case 'low':
            filtered = filtered.filter(item => parseFloat(item.quantity) <= item.reorder_level);
            break;
          case 'normal':
            filtered = filtered.filter(item => 
              parseFloat(item.quantity) > item.reorder_level && 
              parseFloat(item.quantity) <= item.reorder_level * 2
            );
            break;
          case 'high':
            filtered = filtered.filter(item => parseFloat(item.quantity) > item.reorder_level * 2);
            break;
        }
      }
      
      // Apply sorting
      filtered.sort((a, b) => {
        let aValue = this.getSortValue(a, this.sortKey);
        let bValue = this.getSortValue(b, this.sortKey);
        
        // Handle string comparison
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          aValue = aValue.toLowerCase();
          bValue = bValue.toLowerCase();
        }
        
        if (aValue < bValue) return this.sortOrder === 'asc' ? -1 : 1;
        if (aValue > bValue) return this.sortOrder === 'asc' ? 1 : -1;
        return 0;
      });
      
      this.filteredInventory = filtered;
    },
    getSortValue(item, key) {
      // Handle nested properties like 'supplier.name'
      if (key.includes('.')) {
        const parts = key.split('.');
        let value = item;
        for (const part of parts) {
          value = value[part];
          if (value === undefined) return '';
        }
        return value;
      }
      
      // Handle special case for supplier
      if (key === 'supplier.name') {
        return this.getSupplierName(item.supplier.id);
      }
      
      return item[key];
    },
    sortTable(key) {
      // If clicking the same header, toggle sort order
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        // If clicking a different header, set it as the new sort key and default to ascending
        this.sortKey = key;
        this.sortOrder = 'asc';
      }
      
      this.filterInventory();
    },
    enableEdit(productId, field) {
      const editableFieldsByRole = {
        Admin: ['category', 'available_size', 'total_revenue', 'reorder_level', 'unit_price'],
        FinancialAdmin: ['unit_price', 'available_size'],
        StockChecker: ['unit_price'],
      };

      if (editableFieldsByRole[this.userRole]?.includes(field)) {
        this.editingCell = { id: productId, field };
      }
    },
    async saveEdit(product, field, event) {
      const updatedValue = event.target.innerText.trim();
      const productsStore = useProductsStore();

      try {
        const updateData = { [field]: updatedValue };
        const updated = await productsStore.updateProduct(product.id, updateData);
        product[field] = updated[field];
      } catch (error) {
        console.error("Update error:", error);
      } finally {
        this.editingCell = { id: null, field: null };
      }
    },
    validateField(field, value) {
      switch (field) {
        case 'category':
          return value.length > 0 && value.length <= 50; 
        case 'available_size':
          return /^[a-zA-Z0-9, ]+$/.test(value); 
        case 'reorder_level':
          return Number.isInteger(+value) && +value > 0; 
        case 'unit_price':
          return !isNaN(value) && +value > 0; 
        default:
          return true;
      }
    },
  },
};
</script>

<style scoped>

.pagination {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
  background-color: white;
}

.sku-cell {
  padding: 1px;
  color: #4444;
  font-size: 10px;
}
.category-cell {
  background: linear-gradient(120deg, #dcb5ff, #ffcccc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  font-weight: lighter;
  text-transform: uppercase;
  font-size: 9px;
}
.history-heading-span {
   background: linear-gradient(120deg, #dcb5ff, #ffcccc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

button.active {
  font-weight: bold;
  border: 1px solid white;
  color: #4444;
  background-color: white;
  border-radius: 10px;
  font-size: 11px;
}

.pg-button {
  color: white;
  font-size: 9px;
  border: 1px solid white;
  border-radius: 10px;
  background: #FF5B8D;
}

.button {
  background-color: white;
  color: #4444;
  background: white;
  font-size: 11px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: transparent;
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease-out;
  backdrop-filter: blur(8px);
  margin-top: -12px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  width: 90%;
  height: 90%;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes slideUp {
  from { transform: translateY(50px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: #ff5b8d;
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  font-size: 9px;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(255, 91, 141, 0.3);
  transition: all 0.2s ease;
  margin-top: 5px;
  margin-right: 5px;
}

.close-btn:hover {
  transform: scale(1.1);
  background: #ff3a7a;
}

/* Stock Upload Panel Styling */
.stock-upload-panel {
  display: flex;
  height: 100%;
  background: linear-gradient(to bottom, #f9f9f9, #f0f0f0);
  overflow: auto;
  align-items: center;
  justify-content: center;
}

/* Left Side - Upload Section */
.upload-section {
  flex-direction: column;
  border-right: 1px dashed #ddd;
  overflow-y: auto;
  background: white;
  
}

.upload-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 10px;
  background: linear-gradient(90deg, #00c9ff, #92fe9d, #ff758c);
}

.section-title {
  font-size: 28px;
  margin-bottom: 30px;
  color: #333;
  font-weight: 700;
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 60px;
  height: 4px;
  background: transparent;
  border-radius: 2px;
}

.filter-dropdown {
  position: absolute;
  top: 60px;
  right: 20px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
  width: 300px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.filter-header h5 {
  margin: 0;
  font-size: 11px;
  font-weight: lighter;
}

.close-filter-btn {
  background: none;
  border: none;
  font-size: 10px;
  cursor: pointer;
  color: #666;
  background-color: #4444;
  border-radius: 10px;
}

.filter-group {
  margin-bottom: 15px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  font-size: 11px;
  text-align: start;
  color: #4444;
}

.filter-group select,
.filter-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 10px;
  background-color: white;
  color: #4444;
  transition: border-color 0.3s;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.price-range input {
  flex: 1;
}

.price-range span {
  font-size: 12px;
  color: #666;
}

.filter-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.apply-filter-btn,
.reset-filter-btn {
  padding: 8px 15px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.apply-filter-btn {
  background-color: #FF5B8D;
  color: white;
  border: none;
  font-size: 9px;
  font-weight: 500;
  transition: background-color 0.3s;
  padding: 3px 20px;
  height: 35px;
}

.reset-filter-btn {
  background-color: #f1f1f1;
  border: 1px solid #ddd;
  font-size: 9px;
  color: #333;
  padding: 3px 20px;
  height: 35px;
  transition: background-color 0.3s;
  margin-left: 10px;
}

/* Search input styles */
.search-container {
  position: relative;
  margin-right: 10px;
  margin-right: 380px;
  border-radius: 10px;
}

.search-input {
  padding: 7px 10px 5px 35px;
  border: 1px solid #ddd;
  border-radius: 10px;
  width: 250px;
  font-size: 11px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>');
  background-repeat: no-repeat;
  background-position: 10px center;
  background-size: 16px;
  color: #444;
}

/* Table header sorting styles */
table th {
  cursor: pointer;
  position: relative;
  user-select: none;
}

.sort-icon {
  margin-left: 5px;
  font-size: 10px;
}

.no-results {
  text-align: center;
  padding: 20px;
  color: #666;
}

.header-entry-icons-inventory {
  display: flex;
  align-items: end;
}

.entry-icons {
  width: 17px;
  height: 17px;
}

</style>
