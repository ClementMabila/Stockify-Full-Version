<template>
  <div class="profile-container">
    <!-- Modern Profile Header with animated gradient -->
    <div class="profile-header">
    <div class="header-banner">
      <div class="banner-overlay"></div>
      <div class="banner-actions">
        <button class="banner-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
          Edit Cover
        </button>
      </div>
    </div>
    
    <div class="profile-header-content">
      <div class="avatar-container">
        <div v-if="userProfile.avatar" class="avatar-image">
          <img :src="userProfile.avatar" alt="Profile Avatar">
          <div class="avatar-status"></div>
        </div>
        <div v-else class="avatar-placeholder">
          <span>{{ userInitials }}</span>
          <div class="avatar-status"></div>
        </div>
        <div class="avatar-edit">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M8 2v4"></path>
            <path d="M16 2v4"></path>
            <rect x="2" y="9" width="20" height="13" rx="2"></rect>
            <circle cx="12" cy="16" r="4"></circle>
          </svg>
        </div>
      </div>
      
      <div class="user-info">
        <div class="user-name-container">
          <h1>{{ user.first_name }} {{ user.last_name }}</h1>
          <div class="verified-badge">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
        </div>
        
        <div class="role-badge">
          {{ userProfile.role }}
        </div>
        
        <div class="organization-container">
          <svg class="organization-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
          </svg>
          <p class="organization-name">{{ userProfile.organization.name }}</p>
        </div>
        
        <p class="user-bio">{{ userProfile.bio || 'No bio available' }}</p>
        
        <div class="user-stats">
          <div class="stat-item">
            <span class="stat-value">{{organizationMemberCount}}</span>
            <span class="stat-label">Connections</span>
          </div>
          <div class="stat-item">
            <span class="stat-value" style="font-size: 10px; color: white; background-color: #3fc5f0; border-radius: 10px; padding: 6px 10px; cursor: pointer;">Request Access</span>
            <span class="stat-label">Investments</span>
          </div>
          <div class="stat-item">
            <span class="stat-value" id="rating-output">{{ rateValue }}</span>
            <span class="stat-label">Rating</span>
          </div>
        </div>
        
        <div class="contact-actions">
          <button class="primary-button" @click="goToMessagingPage">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
            Message
          </button>
          <button class="secondary-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="8.5" cy="7" r="4"></circle>
              <line x1="20" y1="8" x2="20" y2="14"></line>
              <line x1="23" y1="11" x2="17" y2="11"></line>
            </svg>
            Connected
          </button>

        </div>
        
        <div class="info-section">
          <div class="info-item">
            <svg class="info-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
            <span class="info-text">{{ userProfile.location || 'Not specified' }}</span>
          </div>
          <div class="info-item">
            <svg class="info-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
              <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
            </svg>
            <span class="info-text">Member since, {{ formatDate(user.date_joined) }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="tab-navigation">
      <div class="nav-tab active">Overview</div>
      <div class="nav-tab">Details</div>
      <div class="nav-tab">Activity</div>
      <div class="nav-tab">Teams</div>
      <div class="nav-tab">Files</div>
      <div class="nav-tab">Settings</div>
    </div>

    <!-- Details Tab Content -->
<div class="details-content">
  <!-- Profile Information Card -->
  <div class="details-card profile-info-card">
    <div class="details-card-header">
      <h3>Profile Information</h3>
    </div>
    
    <div class="profile-details-grid">
      <div class="detail-item">
        <div class="detail-content">
          <span class="detail-label">Email</span>
          <span class="detail-value">{{ user.email }}</span>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-content">
          <span class="detail-label">Location</span>
          <span class="detail-value">{{ userProfile.location || 'Not specified' }}</span>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-content">
          <span class="detail-label">Role</span>
          <span class="detail-value">{{ userProfile.role }}</span>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-content">
          <span class="detail-label">Member Since</span>
          <span class="detail-value">{{ formatDate(user.date_joined) }}</span>
        </div>
      </div>

      <div class="detail-item">
        <div class="detail-content">
          <span class="detail-label">Bio</span>
          <span class="detail-value-bio">{{ userProfile.bio }}</span>
        </div>
      </div>
    </div>
  </div>

  <div class="details-card organization-card">
    <div class="org-card-header">
      <h3>
        Organisation
      </h3>
      <div class="plan-badge">
        {{ userProfile.organization.subscription_plan }}
        <span><svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> 
          <path d="M8.5 12.5L10.0089 14.0089C10.3526 14.3526 10.5245 14.5245 10.7198 14.5822C10.8914 14.6328 11.0749 14.6245 
          11.2412 14.5585C11.4305 14.4834 11.5861 14.2967 11.8973 13.9232L16 9M16.3287 4.75855C17.0676 4.77963 17.8001 5.07212 
          18.364 5.636C18.9278 6.19989 19.2203 6.9324 19.2414 7.67121C19.2623 8.40232 19.2727 8.76787 19.2942 8.85296C19.3401 
          9.0351 19.2867 8.90625 19.383 9.06752C19.428 9.14286 19.6792 9.40876 20.1814 9.94045C20.6889 10.4778 21 11.2026 21 
          12C21 12.7974 20.6889 13.5222 20.1814 14.0595C19.6792 14.5912 19.428 14.8571 19.383 14.9325C19.2867 15.0937 19.3401 
          14.9649 19.2942 15.147C19.2727 15.2321 19.2623 15.5977 19.2414 16.3288C19.2203 17.0676 18.9278 17.8001 18.364 
          18.364C17.8001 18.9279 17.0676 19.2204 16.3287 19.2414C15.5976 19.2623 15.2321 19.2727 15.147 19.2942C14.9649 19.3401 
          15.0937 19.2868 14.9325 19.3831C14.8571 19.4281 14.5912 19.6792 14.0595 20.1814C13.5222 20.6889 12.7974 21 12 21C11.2026 21 
          10.4778 20.6889 9.94047 20.1814C9.40874 19.6792 9.14287 19.4281 9.06753 19.3831C8.90626 19.2868 9.0351 19.3401 8.85296 
          19.2942C8.76788 19.2727 8.40225 19.2623 7.67121 19.2414C6.93238 19.2204 6.19986 18.9279 5.63597 18.364C5.07207 17.8001 
          4.77959 17.0676 4.75852 16.3287C4.73766 15.5976 4.72724 15.2321 4.70578 15.147C4.65985 14.9649 4.71322 15.0937 4.61691 
          14.9324C4.57192 14.8571 4.32082 14.5912 3.81862 14.0595C3.31113 13.5222 3 12.7974 3 12C3 11.2026 3.31113 10.4778 3.81862 
          9.94048C4.32082 9.40876 4.57192 9.14289 4.61691 9.06755C4.71322 8.90628 4.65985 9.03512 4.70578 8.85299C4.72724 8.7679 
          4.73766 8.40235 4.75852 7.67126C4.77959 6.93243 5.07207 6.1999 5.63597 5.636C6.19986 5.07211 6.93238 4.77963 7.67121 
          4.75855C8.40232 4.73769 8.76788 4.72727 8.85296 4.70581C9.0351 4.65988 8.90626 4.71325 9.06753 4.61694C9.14287 4.57195 
          9.40876 4.32082 9.94047 3.81863C10.4778 3.31113 11.2026 3 12 3C12.7974 3 13.5222 3.31114 14.0595 3.81864C14.5913 4.32084 14.8571 4.57194 14.9325 4.61693C15.0937 4.71324 14.9649 4.65988 15.147 4.70581C15.2321 4.72726 15.5976 4.73769 16.3287 4.75855Z" 
          stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg></span>
      </div>
    </div>
    
    <div class="org-details-grid">
      <div class="detail-item">
        <div class="detail-content">
          <span class="detail-label">Name</span>
          <span class="detail-value">{{ userProfile.organization.name }}</span>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-content">
          <span class="detail-label">Status</span>
          <span class="detail-value" :class="`status-${userProfile.organization.status.toLowerCase()}`">
            <span class="status-indicator"></span>
            {{ userProfile.organization.status }}
          </span>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-content">
          <span class="detail-label">Established</span>
          <span class="detail-value">{{ formatDate(userProfile.organization.date_established) }}</span>
        </div>
      </div>
      
      <div class="detail-item">
        <div class="detail-content">
          <span class="detail-label">Website</span>
          <a v-if="userProfile.organization.website" :href="userProfile.organization.website" target="_blank" class="website-link">
            {{ userProfile.organization.website }}
          </a>
          <span v-else class="detail-value">Not available</span>
        </div>
      </div>
    </div>
  </div>

</div>
  </div>
  </div>
</template>

<script>
import { useRouter, useRoute } from 'vue-router';
import { ref, computed, onMounted, watch } from 'vue';
import http from '../services/http';
import { getCSRFToken } from '../store/auth';

export default {
  name: 'UserProfileDetail',

  setup() {
    const userProfile = ref({
      role: '',
      bio: '',
      location: '',
      avatar: '',
      organization: {
        name: '',
        subscription_plan: '',
        status: '',
        logo: '',
        date_established: '',
        website: '',
      }
    });

    const user = ref({});
    const route = useRoute();
    const router = useRouter();
    const userId = computed(() => route.params.id);  // Get userId from the URL
    const organizationMembers = ref([]);
    console.log('User ID:', userId.value);

    // Fetching data when the page loads
    const fetchUserProfile = async () => {
      try {
        // Make an API request to fetch the profile based on the userId
        const response = await http.get(`/api/user-profile/${userId.value}/`);
        
        // Assuming the response has 'user' and 'profile' objects
        user.value = response.user;
        userProfile.value = response.profile;
        console.log('User Profile:', userProfile.value);
      } catch (error) {
        console.error('Failed to fetch user profile:', error);
      }
    };

    const fetchOrganizationMembers = async () => {
    try {
      if (!userId.value) return;
      const membersData = await http.get(`/api/organization/members/${userId.value}/`);
      organizationMembers.value = membersData || [];
      console.log('Raw data:', membersData);
    } catch (error) {
      console.error('Failed to fetch organization members:', error);
    }
  };

  const userInitials = computed(() => {
      if (user.value.first_name && user.value.last_name) {
        return `${user.value.first_name[0]}${user.value.last_name[0]}`;
      }
      return user.value.username ? user.value.username[0].toUpperCase() : '?';
    });

  const goToMessagingPage = () => {
      router.push({ name: 'MessagingPage' });
    };


  async function fetchUserRating(userId) {
    try {
      if (!userId) {
        console.error("Missing userId");
        return;
      }

      const response = await fetch(`http://localhost:8000/api/user-rating/${userId}/`, {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCSRFToken(),
        },
        credentials: 'include',
      });

      const data = await response.json();
      if (response.ok) {
        console.log(`User: ${data.username}, Role: ${data.role}, Rating: ${data.rating}`);
        document.getElementById("rating-output").textContent = `${data.rating}`;
      } else {
        console.error(data.error || "Failed to fetch rating");
      }
    } catch (error) {
      console.error("Error fetching rating:", error);
    }
  }

    // Call fetchUserProfile when component is mounted
    onMounted(async () => {
      await fetchUserProfile();
    });

    // You can format or handle the data for display if necessary
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      }).format(date);
    };

    const getStatusColor = (status) => {
      switch (status) {
        case 'Active': return 'green';
        case 'Inactive': return 'gray';
        case 'Suspended': return 'red';
        default: return 'gray';
      }
    };
    
    const organizationMemberCount = computed(() => organizationMembers.value.length);

    onMounted(async () => {
        fetchUserRating(userId.value);
        await fetchOrganizationMembers();
    });

    return {
      user,
      userProfile,
      formatDate,
      userInitials,
      getStatusColor,
      organizationMemberCount,
      goToMessagingPage,
    };
  }
};

