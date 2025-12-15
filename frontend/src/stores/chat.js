import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import io from 'socket.io-client'
import api from '../utils/api'

export const useChatStore = defineStore('chat', () => {
  const socket = ref(null)
  const messages = ref([])
  const channels = ref([])
  const activeChannel = ref(null)
  const onlineUsers = ref([])
  const typingUsers = ref([])
  const isConnected = ref(false)
  const isTyping = ref(false)
  const lastSeen = ref({})

  // Computed
  const sortedMessages = computed(() => {
    return [...messages.value].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
  })

  const unreadCount = computed(() => {
    return messages.value.filter(msg => !msg.read && msg.sender_id !== getCurrentUserId()).length
  })

  // Socket connection
  function connectSocket(token) {
    if (socket.value) return

    socket.value = io(import.meta.env.VITE_API_URL || 'http://localhost:3000', {
      auth: { token },
      transports: ['websocket', 'polling']
    })

    socket.value.on('connect', () => {
      isConnected.value = true
      console.log('Connected to chat server')
    })

    socket.value.on('disconnect', () => {
      isConnected.value = false
      console.log('Disconnected from chat server')
    })

    socket.value.on('message', (message) => {
      addMessage(message)
    })

    socket.value.on('user_typing', (data) => {
      handleUserTyping(data)
    })

    socket.value.on('user_stopped_typing', (data) => {
      handleUserStoppedTyping(data)
    })

    socket.value.on('user_online', (userId) => {
      if (!onlineUsers.value.includes(userId)) {
        onlineUsers.value.push(userId)
      }
    })

    socket.value.on('user_offline', (userId) => {
      onlineUsers.value = onlineUsers.value.filter(id => id !== userId)
    })

    socket.value.on('message_read', (data) => {
      markMessageAsRead(data.messageId, data.userId)
    })
  }

  function disconnectSocket() {
    if (socket.value) {
      socket.value.disconnect()
      socket.value = null
      isConnected.value = false
    }
  }

  // Channel management
  async function joinChannel(channelId) {
    try {
      activeChannel.value = channelId
      if (socket.value) {
        socket.value.emit('join_channel', channelId)
      }
      await loadChannelMessages(channelId)
    } catch (error) {
      console.error('Failed to join channel:', error)
    }
  }

  function leaveChannel() {
    if (socket.value && activeChannel.value) {
      socket.value.emit('leave_channel', activeChannel.value)
    }
    activeChannel.value = null
    messages.value = []
  }

  // Message management
  async function loadChannelMessages(channelId, page = 1, limit = 50) {
    try {
      const response = await api.get(`/chat/channels/${channelId}/messages`, {
        params: { page, limit }
      })
      
      // API returns array directly, not wrapped in messages key
      const messagesData = Array.isArray(response.data) ? response.data : []
      
      if (page === 1) {
        messages.value = messagesData
      } else {
        messages.value = [...messagesData, ...messages.value]
      }
      
      return { messages: messagesData, hasMore: messagesData.length === limit }
    } catch (error) {
      console.error('Failed to load messages:', error)
      return { messages: [], hasMore: false }
    }
  }

  function addMessage(message) {
    const existingIndex = messages.value.findIndex(m => m.id === message.id)
    if (existingIndex >= 0) {
      messages.value[existingIndex] = message
    } else {
      messages.value.push(message)
    }
  }

  async function sendMessage(content, type = 'text', attachments = []) {
    if (!activeChannel.value) {
      console.error('No active channel')
      throw new Error('No active channel selected')
    }

    console.log('sendMessage called:', { content, type, channel: activeChannel.value })

    const tempId = Date.now().toString()
    const tempMessage = {
      id: tempId,
      content,
      type,
      attachments,
      sender_id: getCurrentUserId(),
      sender: { id: getCurrentUserId(), name: 'You' },
      channel_id: activeChannel.value,
      created_at: new Date().toISOString(),
      status: 'sending'
    }

    addMessage(tempMessage)

    try {
      const response = await api.post(`/chat/channels/${activeChannel.value}/messages`, {
        content,
        type,
        attachments
      })

      console.log('Message API response:', response.data)

      // Replace temp message with real one from API
      const index = messages.value.findIndex(m => m.id === tempId)
      if (index >= 0) {
        messages.value[index] = response.data
      }

      // Log message status
      console.log('Message status:', response.data.status)
      
      // Show notification if message is pending
      if (response.data.status === 'PENDING' || response.data.status === 'pending') {
        console.log('Message pending teacher approval')
      } else {
        console.log('Message approved and sent')
      }

      // Emit via socket for real-time delivery if connected
      if (socket.value) {
        socket.value.emit('send_message', response.data)
      }
      
      return response.data
    } catch (error) {
      console.error('Failed to send message:', error)
      // Mark message as failed
      const index = messages.value.findIndex(m => m.id === tempId)
      if (index >= 0) {
        messages.value[index].status = 'failed'
      }
      throw error
    }
  }

  async function editMessage(messageId, newContent) {
    try {
      const response = await api.put(`/chat/messages/${messageId}`, {
        content: newContent
      })
      
      const index = messages.value.findIndex(m => m.id === messageId)
      if (index >= 0) {
        messages.value[index] = response.data
      }
      
      if (socket.value) {
        socket.value.emit('message_edited', response.data)
      }
    } catch (error) {
      console.error('Failed to edit message:', error)
    }
  }

  async function deleteMessage(messageId) {
    try {
      await api.delete(`/chat/messages/${messageId}`)
      
      const index = messages.value.findIndex(m => m.id === messageId)
      if (index >= 0) {
        messages.value[index].deleted = true
        messages.value[index].content = 'This message was deleted'
      }
      
      if (socket.value) {
        socket.value.emit('message_deleted', { messageId })
      }
    } catch (error) {
      console.error('Failed to delete message:', error)
    }
  }

  // Typing indicators
  function startTyping() {
    if (!isTyping.value && socket.value && activeChannel.value) {
      isTyping.value = true
      socket.value.emit('typing_start', {
        channelId: activeChannel.value,
        userId: getCurrentUserId()
      })
    }
  }

  function stopTyping() {
    if (isTyping.value && socket.value && activeChannel.value) {
      isTyping.value = false
      socket.value.emit('typing_stop', {
        channelId: activeChannel.value,
        userId: getCurrentUserId()
      })
    }
  }

  function handleUserTyping(data) {
    if (data.userId !== getCurrentUserId()) {
      if (!typingUsers.value.find(u => u.userId === data.userId)) {
        typingUsers.value.push(data)
      }
    }
  }

  function handleUserStoppedTyping(data) {
    typingUsers.value = typingUsers.value.filter(u => u.userId !== data.userId)
  }

  // Read receipts
  function markMessageAsRead(messageId, userId = null) {
    const message = messages.value.find(m => m.id === messageId)
    if (message) {
      if (!message.readBy) message.readBy = []
      if (userId && !message.readBy.includes(userId)) {
        message.readBy.push(userId)
      }
      message.read = true
    }
  }

  function markChannelAsRead(channelId) {
    if (socket.value) {
      socket.value.emit('mark_channel_read', { channelId })
    }
    
    messages.value.forEach(message => {
      if (message.channel_id === channelId && message.sender_id !== getCurrentUserId()) {
        message.read = true
      }
    })
  }

  // Utility functions
  function getCurrentUserId() {
    // This should get the current user ID from auth store
    return localStorage.getItem('userId') || '1'
  }

  function clearMessages() {
    messages.value = []
  }

  function reset() {
    disconnectSocket()
    messages.value = []
    channels.value = []
    activeChannel.value = null
    onlineUsers.value = []
    typingUsers.value = []
    isTyping.value = false
    lastSeen.value = {}
  }

  return {
    // State
    socket,
    messages,
    channels,
    activeChannel,
    onlineUsers,
    typingUsers,
    isConnected,
    isTyping,
    lastSeen,
    
    // Computed
    sortedMessages,
    unreadCount,
    
    // Actions
    connectSocket,
    disconnectSocket,
    joinChannel,
    leaveChannel,
    loadChannelMessages,
    sendMessage,
    editMessage,
    deleteMessage,
    startTyping,
    stopTyping,
    markChannelAsRead,
    clearMessages,
    reset
  }
})