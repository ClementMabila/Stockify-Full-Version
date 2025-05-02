import { reactive, ref } from 'vue';
import { getMessageContacts, getConversation, sendMessage } from '../services/messaging';

// State setup
const state = reactive({
  contacts: [],
  activeConversation: {
    userId: null,
    userDetails: null,
    messages: [],
    loading: false
  },
  loadingContacts: false,
  error: null
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
      
      const response = await getMessageContacts();
      state.contacts = response.contacts;
      
      return response.contacts;
    } catch (error) {
      state.error = 'Failed to load contacts: ' + error.message;
      console.error(error);
    } finally {
      state.loadingContacts = false;
    }
  }
  
  // Load conversation with specific user
  async function loadConversation(userId) {
    try {
      state.activeConversation.loading = true;
      state.activeConversation.userId = userId;
      state.error = null;
      
      const response = await getConversation(userId);
      
      // Update active conversation
      state.activeConversation.messages = response.messages;
      state.activeConversation.userDetails = response.user;
      
      // Update unread count in contacts list
      const contactIndex = state.contacts.findIndex(c => c.id === parseInt(userId));
      if (contactIndex >= 0) {
        state.contacts[contactIndex].unread_count = 0;
      }
      
      return response;
    } catch (error) {
      state.error = 'Failed to load conversation: ' + error.message;
      console.error(error);
    } finally {
      state.activeConversation.loading = false;
    }
  }
  
  // Send message to user
  async function sendMessageToUser(userId, messageText) {
    try {
      state.error = null;
      
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
      
      return response.message;
    } catch (error) {
      state.error = 'Failed to send message: ' + error.message;
      console.error(error);
      throw error;
    }
  }
  
  // Start polling for new messages
  function startPolling() {
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