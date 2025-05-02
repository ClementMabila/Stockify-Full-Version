<template>
  <BaseLayout>
    <div class="sales-entrie-container">
      <h4 class="history-heading">Inventory</h4>

      <div class="header-entry-icons-inventory">
        <button class="entry-icon-button" @click="toggleFilter">
          <img src="../assets/images/filter.png" alt="Search" class="entry-icons">
          <span> Filter</span>
        </button>
        <button class="entry-icon-button" @click="showAddProductModal = true">
          <img src="../assets/images/add.png" alt="Search" class="entry-icons">
          <span> Add Product</span>
        </button>
        <button class="entry-icon-button-black" @click="downloadCSV">
          <img src="../assets/images/upload1.png" alt="Download" class="csv-icon">
          <span> Download CSV</span>
        </button>
        <button class="entry-icon-button-black" @click="showUploadCSVModal = true">
          <img src="../assets/images/upload1.png" alt="Upload" class="csv-icon">
          <span> Upload CSV</span>
        </button>

        <div v-if="showAddProductModal"  class="modal-overlay">
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

        <div v-if="showFilter" class="filter-section">
        <h5>Filter Options</h5>
        <form @submit.prevent="applyFilters">
          <label>Category:</label>
          <input v-model="filters.category" type="text" placeholder="Enter category" />

          <label>SKU:</label>
          <input v-model="filters.sku" type="text" placeholder="Enter SKU" />

          <label>Price Range:</label>
          <input v-model.number="filters.minPrice" type="number" placeholder="Min Price" />
          <input v-model.number="filters.maxPrice" type="number" placeholder="Max Price" />

          <button type="submit">Apply Filters</button>
          <button type="button" @click="resetFilters">Reset</button>
        </form>
      </div>


        <div v-if="showUploadCSVModal" class="csv-modal-overlay">
          <div class="csv-modal-content">
            <input type="file" @change="handleFileUpload" accept=".csv" class="csv-input" />
            <button class="csv-buttons" @click="submitCSV">Submit CSV</button>
            <button class="csv-buttons" @click="showUploadCSVModal = false">Close</button>
          </div>
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>SKU</th>
            <th>Available Size</th>
            <th>Unit Price</th>
            <th>Location</th>
            <th>Total Revenue</th>
            <th>Reorder Level</th>
            <th>Supplier</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in inventory" :key="product.id">
            <td>{{ product.name }}</td>
            <td
              @dblclick="enableEdit(product.id, 'category')"
              @blur="saveEdit(product, 'category', $event)"
              :contenteditable="editingCell.id === product.id && editingCell.field === 'category'"
              suppress-contenteditable-warning
            >
              {{ product.category }}
            </td>
            <td>{{ product.sku }}</td>
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
        </tbody>
      </table>
    </div>
  </BaseLayout>
</template>

<script>
import axios from 'axios';
import BaseLayout from "../components/BaseLayout.vue";
import { useAuthStore, getCSRFToken } from "../store/auth";
import { useProductsStore } from '../store/products'

export default {
  components: {
    BaseLayout,
  },
  data() {
    return {
      inventory: [],
      suppliers: [],
      showAddProductModal: false,
      showUploadCSVModal: false,
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
      user: null,
      editingCell: { id: null, field: null },
      user: null, // this will be set by fetchUser()
    };
  },
  computed: {
  userRole() {
    return this.user?.role || '';
  },
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
      console.log('Filter button clicked');
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