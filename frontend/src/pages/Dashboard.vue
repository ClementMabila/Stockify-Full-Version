<template>
  <div class="main-container">
    <div id="dashboard" class="d-flex vh-100">
  <div class="sidebar">
    <ul class="nav flex-column">
      <li class="nav-item">
        <router-link to="/dashboard" class="nav-link"><span><img src="../assets/images/d-icon-1.png" alt="Google Icon" class="icon-side" /></span>Dashboard</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/sales-entries" class="nav-link"><span><img src="../assets/images/d-icon-2.png" alt="Google Icon" class="icon-side" /></span>Sales Entry</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/stock-history" class="nav-link-free">Stock History</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/inventory" class="nav-link-free">Inventory</router-link>
      </li>
    </ul>
  </div>

  <section class="main-content flex-grow-1 p-4 bg-light">
    <div class="heading">
        <h4 class="logo">Stockify</h4>
        <div class="header-icons">
                <div class="search-field">
                    <img src="../assets/images/search.png" alt="Search" class="search-icon">
                    <input type="text" placeholder="Search for anything here" />
                </div>

                <div class="dropdown notification-dropdown"
                    @mouseenter="showDropdown = true"
                    @mouseleave="showDropdown = false">
                    
                    <a href="#" id="notification-icon" class="notification-icon-wrapper">
                        <img src="../assets/images/notification.png" alt="Notification" class="app-main-icons">
                        <span v-if="unseenCount > 0" class="notif-dot">{{ unseenCount > 9 ? '9+' : unseenCount }}</span>
                    </a>

                    <div v-if="showDropdown" class="dropdown-content">
                        <div class="notification-header">
                            <h5>Notifications</h5>
                            <small v-if="unseenCount > 0" class="mark-read" @click="markNotificationsSeen">Mark all as read</small>
                        </div>
                        <div class="notification-list">
                            <p v-if="notifications.length === 0" class="empty-notifications">No new notifications</p>
                            <ul v-else>
                                <li v-for="notification in notifications" :key="notification.id">
                                    <div class="notification-content">
                                        <strong>Requested {{ notification.quantity }} of {{ notification.product }}</strong>
                                        <p>{{ notification.status }} • {{ notification.date }}</p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

          <div class="dropdown">
              <a href="#" id="settings-icon">
                  <img src="../assets/images/settings.png" alt="Settings" class="app-main-icons">
              </a>
              <div class="dropdown-content-a settings-dropdown">
                    <a href="#">Account Settings</a>
                    <a href="#">Preferences</a>
                    <a href="#" @click.prevent="logout">Log Out</a> <!-- Call the logout function -->
                </div>
          </div>

                <a href="/profile/">
                    <img src="../assets/images/profile_pic.png" alt="Profile" class="app-main-icons profile-pic">
                </a>
            </div>
        </div>

    
    <div class="row d-flex justify-content-between" style="margin-right: 50px;">
    <div class="col-md-4 top-banner">
      <div class="banner banner-sales d-flex align-items-start">
        <div class="content">
          <h4>Sales Overview</h4>
          <div class="details">
            <section class="full-labels-section">
              <div class="full-label">
                <div class="icon-box">
                  <img src="../assets/images/dollar.png" alt="Sales Icon" class="icon" />
                </div>
                <div class="text-box">
                  <div class="label">Today Sales</div>
                  <div class="number">{{ stats.today_sales }}</div>
                </div>
              </div>

              <div class="full-label ms-3">
                <div class="icon-box">
                  <img src="../assets/images/graph.png" alt="Sales Chart Icon" class="icon" />
                </div>
                <div class="text-box">
                  <div class="label">Total Sales</div>
                  <div class="number">{{ stats.total_sales }}</div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>

    <div class="col-md-4 top-banner">
      <div class="banner banner-sales d-flex align-items-start">
        <div class="content">
          <h4>Inventory Overview</h4>
          <div class="details">
            <section class="full-labels-section">
              <div class="full-label">
                <div class="icon-box">
                  <img src="../assets/images/stock.png" alt="Stock Icon" class="icon" />
                </div>
                <div class="text-box">
                  <div class="label">Stock Available</div>
                  <div class="number">{{ stats.stock_available }}</div>
                </div>
              </div>

              <div class="full-label ms-3">
                <div class="icon-box">
                  <img src="../assets/images/cart.png" alt="Sales Chart Icon" class="icon" />
                </div>
                <div class="text-box">
                  <div class="label">Sold Items</div>
                  <div class="number">{{ stats.sold_items }}</div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>

    <div class="col-md-4 top-banner " >
      <div class="banner banner-sales-dark d-flex align-items-start">
        <div class="content">
          <h4 style="color: white;">Inventory Insights</h4>
          <div class="details">
            <section class="full-labels-section" style="margin-right: 10px;">
              <div class="full-label">
                <div class="icon-box">
                </div>
                <div class="text-box">
                  <div class="label" style="color: white;"> Total Expenses</div>
                  <div class="number" style="color: white;">{{ stats.total_expenses }}</div>
                </div>
              </div>

              <div class="full-label ms-3">
                <div class="icon-box">
                </div>
                <div class="text-box">
                  <div class="label" style="color: white;">Active Stock</div>
                  <div class="number" style="color: white;">{{ stats.active_stock }}</div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div class="graphs-section-display">
  <div class="graph-display">
    <section >
    <SalesStockChart/>
  </section>
  </div>
  <div class="graph-display" style="width: -120px;">
    <section >
    <SalesDistributionPie/>
  </section>
  </div>
  </div>

  <div class="graphs-section-display">
    <div class="graph-display">
      <section >
        <StockHistory/>
    </section>
    </div>
    <div class="graph-display secon-dis">
      <section >
      <StockAlerts/>
    </section>
  </div>
