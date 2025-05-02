import http from './http';

export async function getMessageContacts() {
  try {
    const response = await http.get('/api/messages/contacts/');
    return response;
  } catch (error) {
    console.error('Failed to fetch message contacts:', error);
    throw error;
  }
}

export async function getConversation(userId) {
  try {
    const response = await http.get(`/api/messages/conversation/${userId}/`);
    return response;
  } catch (error) {
    console.error('Failed to fetch conversation:', error);
    throw error;
  }
}

export async function sendMessage(userId, message) {
  try {
    const response = await http.post(`/api/messages/send/${userId}/`, { message });
    return response;
  } catch (error) {
    console.error('Failed to send message:', error);
    throw error;
  }
}