</script>

<style scoped>
/* Modern Color Palette and Variables */
:root {
  --primary: #4f46e5;
  --primary-dark: #4338ca;
  --primary-light: #818cf8;
  --secondary: #10b981;
  --secondary-dark: #059669;
  --accent: #f97316;
  --danger: #ef4444;
  --success: #22c55e;
  --warning: #f59e0b;
  --dark: #1e293b;
  --light: #f8fafc;
  --gray: #94a3b8;
  --gray-light: #e2e8f0;
  --gray-dark: #475569;
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
  --radius: 0.5rem;
  --radius-lg: 1rem;
  --radius-sm: 0.25rem;
  --transition: all 0.3s ease;
}

.profile-container {
  font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
  color: var(--dark);
  background-color: #f1f5f9;
  padding-bottom: 2rem;
}

.profile-header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  z-index: 1;
}

@media (min-width: 768px) {
  .profile-header-content {
    flex-direction: row;
    text-align: left;
    align-items: center;
    justify-content: flex-start;
  }
}

    .header-banner {
      height: 130px;
      background: linear-gradient(120deg, #dcb5ff, #ffcccc);
      position: relative;
    }

    .banner-overlay {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 60px;
      background: linear-gradient(to top, rgba(0, 0, 0, 0.2), transparent);
    }

    .banner-actions {
      position: absolute;
      top: 20px;
      right: 20px;
      display: flex;
      gap: 12px;
    }

    .banner-button {
      background-color: rgba(255, 255, 255, 0.2);
      color: white;
      border: none;
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 11px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      backdrop-filter: blur(5px);
      transition: all 0.2s ease;
      margin-right: 50px;
    }

    .banner-button:hover {
      background-color: rgba(255, 255, 255, 0.3);
    }

    .profile-header-content {
      padding: 0 30px 30px;
      display: flex;
      position: relative;
    }

    .avatar-container {
      margin-top: -50px;
      position: relative;
      z-index: 2;
    }

    .avatar-image {
      width: 140px;
      height: 140px;
      border-radius: 50%;
      overflow: hidden;
      border: 5px solid white;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
      background-color: #f0f0f0;
      position: relative;
    }

    .avatar-image img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .avatar-placeholder {
      width: 140px;
      height: 140px;
      border-radius: 50%;
      background: linear-gradient(120deg, #dcb5ff, #ffcccc);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 48px;
      font-weight: 600;
      border: 5px solid white;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }

    .avatar-status {
      position: absolute;
      bottom: 10px;
      right: 10px;
      width: 24px;
      height: 24px;
      background-color: #10b981;
      border-radius: 50%;
      border: 3px solid white;
    }

    .avatar-edit {
      position: absolute;
      bottom: 0;
      right: 0;
      background-color: #f0f0f0;
      border-radius: 50%;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      border: 2px solid white;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      transition: all 0.2s ease;
    }

    .avatar-edit:hover {
      background-color: #e0e0e0;
    }

    .user-info {
      padding-left: 30px;
      padding-top: 20px;
      flex: 1;
    }

    .user-name-container {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 8px;
    }

    h1 {
      font-size: 28px;
      font-weight: 700;
      color: #1e293b;
      margin-right: 10px;
    }

    .verified-badge {
      background-color: #0ea5e9;
      color: white;
      border-radius: 50%;
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
    }

    .role-badge {
      display: inline-block;
      background-color: #f0f9ff;
      color: #0369a1;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 500;
      margin-bottom: 12px;
      border: 1px solid #bae6fd;
    }

    .organization-container {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
    }

    .organization-icon {
      width: 20px;
      height: 20px;
      color: #64748b;
    }

    .organization-name {
      font-size: 16px;
      color: #64748b;
      font-weight: 500;
      margin-bottom: -3px;
    }

    .user-bio {
      color: #475569;
      font-size: 16px;
      line-height: 1.6;
      margin-bottom: 20px;
      max-width: 100%;
      width: 900px;
    }

    .user-stats {
      display: flex;
      gap: 24px;
      margin-bottom: 20px;
    }

    .stat-item {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .stat-value {
      font-size: 18px;
      font-weight: 700;
      color: #1e293b;
    }

    .stat-label {
      font-size: 14px;
      color: #64748b;
    }

    .contact-actions {
      display: flex;
      gap: 12px;
    }


    .primary-button {
      background-color: #3fc5f0;
      color: white;
      border: none;
      border-radius: 6px;
      padding: 10px 18px;
      font-size: 15px;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }

    .primary-button:hover {
     border: 1px solid white;
    }

    .secondary-button {
      background-color: #f8fafc;
      color: #475569;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 10px 18px;
      font-size: 15px;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }

    .secondary-button:hover {
      background-color: #f1f5f9;
    }


    .info-section {
      display: flex;
      gap: 20px;
      margin-top: 15px;
    }

    .info-item {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .info-icon {
      color: #64748b;
    }

    .info-text {
      font-size: 14px;
      color: #475569;
    }

    .tab-navigation {
      display: flex;
      border-bottom: 1px solid #e2e8f0;
      margin-top: 20px;
      padding: 0 30px;
    }

    .nav-tab {
      padding: 16px 20px;
      font-size: 15px;
      font-weight: 500;
      color: #64748b;
      cursor: pointer;
      position: relative;
      transition: all 0.2s ease;
    }

    .nav-tab.active {
      color: #3fc5f0;
    }

    .nav-tab.active::after {
      content: '';
      position: absolute;
      bottom: -1px;
      left: 0;
      right: 0;
      height: 2px;
      background-color: #3fc5f0;
    }

    .nav-tab:hover:not(.active) {
      color: #334155;
    }

/* Main Container Layout */
.details-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px 30px;
  background-color: #f1f5f9;
}

/* Card Styles */
.details-card {
  background-color: #f7fbfcc0;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  border-radius: 10px;
  width: 96%;
  border: 1px solid var(--gray-light);
}

.details-card-header, .org-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--gray-light);
}

.details-card-header h3, .org-card-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 13px;
  font-weight: lighter;
  color: var(--dark);
}

