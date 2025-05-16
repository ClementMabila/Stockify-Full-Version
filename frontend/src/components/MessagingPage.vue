<template>
    <div class="messaging-container">
      <!-- Sidebar with contacts -->
      <div class="contacts-sidebar">
        <div class="header">
          <h2><span class="heading-span">Stockify</span> Messager</h2>
          <div class="search-box">
            <input type="text" placeholder="Search inbox" v-model="searchQuery" />
            <i class="fas fa-search"></i>
          </div>
        </div>
        
        <div class="contacts-list" v-if="!messaging.state.loadingContacts">
          <div
            v-for="contact in filteredContacts"
            :key="contact.id"
            class="contact-item"
            :class="{ 'active': activeContactId === contact.id }"
            @click="selectContact(contact.id)"
          >
            <div class="avatar-container">
              <div v-if="contact.avatar">
              <img :src="contact.avatar" alt="Profile Avatar" class="avatar">
            </div>
            <div v-else class="avatar-placeholder">
              <img src="../assets/images/speech-bub.png" alt="contact.full_name" class="avatar">
            </div>
              <span class="status-indicator" :class="{ 'online': contact.is_online }"></span>
            </div>
            
            <div class="contact-info">
              <div class="contact-header">
                <h3>{{ contact.full_name }}</h3>
                <span class="last-message-time">{{ formatTime(contact.last_message_time) }}</span>
              </div>
              <div class="last-message-container">
                <p class="last-message">{{ contact.last_message || 'No messages yet' }}</p>
                <span v-if="contact.unread_count > 0" class="unread-badge">{{ contact.unread_count }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading contacts...</p>
        </div>
      </div>
      
      <!-- Conversation area -->
      <div class="conversation-area" v-if="activeContactId">
        <!-- Conversation header -->
        <div class="conversation-header">
          <div class="contact-profile">
            <div class="status-top">
              <h3>{{ messaging.state.activeConversation.userDetails?.full_name }}</h3>
              <p class="status">
                {{ messaging.state.activeConversation.userDetails?.is_online ? 'Online' : 'Offline' }}
              </p>
            </div>
          </div>
          <div class="conversation-actions">
            <button class="action-button">
              <i class="fas fa-phone"></i>
            </button>
            <button class="action-button">
              <i class="fas fa-video"></i>
            </button>
            <button class="action-button">
              <i class="fas fa-ellipsis-v"></i>
            </button>
          </div>
        </div>
        
        <!-- Messages -->
        <div class="messages-container" ref="messagesContainer">
          <div v-if="messaging.state.activeConversation.loading" class="loading-messages">
            <div class="loading-spinner"></div>
            <p>Loading conversation...</p>
          </div>
          
          <template v-else>
            <div class="date-separator" v-if="messaging.state.activeConversation.messages.length > 0">
              {{ formatDate(messaging.state.activeConversation.messages[0].timestamp) }}
            </div>
            
            <div
              v-for="(message, index) in messaging.state.activeConversation.messages"
              :key="message.id"
              class="message"
              :class="{ 'my-message': message.is_mine, 'other-message': !message.is_mine }"
            >
              <div class="message-content">
                <p>{{ message.message }}</p>
                <div class="message-meta">
                  <span class="time">{{ formatMessageTime(message.timestamp) }}</span>
                  <span v-if="message.is_mine" class="read-status">
                    <i class="fas" :class="message.is_read ? 'fa-check-double' : 'fa-check'"></i>
                  </span>
                </div>
              </div>
              
              <!-- Show date separator when day changes -->
              <div class="date-separator" v-if="shouldShowDateSeparator(index)">
                {{ formatDate(messaging.state.activeConversation.messages[index + 1].timestamp) }}
              </div>
            </div>
          </template>
        </div>
        
        <!-- Message input -->
        <div class="message-input-container">
          <button class="attachment-button">
            <i class="fas fa-paperclip"></i>
          </button>
          <textarea
            v-model="newMessage"
            placeholder="Type a message..."
            @keyup.enter="sendMessage"
            @input="adjustTextareaHeight"
            ref="messageInput"
            rows="1"
          ></textarea>
          <button 
            class="send-button" 
            :disabled="!newMessage.trim()" 
            @click="sendMessage"
          >
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
      
      <!-- Empty state when no conversation is selected -->
      <div class="empty-state" v-else>
        <div class="empty-state-content">
          <i class="fas fa-comments empty-icon"></i>
          <h2>Select a <span class="heading-span">conversation</span></h2>
          <p>Choose a contact to start messaging</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue';
  import { useMessaging } from '../store/messaging';
  import { format, isToday, isYesterday, isSameDay } from 'date-fns';
  
  export default {
    name: 'MessagingPage',
    
    setup() {
      const messaging = useMessaging();
      const searchQuery = ref('');
      const activeContactId = ref(null);
      const newMessage = ref('');
      const messagesContainer = ref(null);
      const messageInput = ref(null);
      
      const filteredContacts = computed(() => {
        if (!searchQuery.value) return messaging.state.contacts;
        
        const query = searchQuery.value.toLowerCase();
        return messaging.state.contacts.filter(contact => 
          contact.full_name.toLowerCase().includes(query) || 
          contact.username.toLowerCase().includes(query)
        );
      });
      
      // Format time for contact list
      const formatTime = (timestamp) => {
        if (!timestamp) return '';
        
        const date = new Date(timestamp);
        
        if (isToday(date)) {
          return format(date, 'HH:mm');
        } else if (isYesterday(date)) {
          return 'Yesterday';
        } else {
          return format(date, 'dd/MM/yyyy');
        }
      };
      
      // Format date for message separators
      const formatDate = (timestamp) => {
        if (!timestamp) return '';
        
        const date = new Date(timestamp);
        
        if (isToday(date)) {
          return 'Today';
        } else if (isYesterday(date)) {
          return 'Yesterday';
        } else {
          return format(date, 'EEEE, MMMM d, yyyy');
        }
      };
      
      // Format time for messages
      const formatMessageTime = (timestamp) => {
        if (!timestamp) return '';
        return format(new Date(timestamp), 'HH:mm');
      };
      
      // Check if we should show a date separator between messages
      const shouldShowDateSeparator = (index) => {
        const messages = messaging.state.activeConversation.messages;
        if (index === messages.length - 1) return false;
        
        const currentMsg = messages[index];
        const nextMsg = messages[index + 1];
        
        return !isSameDay(new Date(currentMsg.timestamp), new Date(nextMsg.timestamp));
      };
      
      // Select a contact to start or continue a conversation
      const selectContact = async (contactId) => {
        activeContactId.value = contactId;
        await messaging.loadConversation(contactId);
        
        // Scroll to bottom of messages
        nextTick(() => {
          scrollToBottom();
        });
      };
      
      // Send a new message
      const sendMessage = async () => {
        if (!newMessage.value.trim()) return;
        
        try {
          await messaging.sendMessageToUser(activeContactId.value, newMessage.value);
          newMessage.value = '';
          
          // Reset textarea height
          if (messageInput.value) {
            messageInput.value.style.height = 'auto';
          }
          
          // Scroll to bottom after message is sent
          nextTick(() => {
            scrollToBottom();
          });
        } catch (error) {
          console.error('Failed to send message:', error);
        }
      };
      
      // Auto-grow textarea
      const adjustTextareaHeight = () => {
        const textarea = messageInput.value;
        if (!textarea) return;
        
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;
      };
      
      // Scroll to bottom of messages
      const scrollToBottom = () => {
        const container = messagesContainer.value;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      };
      
      // Start polling for new messages when component mounts
      onMounted(() => {
        messaging.startPolling();
      });
      
      // Stop polling when component unmounts
      onUnmounted(() => {
        messaging.stopPolling();
      });
      
      // Watch for changes in active conversation messages and scroll to bottom
      watch(
        () => messaging.state.activeConversation.messages,
        () => {
          nextTick(() => {
            scrollToBottom();
          });
        },
        { deep: true }
      );
      
      return {
        messaging,
        searchQuery,
        activeContactId,
        filteredContacts,
        newMessage,
        messagesContainer,
        messageInput,
        formatTime,
        formatDate,
        formatMessageTime,
        shouldShowDateSeparator,
        selectContact,
        sendMessage,
        adjustTextareaHeight
      };
    }
  };
  </script>
  
  <style scoped>
  .messaging-container {
    margin-top: -7px;
    display: flex;
    height: calc(100vh - 64px); /* Adjust based on your navbar height */
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin-right: 40px;
    margin-bottom: 50px;
  }
  
  /* Contacts sidebar */
  .contacts-sidebar {
    width: 320px;
    background-color: #ffffff;
    border-right: 1px solid #e9edef;
    display: flex;
    flex-direction: column;
  }
  
  .contacts-sidebar .header {
    padding: 16px;
    border-bottom: 1px solid #e9edef;
  }
  
  .header h2 {
    font-size: 24px;
    font-weight: 600;
    color: #111b21;
    margin-left: -90px;
  }
  .contacts-sidebar h2 {
    font-size: 19px;
    font-weight: 600;
    margin-bottom: 16px;
    color:  Black;
  }
  
  .search-box {
    position: relative;
    margin-bottom: 8px;
  }
  
  .search-box input {
    width: 100%;
    padding: 12px 16px 12px 40px;
    border-radius: 24px;
    border: none;
    background-color: #f0f2f5;
    font-size: 12px;
    outline: none;
  }
  
  .search-box i {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: #54656f;
  }
  
  .contacts-list {
    flex: 1;
    overflow-y: scroll; /* ensure scrolling still works */
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none;  /* IE and Edge */
  }

  .contacts-list::-webkit-scrollbar {
    display: none; /* Chrome, Safari, and Opera */
  }

  .contact-item {
    display: flex;
    padding: 16px;
    cursor: pointer;
    transition: background-color 0.2s;
    border-bottom: 1px solid #f0f2f5;
  }
  
  .contact-item:hover {
    background-color: #f5f6f6;
  }
  
  .contact-item.active {
    background-color: #e9edef;
  }
  
  .avatar-container {
    position: relative;
    margin-right: 16px;
  }
  
  .avatar {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #e9edef;
    padding: 2px;
  }
  
  .status-indicator {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: #b9b9b9;
    border: 2px solid #ffffff;
  }
  
  .status-indicator.online {
    background-color: #25d366;
  }
  
  .contact-info {
    flex: 1;
    min-width: 0; /* Important for text ellipsis to work */
  }
  
  .contact-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
  }
  
  .contact-header h3 {
    font-size: 13px;
    font-weight: bold;
    color: #111b21;
    margin: 0;
    white-space: nowrap;
  }
  
  .last-message-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .last-message {
    margin: 0;
    font-size: 12px;
    color: #667781;
    white-space: nowrap;
    /* Removed misplaced CSS property */
    max-width: 200px;
  }
  
  .unread-badge {
    background-color: #25d366;
    color: white;
    font-size: 12px;
    font-weight: 600;
    min-width: 20px;
    height: 20px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 6px;
  }
  
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #667781;
  }
  
  .loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #f0f2f5;
    border-top: 3px solid #128c7e;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* Conversation area */
  .conversation-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: white;
    width: 710px;
  }
  
  .conversation-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    background-color: white;
    border-bottom: 1px solid #e9edef;
    width: 710px;
    border-radius: 0px 10px 0px 0px;
  }

  .conversation-header h3 {
    font-size: 11px;
  }
  
  .contact-profile {
    display: flex;
    align-items: center;
  }
  
  .contact-profile .avatar {
    width: 40px;
    height: 40px;
    margin-right: 16px;
  }
  
  .contact-profile h3 {
    margin: 0;
    font-size: 12px;
    font-weight: bold;
  }
  
  .status {
    margin: 0;
    font-size: 11px;
    color: #667781;
    margin-left: 10px;
  }
  
  .conversation-actions {
    display: flex;
  }
  
  .action-button {
    background: none;
    border: none;
    color: #54656f;
    font-size: 18px;
    padding: 8px;
    margin-left: 8px;
    border-radius: 50%;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .action-button:hover {
    background-color: #e9edef;
  }
  
  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    background-color: white;
    width: 710px;
  }
  
  .loading-messages {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #667781;
  }
  
  .date-separator {
    text-align: center;
    font-size: 12px;
    color: #54656f;
    background-color: rgba(225, 245, 254, 0.92);
    border-radius: 7px;
    padding: 5px 12px;
    margin: 16px auto;
    display: inline-block;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
  }
  
  .message {
    margin-bottom: 8px;
    display: flex;
    flex-direction: column;
  }
  
  .message-content {
    padding: 8px 12px;
    border-radius: 7.5px;
    position: relative;
    box-shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13);
    width: 200px;
    text-align: start;
  }
  
  .my-message .message-content {
    background: linear-gradient(120deg, #dcb5ff, #ffcccc);
    align-self: flex-end;
    border-top-right-radius: 0;
  }
  
  .other-message .message-content {
    background-color: #f9f5f0;
    align-self: flex-start;
    border-top-left-radius: 0;
  }
  
  .message-content p {
    margin: 0 0 5px;
    font-size: 12px;
    line-height: 1.4;
    color: #4444;
    word-wrap: break-word;
  }
  
  .message-meta {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    font-size: 11px;
    color: #667781;
  }
  
  .time {
    margin-right: 4px;
  }
  
  .read-status i.fa-check {
    color: #667781;
  }
  
  .read-status i.fa-check-double {
    color: #53bdeb;
  }
  
  .message-input-container {
    display: flex;
    align-items: center;
    background-color: white;
    padding: 10px 16px;
  }
  
  .attachment-button {
    background: none;
    border: none;
    color: #54656f;
    font-size: 20px;
    padding: 8px;
    margin-right: 8px;
    cursor: pointer;
  }
  
  textarea {
    flex: 1;
    border: none;
    border-radius: 21px;
    padding: 9px 12px;
    font-size: 12px;
    max-height: 100px;
    resize: none;
    outline: none;
    font-family: inherit;
    background-color: #70707044;
  }
  
  .send-button {
    background: none;
    border: none;
    color: #54656f;
    font-size: 20px;
    padding: 8px;
    margin-left: 8px;
    cursor: pointer;
    transition: color 0.2s;
  }
  
  .send-button:disabled {
    color: #b3b3b3;
    cursor: default;
  }
  
  .send-button:not(:disabled):hover {
    color: #128c7e;
  }
  
  /* Empty state */
  .empty-state {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f8f9fa;
    width: 1100px;
    margin-right: 30px;
  }
  
  .empty-state-content {
    text-align: center;
    max-width: 340px;
    padding: 20px;
  }
  
  .empty-icon {
    font-size: 72px;
    color: #128c7e;
    margin-bottom: 16px;
  }
  
  .empty-state h2 {
    font-size: 32px;
    font-weight: 300;
    color: #41525d;
    margin-bottom: 16px;
  }
  
  .empty-state p {
    font-size: 14px;
    color: #667781;
  }
  
  /* Media query for smaller screens */
  @media (max-width: 768px) {
    .messaging-container {
      flex-direction: column;
    }
    
    .contacts-sidebar {
      width: 100%;
      height: 100%;
      position: absolute;
      z-index: 2;
      transform: translateX(-100%);
      transition: transform 0.3s ease;
    }
    
    .contacts-sidebar.open {
      transform: translateX(0);
    }
    
    .conversation-area {
      width: 100%;
    }
    
    .message-content {
      max-width: 80%;
    }
  }
  /* Removed misplaced CSS property */
  
  .last-message-time {
    font-size: 12px;
    color: #667781;
    white-space: nowrap;
  }
  
  /* Fix for any container overflows */
  .contact-info {
    width: calc(100% - 64px);
  }
  
  /* Additional responsive styling */
  @media (max-width: 576px) {
    .contacts-sidebar {
      width: 100%;
    }
    
    .conversation-area {
      display: none;
    }
    
    .conversation-area.active {
      display: flex;
    }
    
    .back-button {
      display: block;
    }
  }
  
  /* Add mobile navigation button */
  .mobile-nav-button {
    display: none;
  }
  
  @media (max-width: 576px) {
    .mobile-nav-button {
      display: block;
      position: absolute;
      top: 16px;
      left: 16px;
      background: #128c7e;
      color: white;
      border: none;
      border-radius: 50%;
      width: 40px;
      height: 40px;
      z-index: 3;
    }
  }

  .status-top {
    display: flex;
  }

  .heading-span {
    background: linear-gradient(120deg, #dcb5ff, #ffcccc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
</style>