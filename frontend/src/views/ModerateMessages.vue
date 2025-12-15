<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Moderate Messages</h1>
            <p class="text-gray-600 mt-1">{{ pendingCount }} pending messages</p>
          </div>
          <button @click="$router.back()" class="px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200">
            Back to Dashboard
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="bg-white rounded-lg shadow-sm p-12 text-center">
        <div class="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading pending messages...</p>
      </div>

      <!-- No pending messages -->
      <div v-else-if="pendingMessages.length === 0" class="bg-white rounded-lg shadow-sm p-12 text-center">
        <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">All caught up!</h3>
        <p class="text-gray-600">No pending messages to moderate</p>
      </div>

      <!-- Pending messages list -->
      <div v-else class="space-y-4">
        <div v-for="msg in pendingMessages" :key="msg.id" 
             class="bg-white rounded-lg shadow-sm p-6 border-l-4 border-yellow-400">
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <span class="font-semibold text-gray-900">{{ msg.sender_name }}</span>
                <span class="text-sm text-gray-500">→</span>
                <span class="text-sm font-medium text-blue-600">#{{ msg.channel_name }}</span>
              </div>
              <p class="text-sm text-gray-500">{{ formatTime(msg.created_at) }}</p>
            </div>
            <span class="px-3 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded-full">
              Pending
            </span>
          </div>

          <div class="bg-gray-50 rounded-lg p-4 mb-4">
            <p class="text-gray-900">{{ msg.content }}</p>
          </div>

          <div class="flex gap-3">
            <button @click="approveMessage(msg.id)" 
                    class="flex-1 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 font-medium">
              ✓ Approve
            </button>
            <button @click="rejectMessage(msg.id)" 
                    class="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 font-medium">
              ✗ Reject
            </button>
            <button @click="viewInChannel(msg.channel_id, msg.channel_name)" 
                    class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-medium">
              View Channel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'

const router = useRouter()
const pendingMessages = ref([])
const loading = ref(true)
const pendingCount = ref(0)

onMounted(async () => {
  await loadPendingMessages()
})

async function loadPendingMessages() {
  try {
    const response = await api.get('/simple-chat/pending-messages')
    pendingMessages.value = response.data.pending || []
    pendingCount.value = response.data.count || 0
  } catch (error) {
    console.error('Failed to load pending messages:', error)
    alert('Failed to load pending messages')
  } finally {
    loading.value = false
  }
}

async function approveMessage(messageId) {
  try {
    await api.post(`/simple-chat/approve-message/${messageId}`)
    // Remove from list
    pendingMessages.value = pendingMessages.value.filter(m => m.id !== messageId)
    pendingCount.value--
    alert('✅ Message approved!')
  } catch (error) {
    console.error('Failed to approve message:', error)
    alert('❌ Failed to approve message')
  }
}

async function rejectMessage(messageId) {
  if (!confirm('Are you sure you want to reject this message?')) return
  
  try {
    await api.post(`/simple-chat/reject-message/${messageId}`)
    // Remove from list
    pendingMessages.value = pendingMessages.value.filter(m => m.id !== messageId)
    pendingCount.value--
    alert('✅ Message rejected')
  } catch (error) {
    console.error('Failed to reject message:', error)
    alert('❌ Failed to reject message')
  }
}

function viewInChannel(channelId, channelName) {
  router.push({
    path: `/chat/${channelId}`,
    query: { name: channelName }
  })
}

function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}
</script>
