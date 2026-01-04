<template>
  <div class="relative">
    <button @click="toggleDropdown" class="relative p-2 text-gray-600 hover:text-blue-600 transition-colors">
      <BellIcon class="h-6 w-6" />
      <span v-if="unreadCount > 0" class="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>

    <div v-if="showDropdown" class="absolute right-0 mt-2 w-96 bg-white rounded-lg shadow-xl z-50 max-h-[500px] overflow-hidden flex flex-col">
      <div class="p-4 border-b flex justify-between items-center bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
        <h3 class="font-semibold">Notifications</h3>
        <button v-if="unreadCount > 0" @click="markAllRead" class="text-xs hover:underline">Mark all read</button>
      </div>

      <div v-if="loading" class="p-8 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
      </div>

      <div v-else-if="notifications.length === 0" class="p-8 text-center text-gray-500">
        <BellIcon class="h-12 w-12 mx-auto mb-2 text-gray-300" />
        <p>No notifications yet</p>
      </div>

      <div v-else class="overflow-y-auto flex-1">
        <div v-for="notif in notifications" :key="notif.id" 
             @click="handleNotificationClick(notif)"
             :class="['p-4 border-b hover:bg-gray-50 cursor-pointer transition-colors', !notif.is_read && 'bg-blue-50']">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0">
              <component :is="getIcon(notif.type)" class="h-6 w-6" :class="getIconColor(notif.type)" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-semibold text-sm text-gray-900">{{ notif.title }}</p>
              <p class="text-sm text-gray-600 mt-1">{{ notif.message }}</p>
              <p class="text-xs text-gray-400 mt-1">{{ formatTime(notif.created_at) }}</p>
            </div>
            <button v-if="!notif.is_read" @click.stop="markAsRead(notif.id)" class="flex-shrink-0 w-2 h-2 bg-blue-600 rounded-full"></button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api, { getWebSocketURL } from '../utils/api'
import { BellIcon, DocumentTextIcon, ChatBubbleLeftIcon, UserGroupIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const showDropdown = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const loading = ref(false)
let ws = null
let reconnectTimeout = null

const connectWebSocket = () => {
  if (!authStore.user?.id) return
  
  const wsUrl = getWebSocketURL()
  const fullWsUrl = `${wsUrl}/ws/notifications/${authStore.user.id}`
  
  console.log('🔌 Connecting to notification WebSocket:', fullWsUrl)
  
  try {
    ws = new WebSocket(fullWsUrl)
    
    ws.onopen = () => {
      console.log('✅ Notification WebSocket connected')
      // Send ping every 30 seconds to keep alive
      setInterval(() => {
        if (ws?.readyState === WebSocket.OPEN) {
          ws.send('ping')
        }
      }, 30000)
    }
    
    ws.onmessage = (event) => {
      if (event.data === 'pong') return
      
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'notification') {
          // New notification received!
          console.log('🔔 New notification:', data.data.title)
          unreadCount.value++
          
          // Show browser notification if permitted
          if (Notification.permission === 'granted') {
            new Notification(data.data.title, {
              body: data.data.message,
              icon: '/logo.png',
              badge: '/logo.png'
            })
          }
          
          // Refresh notifications if dropdown is open
          if (showDropdown.value) {
            fetchNotifications()
          }
        }
      } catch (err) {
        console.error('Failed to parse notification:', err)
      }
    }
    
    ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error)
    }
    
    ws.onclose = () => {
      console.log('🔌 WebSocket closed, reconnecting in 5s...')
      reconnectTimeout = setTimeout(connectWebSocket, 5000)
    }
  } catch (err) {
    console.error('Failed to connect WebSocket:', err)
    reconnectTimeout = setTimeout(connectWebSocket, 5000)
  }
}

const toggleDropdown = async () => {
  showDropdown.value = !showDropdown.value
  if (showDropdown.value) {
    await fetchNotifications()
  }
}

const fetchNotifications = async () => {
  loading.value = true
  try {
    const response = await api.get('/notifications/')
    notifications.value = response.data
  } catch (error) {
    console.error('Failed to fetch notifications:', error)
  } finally {
    loading.value = false
  }
}

const fetchUnreadCount = async () => {
  try {
    const response = await api.get('/notifications/unread-count')
    unreadCount.value = response.data.unread_count
  } catch (error) {
    console.error('Failed to fetch unread count:', error)
  }
}

const markAsRead = async (notificationId) => {
  try {
    await api.put(`/notifications/${notificationId}/read`)
    const notif = notifications.value.find(n => n.id === notificationId)
    if (notif) notif.is_read = true
    unreadCount.value = Math.max(0, unreadCount.value - 1)
  } catch (error) {
    console.error('Failed to mark as read:', error)
  }
}

const markAllRead = async () => {
  try {
    await api.put('/notifications/mark-all-read')
    notifications.value.forEach(n => n.is_read = true)
    unreadCount.value = 0
  } catch (error) {
    console.error('Failed to mark all as read:', error)
  }
}

const handleNotificationClick = async (notif) => {
  if (!notif.is_read) {
    await markAsRead(notif.id)
  }
  if (notif.link) {
    router.push(notif.link)
    showDropdown.value = false
  }
}

const getIcon = (type) => {
  const icons = {
    RESOURCE_UPLOADED: DocumentTextIcon,
    NEW_ANNOUNCEMENT: ChatBubbleLeftIcon,
    NEW_MESSAGE: ChatBubbleLeftIcon,
    CLASS_ASSIGNED: UserGroupIcon,
    GROUP_ASSIGNED: UserGroupIcon,
    MESSAGE_APPROVED: CheckCircleIcon,
    MESSAGE_REJECTED: XCircleIcon,
  }
  return icons[type] || BellIcon
}

const getIconColor = (type) => {
  const colors = {
    RESOURCE_UPLOADED: 'text-blue-600',
    NEW_ANNOUNCEMENT: 'text-purple-600',
    NEW_MESSAGE: 'text-green-600',
    CLASS_ASSIGNED: 'text-indigo-600',
    GROUP_ASSIGNED: 'text-pink-600',
    MESSAGE_APPROVED: 'text-green-600',
    MESSAGE_REJECTED: 'text-red-600',
  }
  return colors[type] || 'text-gray-600'
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)

  if (diff < 60) return 'Just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`
  return date.toLocaleDateString()
}

onMounted(() => {
  fetchUnreadCount()
  connectWebSocket()
  
  // Request browser notification permission
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission()
  }
})

onUnmounted(() => {
  if (ws) {
    ws.close()
    ws = null
  }
  if (reconnectTimeout) {
    clearTimeout(reconnectTimeout)
  }
})
</script>
