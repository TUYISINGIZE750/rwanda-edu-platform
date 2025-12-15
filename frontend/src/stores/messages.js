import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../utils/api'
import { saveMessages, getMessages } from '../utils/indexeddb'

export const useMessagesStore = defineStore('messages', () => {
  const messages = ref({})
  const ws = ref(null)
  
  async function fetchChannelMessages(channelId) {
    try {
      const response = await api.get(`/messages/channel/${channelId}`)
      messages.value[channelId] = response.data
      await saveMessages(channelId, response.data)
    } catch (error) {
      // Fallback to offline cache
      const cached = await getMessages(channelId)
      if (cached) messages.value[channelId] = cached
    }
  }
  
  function connectWebSocket(channelId) {
    const wsUrl = `${import.meta.env.VITE_WS_URL}/ws/channels/${channelId}`
    ws.value = new WebSocket(wsUrl)
    
    ws.value.onmessage = (event) => {
      const message = JSON.parse(event.data)
      if (!messages.value[channelId]) messages.value[channelId] = []
      messages.value[channelId].unshift(message)
    }
  }
  
  async function sendMessage(channelId, content, attachments = []) {
    const response = await api.post('/messages/', {
      channel_id: channelId,
      content,
      attachments
    })
    return response.data
  }
  
  return { messages, fetchChannelMessages, connectWebSocket, sendMessage }
})