</div>

  </section>
  </div>
</div>
    <router-view></router-view>
</template>

<script>
import { ref, onMounted } from "vue";
import { useAuthStore } from "../store/auth";
import { useRouter } from "vue-router";
import axios from "axios";

import SalesStockChart from "../components/SalesStockChart.vue";
import SalesDistributionPie from "../components/SalesDistributionPie.vue";
import StockHistory from '../pages/StockHistory.vue';
import StockAlerts from '../pages/StockAlerts.vue';
import fetchDashboardStats from "../store/dashboardStats";

export default {
  name: "Dashboard",
  components: {
    SalesStockChart,
    SalesDistributionPie,
    StockHistory,
    StockAlerts,
  },
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const notifications = ref([]);
    const unseenCount = ref(0);
    const showDropdown = ref(false);

    const stats = ref({
      today_sales: 0,
      total_sales: 0,
      stock_available: 0,
      sold_items: 0,
      total_expenses: 0,
      active_stock: 0,
    });

    const fetchNotifications = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/notifications/");
        if (response.data.notifications) {
          notifications.value = response.data.notifications;
          unseenCount.value = response.data.unseen_count || 0;
        }
      } catch (error) {
        console.error("Error fetching notifications:", error);
      }
    };

    const fetchUser = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/user", {
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (response.ok) {
          const data = await response.json();
          authStore.user = data;
          authStore.isAuthenticated = true;
          console.log("Logged in user:", data);
        } else {
          authStore.user = null;
          authStore.isAuthenticated = false;
        }
      } catch (error) {
        console.error("Failed to fetch user", error);
        authStore.user = null;
        authStore.isAuthenticated = false;
      }
      authStore.saveState();
    };

    const logout = async () => {
      try {
        console.log("Logging out...");
        await authStore.logout(router);
      } catch (error) {
        console.error("Logout failed", error);
      }
    };

    const markNotificationsSeen = async () => {
      try {
        console.log("Marking notifications as seen...");
        await axios.post("http://127.0.0.1:8000/api/mark-notifications-seen/");
        unseenCount.value = 0;
      } catch (error) {
        console.error("Error marking notifications as seen:", error);
      }
    };

    const toggleDropdown = () => {
      showDropdown.value = !showDropdown.value;
      if (showDropdown.value && unseenCount.value > 0) {
        markNotificationsSeen();
      }
    };

    onMounted(async () => {
      fetchNotifications();
      fetchUser();

      try {
        stats.value = await fetchDashboardStats();
      } catch (error) {
        console.error("Could not load dashboard stats.");
      }

      setInterval(fetchNotifications, 5000);
    });

    return {
      notifications,
      unseenCount,
      showDropdown,
      toggleDropdown,
      logout,
      stats,
    };
  },
};
</script>

<style src="../assets/css/dashboard.css"></style>