/* Buttons */
.edit-button, .refresh-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 8px;
  border-radius: 10px;
  font-size: 11px;
  border: 1px solid var(--gray-light);
  background-color: #3fc5f0;
  color: white;
  cursor: pointer;
  transition: var(--transition);
}

.edit-button:hover, .refresh-button:hover {
  background-color: #3fc5f0;
}

.save-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 8px;
  border-radius: 10px;
  font-size: 11px;
  border: 1px solid var(--gray-light);
  background-color: #3fc5f0;
  color: white;
  cursor: pointer;
  transition: var(--transition);
}

.save-button:hover {
  font-size: 11.5px;
}

.explore-button {
  background-color: var(--primary);
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.explore-button:hover {
  background-color: var(--primary-dark);
}

/* Form Styles */
.edit-profile-form {
  padding: 20px;
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
  flex: 1;
}

.form-group label {
  font-size: 11px;
  color: #9ba6a5;
  text-align: start;
  background-color: #f8fafc;
}

.form-input, .form-textarea {
  padding: 10px 12px;
  border: 1px solid #4444;
  border-radius: 10PX;
  font-size: 11px;
  color: #4444;
  background-color: transparent;
  transition: var(--transition);
  font-weight: lighter;
}

.form-input:focus, .form-textarea:focus {
  border-color: #3fc5f0;
  outline: none;
  box-shadow: 0 0 0 0px #3fc5f0;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

/* File Upload */
.file-upload-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border: 1px dashed var(--gray);
  border-radius: var(--radius-sm);
  background-color: #f8fafc;
  cursor: pointer;
  position: relative;
  transition: var(--transition);
  margin-top: 10px;
  font-size: 11px;
}

.file-upload-wrapper:hover {
  border-color: var(--primary-light);
  background-color: #3fc5f0;
  border-radius: 10px;
}

.file-upload-wrapper input[type="file"] {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

/* Profile Details Grid */
.profile-details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 20px;
  width: 73%;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 2px;
  margin-left: 9px;
}

.detail-icon {
  color: var(--gray);
  flex-shrink: 0;
  margin-top: 2px;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 14px;
  color: #9ba6a5;
  text-align: start;
}

.detail-value {
  font-size: 13px;
  color: var(--dark);
  font-weight: lighter;
}

/* Bio Section */
.bio-section {
  padding: 0 20px 20px;
  border-top: 1px solid var(--gray-light);
  margin-top: 10px;
}

.bio-heading {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 500;
  color: var(--gray-dark);
  margin: 16px 0 8px;
}

.bio-content {
  font-size: 15px;
  line-height: 1.6;
  color: var(--dark);
}

/* Activity Table */
.activity-table-wrapper {
  padding: 0 20px 20px;
  overflow-x: auto;
}

.activity-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.activity-table th, .activity-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--gray-light);
}

