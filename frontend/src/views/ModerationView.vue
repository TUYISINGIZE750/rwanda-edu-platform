<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
    <nav class="bg-white/90 backdrop-blur-xl shadow-lg border-b border-blue-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button @click="$router.back()" class="w-10 h-10 flex items-center justify-center rounded-xl bg-blue-100 text-blue-600 hover:bg-blue-200 transition-all">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <div>
              <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">Message Moderation</h1>
              <p class="text-sm text-gray-600">TSSANYWHERE - Review & Approve Messages</p>
            </div>
          </div>
        </div>
      </div>
    </nav>
    
    <main class="max-w-5xl mx-auto p-6">
      <div v-if="loading" class="text-center py-20">
        <div class="animate-spin h-16 w-16 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
        <p class="text-lg font-medium text-gray-700">Loading messages...</p>
      </div>

      <div v-else-if="pendingMessages.length === 0" class="text-center py-20">
        <div class="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-2xl font-bold text-gray-900 mb-2">All Clear!</p>
        <p class="text-gray-600">No pending messages to review</p>
      </div>

      <div v-else class="space-y-4">
        <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-4 mb-6 border border-blue-200">
          <p class="text-sm font-semibold text-gray-700">{{ pendingMessages.length }} message{{ pendingMessages.length !== 1 ? 's' : '' }} pending review</p>
        </div>
        
        <div v-for="msg in pendingMessages" :key="msg.id" 
             class="bg-white/90 backdrop-blur-xl rounded-2xl shadow-lg border-2 border-gray-200 hover:border-blue-300 transition-all overflow-hidden">
          <div class="p-6">
            <div class="flex justify-between items-start mb-4">
              <div class="flex items-start gap-3">
                <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-full flex items-center justify-center text-white font-bold text-lg">
                  {{ msg.sender?.charAt(0)?.toUpperCase() || 'U' }}
                </div>
                <div>
                  <p class="font-bold text-gray-900 text-lg">{{ msg.sender }}</p>
                  <p class="text-sm text-gray-600">{{ msg.group }} • {{ msg.channel }}</p>
                </div>
              </div>
              <span class="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full">{{ formatDate(msg.created_at) }}</span>
            </div>
            
            <div class="bg-gray-50 rounded-xl p-4 mb-4 border border-gray-200">
              <p class="text-gray-800 leading-relaxed">{{ msg.content }}</p>
            </div>
            
            <div class="flex gap-3">
              <button @click="approveMessage(msg.id)" 
                      class="flex-1 bg-gradient-to-r from-green-500 to-emerald-500 text-white py-3 px-6 rounded-xl hover:from-green-600 hover:to-emerald-600 transition-all shadow-lg hover:shadow-xl font-semibold flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Approve
              </button>
              <button @click="rejectMessage(msg.id)" 
                      class="flex-1 bg-gradient-to-r from-red-500 to-pink-500 text-white py-3 px-6 rounded-xl hover:from-red-600 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl font-semibold flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                Reject
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../utils/api'

const pendingMessages = ref([])
const loading = ref(true)

onMounted(async () => {
  await loadPendingMessages()
})

async function loadPendingMessages() {
  try {
    const response = await api.get('/teacher/pending-messages')
    pendingMessages.value = response.data
  } catch (err) {
    console.error('Failed to load pending messages:', err)
  } finally {
    loading.value = false
  }
}

async function approveMessage(id) {
  try {
    await api.post(`/teacher/messages/${id}/approve`)
    pendingMessages.value = pendingMessages.value.filter(m => m.id !== id)
  } catch (err) {
    console.error('Failed to approve message:', err)
  }
}

async function rejectMessage(id) {
  try {
    await api.post(`/teacher/messages/${id}/reject`)
    pendingMessages.value = pendingMessages.value.filter(m => m.id !== id)
  } catch (err) {
    console.error('Failed to reject message:', err)
  }
}

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleString('en-US', { 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
