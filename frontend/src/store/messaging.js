import { reactive, ref } from 'vue';
import { getMessageContacts, getConversation, sendMessage } from '../services/messaging';

const state = reactive({
  contacts: [],
  activeConversation: {
    userId: null,
    userDetails: null,
    messages: [],
    loading: false
  },
  loadingContacts: false,
  error: null,
  lastErrorDetails: null  // Added to store full error details
});

// Poll interval for refreshing contacts (in milliseconds)
const POLL_INTERVAL = 10000;
let pollTimer = null;

export function useMessaging() {
  // Load all contacts with conversations
  async function loadContacts() {
    try {
      state.loadingContacts = true;
      state.error = null;
      state.lastErrorDetails = null;
      
      const response = await getMessageContacts();
      state.contacts = response.contacts;
      
      return response.contacts;
    } catch (error) {
      state.error = 'Failed to load contacts: ' + error.message;
      state.lastErrorDetails = error;
      console.error('Contact loading error:', error);
      
      // If polling is active and we hit several errors, maybe slow down or pause
      handlePollingErrors();
    } finally {
      state.loadingContacts = false;
    }
  }
  
  let consecutiveErrors = 0;
  
  function handlePollingErrors() {
    consecutiveErrors++;
    
    if (consecutiveErrors >= 3) {
      console.warn('Too many consecutive errors, pausing polling for 1 minute');
      stopPolling();
      
      setTimeout(() => {
        consecutiveErrors = 0;
        startPolling();
      }, 60000);
    }
  }

  async function loadConversation(userId) {
    try {
      state.activeConversation.loading = true;
      state.activeConversation.userId = userId;
      state.error = null;
      state.lastErrorDetails = null;
      
      const response = await getConversation(userId);

      state.activeConversation.messages = response.messages;
      state.activeConversation.userDetails = response.user;

      const contactIndex = state.contacts.findIndex(c => c.id === parseInt(userId));
      if (contactIndex >= 0) {
        state.contacts[contactIndex].unread_count = 0;
      }

      consecutiveErrors = 0;
      
      return response;
    } catch (error) {
      state.error = 'Failed to load conversation: ' + error.message;
      state.lastErrorDetails = error;
      console.error('Conversation loading error:', error);
    } finally {
      state.activeConversation.loading = false;
    }
  }
  
  // Send message to user
  async function sendMessageToUser(userId, messageText) {
    try {
      state.error = null;
      state.lastErrorDetails = null;
      
      const response = await sendMessage(userId, messageText);
      
      // Update the active conversation with the new message
      if (state.activeConversation.userId === userId) {
        state.activeConversation.messages.push(response.message);
      }
      
      // Update the contacts list with the new last message
      const contactIndex = state.contacts.findIndex(c => c.id === parseInt(userId));
      if (contactIndex >= 0) {
        state.contacts[contactIndex].last_message = messageText.length > 50 ? 
          messageText.substring(0, 50) + '...' : messageText;
        state.contacts[contactIndex].last_message_time = response.message.timestamp;
        
        // Move this contact to the top of the list
        const updatedContact = state.contacts.splice(contactIndex, 1)[0];
        state.contacts.unshift(updatedContact);
      }
      
      // Reset error counter when successful
      consecutiveErrors = 0;
      
      return response.message;
    } catch (error) {
      state.error = 'Failed to send message: ' + error.message;
      state.lastErrorDetails = error;
      console.error('Message sending error:', error);
      throw error;
    }
  }
  
  // Check if user is authenticated before polling
  function checkAuthBeforePolling() {
    // Get auth token or check auth status - adjust based on your auth system
    const token = localStorage.getItem('authToken');
    if (!token) {
      console.warn('User not authenticated. Not starting polling.');
      state.error = 'Authentication required to access messages';
      return false;
    }
    return true;
  }
  
  // Start polling for new messages
  function startPolling() {
    if (!checkAuthBeforePolling()) return;
    
    if (pollTimer) clearInterval(pollTimer);
    
    // Immediately load contacts
    loadContacts();
    
    // Set up polling
    pollTimer = setInterval(() => {
      loadContacts();
      
      // If there's an active conversation, refresh it
      if (state.activeConversation.userId) {
        loadConversation(state.activeConversation.userId);
      }
    }, POLL_INTERVAL);
  }
  
  // Stop polling
  function stopPolling() {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  }
  
  return {
    state,
    loadContacts,
    loadConversation,
    sendMessageToUser,
    startPolling,
    stopPolling
  };
}