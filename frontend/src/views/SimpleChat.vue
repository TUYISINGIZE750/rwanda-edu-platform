<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b px-6 py-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">{{ channelName }}</h1>
        <p class="text-sm text-gray-500">{{ messageCount }} messages</p>
      </div>
      <button @click="$router.back()" class="px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200">
        Back
      </button>
    </div>

    <!-- Messages -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-3 bg-gradient-to-b from-gray-50 to-gray-100">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading messages...</p>
      </div>

      <div v-else-if="messages.length === 0" class="text-center py-12">
        <p class="text-gray-500 text-lg">No messages yet</p>
        <p class="text-gray-400 text-sm mt-2">Be the first to send a message!</p>
      </div>

      <div v-else>
        <div v-for="msg in messages" :key="msg.id" 
             class="flex items-end gap-2" :class="msg.is_mine ? 'justify-end' : 'justify-start'">
          <!-- Avatar for others -->
          <div v-if="!msg.is_mine" class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-semibold text-sm flex-shrink-0">
            {{ msg.sender_name.charAt(0).toUpperCase() }}
          </div>
          
          <div class="max-w-md">
            <div v-if="!msg.is_mine" class="flex items-center gap-2 mb-1 ml-1">
              <span class="text-sm font-semibold text-gray-800">{{ msg.sender_name }}</span>
              <span class="text-xs px-2 py-0.5 rounded-full" 
                    :class="msg.sender_role === 'teacher' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'">
                {{ msg.sender_role }}
              </span>
            </div>
            <div class="rounded-2xl px-4 py-2.5 shadow-sm" 
                 :class="msg.is_mine ? 'bg-blue-500 text-white rounded-br-sm' : 'bg-white text-gray-900 rounded-bl-sm'">
              <p class="text-sm leading-relaxed">{{ msg.content }}</p>
              <div class="flex items-center justify-end gap-1 mt-1">
                <p class="text-xs" :class="msg.is_mine ? 'text-blue-100' : 'text-gray-500'">{{ formatTime(msg.timestamp) }}</p>
                <svg v-if="msg.is_mine" class="w-4 h-4" :class="msg.is_mine ? 'text-blue-100' : 'text-gray-400'" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                </svg>
              </div>
            </div>
          </div>
          
          <!-- Avatar for own messages -->
          <div v-if="msg.is_mine" class="w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white font-semibold text-sm flex-shrink-0">
            {{ msg.sender_name.charAt(0).toUpperCase() }}
          </div>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="bg-white border-t p-4">
      <div class="max-w-4xl mx-auto flex gap-3">
        <input 
          v-model="newMessage"
          @keyup.enter="sendMessage"
          type="text"
          placeholder="Type your message..."
          class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="sending"
        />
        <button 
          @click="sendMessage"
          :disabled="!newMessage.trim() || sending"
          class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed font-medium">
          {{ sending ? 'Sending...' : 'Send' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../utils/api'

const route = useRoute()
const router = useRouter()

const channelId = ref(parseInt(route.params.channelId))
const channelName = ref(route.query.name || 'Chat')
const messages = ref([])
const newMessage = ref('')
const loading = ref(true)
const sending = ref(false)
const messagesContainer = ref(null)
const messageCount = ref(0)
const refreshInterval = ref(null)

onMounted(async () => {
  await loadMessages()
  scrollToBottom()
  
  // Auto-refresh every 3 seconds
  refreshInterval.value = setInterval(loadMessages, 3000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})

async function loadMessages() {
  try {
    const response = await api.get(`/simple-chat/channels/${channelId.value}/messages`)
    messages.value = response.data.messages || []
    messageCount.value = response.data.count || 0
    loading.value = false
  } catch (error) {
    console.error('Failed to load messages:', error)
    loading.value = false
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || sending.value) return
  
  sending.value = true
  const content = newMessage.value.trim()
  newMessage.value = ''
  
  try {
    const response = await api.post(`/simple-chat/channels/${channelId.value}/messages`, {
      content
    })
    
    if (response.data.needs_approval) {
      alert('✅ Message sent! Waiting for teacher approval.')
    }
    
    // Reload messages immediately
    await loadMessages()
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)
    alert('❌ Failed to send message: ' + (error.response?.data?.detail || error.message))
    newMessage.value = content // Restore message
  } finally {
    sending.value = false
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

function formatTime(timestamp) {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
}
</script>
