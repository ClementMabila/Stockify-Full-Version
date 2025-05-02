<template>
  <div class="profile-container">
    <!-- Profile Header with gradient background -->
    <div class="header-section bg-gradient-to-r from-blue-600 to-indigo-800 text-white p-6 rounded-lg shadow-lg mb-6">
      <div class="flex flex-col md:flex-row items-center">
        <div class="avatar-container mb-4 md:mb-0 md:mr-6">
          <div v-if="userProfile.avatar" class="avatar-image">
            <img :src="userProfile.avatar" alt="Profile Avatar" class="rounded-full h-24 w-24 object-cover border-4 border-white shadow-md">
          </div>
          <div v-else class="avatar-placeholder bg-white bg-opacity-20 rounded-full h-24 w-24 flex items-center justify-center border-4 border-white shadow-md">
            <span class="text-3xl font-semibold">{{ userInitials }}</span>
          </div>
        </div>
        <div class="user-info text-center md:text-left">
          <h1 class="text-2xl font-bold">{{ user.first_name }} {{ user.last_name }}</h1>
          <div class="role-badge inline-block px-3 py-1 rounded-full bg-blue-500 bg-opacity-40 text-white text-sm font-medium mt-2">
            {{ userProfile.role }}
          </div>
          <p class="text-blue-100 mt-2">{{ userProfile.organization.name }}</p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Profile Information -->
      <div class="col-span-1 lg:col-span-2">
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-800">Profile Information</h2>
            <button @click="editMode = !editMode" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md flex items-center">
              <i class="fas fa-edit mr-2"></i> 
              {{ editMode ? 'Cancel' : 'Edit Profile' }}
            </button>
          </div>
          
          <form v-if="editMode" @submit.prevent="updateProfile" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="form-group">
                <label class="block text-gray-700 mb-1">First Name</label>
                <input v-model="editForm.first_name" type="text" class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
              </div>
              <div class="form-group">
                <label class="block text-gray-700 mb-1">Last Name</label>
                <input v-model="editForm.last_name" type="text" class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
              </div>
            </div>
            
            <div class="form-group">
              <label class="block text-gray-700 mb-1">Email</label>
              <input v-model="editForm.email" type="email" class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            
            <div class="form-group">
              <label class="block text-gray-700 mb-1">Bio</label>
              <textarea v-model="editForm.bio" rows="3" class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
            </div>
            
            <div class="form-group">
              <label class="block text-gray-700 mb-1">Location</label>
              <input v-model="editForm.location" type="text" class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            
            <div class="form-group">
              <label class="block text-gray-700 mb-1">Avatar</label>
              <input type="file" @change="handleAvatarChange" accept="image/*" class="w-full px-4 py-2 border rounded-md">
            </div>
            
            <div class="flex justify-end">
              <button type="submit" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-md">
                Save Changes
              </button>
            </div>
          </form>
          
          <div v-else class="user-details">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="detail-item">
                <p class="text-gray-500 text-sm">Email</p>
                <p class="text-gray-800">{{ user.email }}</p>
              </div>
              <div class="detail-item">
                <p class="text-gray-500 text-sm">Location</p>
                <p class="text-gray-800">{{ userProfile.location || 'Not specified' }}</p>
              </div>
              <div class="detail-item">
                <p class="text-gray-500 text-sm">Role</p>
                <p class="text-gray-800">{{ userProfile.role }}</p>
              </div>
              <div class="detail-item">
                <p class="text-gray-500 text-sm">Member Since</p>
                <p class="text-gray-800">{{ formatDate(user.date_joined) }}</p>
              </div>
            </div>
            
            <div class="mt-6">
              <p class="text-gray-500 text-sm">Bio</p>
              <p class="text-gray-800 mt-1">{{ userProfile.bio || 'No bio available' }}</p>
            </div>
          </div>
        </div>
        
        <!-- Recent Activity -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Recent Activity</h2>
          <div v-if="stockHistory.length > 0" class="overflow-x-auto">
            <table class="w-full text-left">
              <thead>
                <tr class="border-b">
                  <th class="py-3 px-2">Date</th>
                  <th class="py-3 px-2">Action</th>
                  <th class="py-3 px-2">Stock</th>
                  <th class="py-3 px-2">Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(activity, index) in stockHistory.slice(0, 5)" :key="index" class="border-b hover:bg-gray-50">
                  <td class="py-3 px-2">{{ formatDate(activity.transaction_date) }}</td>
                  <td class="py-3 px-2">{{ activity.transaction_type }}</td>
                  <td class="py-3 px-2">{{ activity.stock_name }}</td>
                  <td class="py-3 px-2" :class="activity.transaction_type === 'BUY' ? 'text-green-600' : 'text-red-600'">
                    {{ activity.transaction_type === 'BUY' ? '+' : '-' }}${{ activity.amount.toFixed(2) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center text-gray-500 py-6">
            No recent activity to display
          </div>
        </div>
      </div>

      <!-- Organization and Messaging Sidebar -->
      <div class="col-span-1">
        <!-- Organization Info Card -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold text-gray-800">Organization</h2>
            <div class="plan-badge px-3 py-1 rounded-full bg-indigo-100 text-indigo-800 text-sm font-medium">
              {{ userProfile.organization.subscription_plan }}
            </div>
          </div>
          
          <div class="org-logo mb-4 flex justify-center">
            <img v-if="userProfile.organization.logo" :src="userProfile.organization.logo" alt="Organization Logo" class="h-16 rounded">
            <div v-else class="h-16 w-16 bg-gray-200 rounded flex items-center justify-center text-gray-500">
              <i class="fas fa-building text-2xl"></i>
            </div>
          </div>
          
          <div class="org-details space-y-2">
            <div class="detail-item">
              <p class="text-gray-500 text-sm">Name</p>
              <p class="text-gray-800 font-medium">{{ userProfile.organization.name }}</p>
            </div>
            <div class="detail-item">
              <p class="text-gray-500 text-sm">Status</p>
              <p :class="`text-${getStatusColor(userProfile.organization.status)}-600 font-medium`">
                {{ userProfile.organization.status }}
              </p>
            </div>
            <div class="detail-item">
              <p class="text-gray-500 text-sm">Established</p>
              <p class="text-gray-800">{{ formatDate(userProfile.organization.date_established) }}</p>
            </div>
            <div class="detail-item">
              <p class="text-gray-500 text-sm">Website</p>
              <a v-if="userProfile.organization.website" :href="userProfile.organization.website" target="_blank" class="text-blue-600 hover:underline">
                {{ userProfile.organization.website }}
              </a>
              <p v-else class="text-gray-500">Not available</p>
            </div>
          </div>
        </div>
        
        <!-- Messages -->
        <div class="bg-white rounded-lg shadow-md p-6" v-if="canSendMessages">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Messages</h2>
          
          <div v-if="messages.length > 0" class="messages space-y-4 max-h-80 overflow-y-auto mb-4">
            <div v-for="(message, index) in messages.slice(0, 5)" :key="index" 
                 class="message p-3 rounded-lg" 
                 :class="message.sender.id === user.id ? 'bg-blue-50 ml-4' : 'bg-gray-50 mr-4'">
              <div class="flex justify-between mb-1">
                <span class="font-medium text-sm">
                  {{ message.sender.id === user.id ? 'You' : message.sender.first_name }}
                </span>
                <span class="text-xs text-gray-500">{{ formatTime(message.timestamp) }}</span>
              </div>
              <p class="text-gray-700">{{ message.message }}</p>
            </div>
          </div>
          <div v-else class="text-center text-gray-500 py-4 mb-4">
            No messages yet
          </div>
          
          <div class="new-message">
            <textarea 
              v-model="newMessage" 
              placeholder="Type a message..." 
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows="2"
            ></textarea>
            <div class="flex justify-between items-center mt-2">
              <select v-model="selectedReceiver" class="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option disabled value="">Select recipient</option>
                <option v-for="member in organizationMembers" :key="member.id" :value="member.id">
                  {{ member.first_name }} {{ member.last_name }} ({{ member.role }})
                </option>
              </select>
              <button 
                @click="sendMessage" 
                :disabled="!newMessage || !selectedReceiver" 
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md disabled:bg-gray-400">
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import http from '../services/http';

export default {
  name: 'UserProfile',
  
  setup() {
    // User data
    const user = ref({});
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
        website: ''
      }
    });
    
    // Form and UI state
    const editMode = ref(false);
    const editForm = ref({
      first_name: '',
      last_name: '',
      email: '',
      bio: '',
      location: '',
      avatar: null
    });
    
    // Activity and messages
    const stockHistory = ref([]);
    const messages = ref([]);
    const newMessage = ref('');
    const selectedReceiver = ref('');
    const organizationMembers = ref([]);
    
    // Computed properties
    const userInitials = computed(() => {
      if (user.value.first_name && user.value.last_name) {
        return `${user.value.first_name[0]}${user.value.last_name[0]}`;
      }
      return user.value.username ? user.value.username[0].toUpperCase() : '?';
    });
    
    const canSendMessages = computed(() => {
      return ['Admin', 'Investor'].includes(userProfile.value.role);
    });
    
    // Methods
    const fetchUserData = async () => {
      try {
        const userData = await http.get('/api/user/profile/');
        user.value = userData.user;
        userProfile.value = userData.profile;
        
        // Initialize edit form with current values
        editForm.value = {
          first_name: userData.user.first_name,
          last_name: userData.user.last_name,
          email: userData.user.email,
          bio: userData.profile.bio,
          location: userData.profile.location,
          avatar: null
        };
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      }
    };
    
    const fetchStockHistory = async () => {
      try {
        const history = await http.get('/api/stock-history/');
        stockHistory.value = history.results || [];
      } catch (error) {
        console.error('Failed to fetch stock history:', error);
      }
    };
    
    const fetchMessages = async () => {
      try {
        const messagesData = await http.get('/api/messages/');
        messages.value = messagesData.results || [];
      } catch (error) {
        console.error('Failed to fetch messages:', error);
      }
    };
    
    const fetchOrganizationMembers = async () => {
      try {
        const membersData = await http.get('/api/organization/members/');
        organizationMembers.value = membersData.results || [];
      } catch (error) {
        console.error('Failed to fetch organization members:', error);
      }
    };
    
    const updateProfile = async () => {
      try {
        const formData = new FormData();
        formData.append('first_name', editForm.value.first_name);
        formData.append('last_name', editForm.value.last_name);
        formData.append('email', editForm.value.email);
        formData.append('bio', editForm.value.bio);
        formData.append('location', editForm.value.location);
        
        if (editForm.value.avatar) {
          formData.append('avatar', editForm.value.avatar);
        }
        
        const response = await fetch(`http://localhost:8000/api/user/profile/update/`, {
          method: 'PATCH',
          headers: {
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
          body: formData
        });
        
        if (!response.ok) throw new Error(await response.text());
        
        // Refresh user data
        await fetchUserData();
        editMode.value = false;
      } catch (error) {
        console.error('Failed to update profile:', error);
      }
    };
    
    const handleAvatarChange = (event) => {
      editForm.value.avatar = event.target.files[0];
    };
    
    const sendMessage = async () => {
      if (!newMessage.value || !selectedReceiver.value) return;
      
      try {
        await http.post('/api/messages/', {
          receiver_id: selectedReceiver.value,
          message: newMessage.value
        });
        
        // Reset form and refresh messages
        newMessage.value = '';
        selectedReceiver.value = '';
        await fetchMessages();
      } catch (error) {
        console.error('Failed to send message:', error);
      }
    };
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      }).format(date);
    };
    
    const formatTime = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', { 
        hour: '2-digit', 
        minute: '2-digit'
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
    
    // Lifecycle hooks
    onMounted(async () => {
      await fetchUserData();
      await fetchStockHistory();
      
      if (canSendMessages.value) {
        await fetchMessages();
        await fetchOrganizationMembers();
      }
    });
    
    return {
      user,
      userProfile,
      userInitials,
      editMode,
      editForm,
      stockHistory,
      messages,
      newMessage,
      selectedReceiver,
      organizationMembers,
      canSendMessages,
      formatDate,
      formatTime,
      updateProfile,
      handleAvatarChange,
      sendMessage,
      getStatusColor
    };
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem;
}

.header-section {
  background-image: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
}

.messages::-webkit-scrollbar {
  width: 8px;
}

.messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.messages::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 10px;
}

.messages::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}
</style>