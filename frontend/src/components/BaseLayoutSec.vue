<template>
  <div class="main-container">
    <div id="dashboard" class="d-flex vh-100">
      <section class="main-content">
        <div class="heading">
        <h4 class="logo">Stockify</h4>
        
        </div>

        <slot></slot>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
name: "BaseLayout",
setup() {
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

      onMounted(() => {
        fetchNotifications();
        setInterval(fetchNotifications, 5000); 
      });

      return {
        notifications,
        unseenCount,
        showDropdown,
        toggleDropdown,
      };
    },
};
</script>


<style src="../assets/css/dashboard.css"></style>
