<template>
  <BaseLayout>
    <div class="sales-entrie-container">
      <h2 class="history-heading">Sales Entry</h2>
      <div class="sales-actions">
        <div class="search-field-fields">
          <img src="../assets/images/search.png" alt="Search" class="search-icon">
          <input type="text" placeholder="Search Entry..." />
        </div>
        <div class="header-entry-icons" style="margin-right: -310px;">
          <button class="entry-icon-button" @click="toggleFilter">
            <img src="../assets/images/filter.png" alt="Search" class="entry-icons">
            <span> Filter</span>
          </button>
          <button class="entry-icon-button-black" @click="showModal = true">
            <img src="../assets/images/plus.png" alt="Add" class="entry-icons">
            <span> Add Entry</span>
          </button>
          <button 
            class="entry-icon-button-black" 
            @click="showModal = true"
            v-if="canCreateSales"
          >
            <img src="../assets/images/plus.png" alt="Add" class="entry-icons">
            <span> Add Entry</span>
          </button>

          <div v-if="showModal" class="modal-overlay">
            <div class="modal-content">
              <label>Product:</label>
              <select v-model="newSale.product_id" required>
                <option value="" disabled>Select Product</option>
                <option 
                  v-for="product in products" 
                  :key="product.id" 
                  :value="product.id"
                >
                  {{ product.name }} ({{ product.sku }})
                </option>
              </select>

              <label>Customer:</label>
              <select v-model="newSale.customer_id" required>
                <option value="" disabled>Select Customer</option>
                <option 
                  v-for="customer in customers" 
                  :key="customer.id" 
                  :value="customer.id"
                >
                  {{ customer.name }}
                </option>
              </select>

              <label>Quantity Sold:</label>
              <input 
                type="number" 
                min="1" 
                v-model.number="newSale.quantity_sold" 
                required
              >

              <label>Sale Price:</label>
              <input 
                type="number" 
                min="0" 
                step="0.01" 
                v-model.number="newSale.sale_price" 
                required
              >

              <label>Status:</label>
              <select v-model="newSale.status">
                <option value="Completed">Completed</option>
                <option value="Pending">Pending</option>
                <option value="Cancelled">Cancelled</option>
              </select>

              <div class="modal-actions">
                <button class="modal-buttons" @click="submitSale">Submit</button>
                <button class="modal-buttons" @click="showModal = false">Cancel</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <table class="entry-table">
        <thead>
          <tr>
            <th class="sales-entry-th">Date</th>
            <th class="sales-entry-th">Product</th>
            <th class="sales-entry-th">SKU</th>
            <th class="sales-entry-th">Quantity</th>
            <th class="sales-entry-th">Unit Price</th>
            <th class="sales-entry-th">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sale in salesEntries" :key="sale.id" class="sales-entry-tr">
            <td>{{ new Date(sale.sale_date).toLocaleDateString() }}</td>
            <td>{{ sale.product }}</td>
            <td>{{ sale.sku }}</td>
            <td>{{ sale.quantity_sold }}</td>
            <td>${{ sale.sale_price }}</td>
            <td class="status-td">
              <span 
                class="status-box" 
                :class="getStatusClass(sale.status)"
              ></span>
              <span 
                class="status-text"
                :class="getStatusClass(sale.status)"
              >
                {{ sale.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </BaseLayout>
</template>

<script>
import BaseLayout from "../components/BaseLayout.vue";
import { useAuthStore } from "../store/auth";
import { useSalesStore } from '../store/sales';
import { useProductsStore } from '../store/products';
import axios from 'axios';
import http from '../services/http';

export default {
  name: "SalesEntriesPage",
  components: {
    BaseLayout,
  },
  data() {
    return {
      salesEntries: [],
      products: [],
      customers: [],
      showModal: false,
      canCreateSales: false,
      newSale: {
        product_id: null,
        customer_id: null,
        quantity_sold: 1,
        sale_price: 0,
        status: 'Completed'
      }
    };
  },
  async created() {
    await this.fetchUser();
    this.checkPermissions();
    this.fetchSalesEntries();
    this.fetchProducts();
    this.fetchCustomers();
  },
  setup() {
    const auth = useAuthStore(); 
    return { auth };
  },
  methods: {
        async fetchSalesEntries() {
      const salesStore = useSalesStore();
      try {
        const salesData = await salesStore.fetchSales();
        console.log("Sales data:", salesData);
        this.salesEntries = salesData;
      } catch (error) {
        console.error("Error fetching sales entries:", error);
        alert('Failed to load sales data');
      }
    },
    
    async fetchProducts() {
      const productsStore = useProductsStore();
      try {
        this.products = await productsStore.fetchProducts();
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    },
    
    async fetchCustomers() {
      try {
        const response = await http.get('/api/customers/');
        this.customers = response;
      } catch (error) {
        console.error("Error fetching customers:", error);
      }
    },
    
    async submitSale() {
      try {
        const salesStore = useSalesStore();
        const newSale = await salesStore.addSale({
        product: this.newSale.product_id,
        customer: this.newSale.customer_id,
        quantity_sold: this.newSale.quantity_sold,
        sale_price: this.newSale.sale_price,
        status: this.newSale.status
        });
        
        this.salesEntries.unshift(newSale);
        this.showModal = false;
        this.resetSaleForm();
        alert('Sale recorded successfully!');
      } catch (error) {
        console.error('Error:', error.response?.data || error);
        alert(error.response?.data?.error || 'Failed to record sale');
      }
    },
    
    resetSaleForm() {
      this.newSale = {
        product_id: null,
        customer_id: null,
        quantity_sold: 1,
        sale_price: 0,
        status: 'Completed'
      };
    },
    
    async fetchUser() {
      try {
        await this.auth.fetchUser();
        this.user = this.auth.user;
      } catch (error) {
        console.error("Failed to fetch user", error);
      }
    },
    
    checkPermissions() {
      this.canCreateSales = ['Admin', 'Financial Admin'].includes(this.user?.role);
    },
    
    getStatusClass(status) {
      return {
        'status-completed': status === 'Completed',
        'status-pending': status === 'Pending',
        'status-cancelled': status === 'Cancelled'
      };
    }
  }
};
</script>
