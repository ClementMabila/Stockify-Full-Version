<template>
    <div class="main-container">
      <div id="dashboard" class="d-flex vh-100">

        <div class="sidebar">
        <ul class="nav flex-column">
        <li class="nav-item">
            <router-link to="/Investments" class="nav-link"><span><img src="../assets/images/animated.png" alt="Google Icon" class="icon-side" /></span>Investment</router-link>
        </li>
        <li class="nav-item">
            <router-link to="/InvestmentsDisplay" class="nav-link"><span><img src="../assets/images/stocks-icons2.png" alt="Google Icon" class="icon-side" /></span>Org Stats</router-link>
        </li>
        <li class="nav-item">
            <router-link to="/Messanger" class="nav-link"><span><img src="../assets/images/messanger.png" alt="Google Icon" class="icon-side" /></span>Messanger</router-link>
        </li>
        <li class="nav-item">
            <router-link to="/Profile" class="nav-link"><span><img src="../assets/images/user-icon.png" alt="Google Icon" class="icon-side" /></span>Profile</router-link>
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
                          <div class="notification-header-a">
                              <h5>Notifications</h5>
                              <small v-if="unseenCount > 0" class="mark-read" @click="markNotificationsSeen">Mark all as read</small>
                          </div>
                          <div class="notification-list-a">
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
                <div class="dropdown-content settings-dropdown">
                    <a class="dark-a" href="#">Account Settings</a>
                    <a class="dark-a" href="#">Preferences</a>
                    <a class="dark-a" href="#" @click.prevent="logout">Log Out</a>
                </div>
            </div>

                  <a href="/profile/">
                      <img src="../assets/images/profile_pic.png" alt="Profile" class="app-main-icons profile-pic">
                  </a>
              </div>
          </div>

          <slot></slot>
        </section>
      </div>
    </div>
  </template>
  
<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useAuthStore } from "../store/auth";
import { useRouter } from "vue-router";

export default {
  name: "BaseLayoutUI",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const notifications = ref([]);
    const unseenCount = ref(0);
    const showDropdown = ref(false);

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

    const markNotificationsSeen = async () => {
      try {
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

    const logout = async () => {
      try {
        console.log("Logging out..."); 
        await authStore.logout(router); 
      } catch (error) {
        console.error("Logout failed", error);
      }
    };

    onMounted(() => {
      fetchNotifications();
      setInterval(fetchNotifications, 5000);
    });

    return {
      notifications,
      unseenCount,
      showDropdown,
      toggleDropdown,
      logout,
    };
  },
};
</script>

<style src="../assets/css/dashboard.css"></style>