.activity-table th {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-dark);
  background-color: #f8fafc;
  white-space: nowrap;
}

.activity-table th svg {
  margin-right: 6px;
  vertical-align: -3px;
}

.activity-table td {
  font-size: 14px;
  color: var(--dark);
}

.transaction-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.buy-badge {
  background-color: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.sell-badge {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--danger);
}

.amount-buy {
  color: var(--success);
  font-weight: 500;
}

.amount-sell {
  color: var(--danger);
  font-weight: 500;
}

/* Empty Activity State */
.empty-activity {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
}

.empty-activity svg {
  color: var(--gray-light);
  margin-bottom: 16px;
}

.empty-activity p {
  color: var(--gray-dark);
  margin-bottom: 16px;
  font-size: 15px;
}

/* Organization Card */
.organization-card {
  margin-bottom: 24px;
}

.plan-badge {
  background-color: #A1F480;
  color: white;
  padding: 9px 35px;
  border-radius: 10px;
  font-size: 10px;
  text-transform: uppercase;
}

.org-details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 20px;
  width: 73%;
}

.org-detail-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.org-name {
  font-weight: 600;
}

.status-value {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-active .status-indicator {
  background-color: #4ef037;
}

.status-pending .status-indicator {
  background-color: var(--warning);
}

.status-inactive .status-indicator {
  background-color: var(--danger);
}

.website-link {
  color: var(--primary);
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
}

.website-link:hover {
  text-decoration: underline;
}

.no-website {
  color: var(--gray);
  font-style: italic;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .profile-details-grid, .org-details-grid {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    flex-direction: column;
  }
}

.detail-value-bio {
  font-size: 12px;
  font-weight: lighter;
  border-radius: 10px;
  color: #444;
}

.members-select {
  background-color: transparent;
  color: #4444;
  padding: 10px;
  font-size: 11px;
  border: none;
}
</style>