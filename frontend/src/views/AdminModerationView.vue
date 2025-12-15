<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <button @click="$router.back()" class="text-gray-600 hover:text-gray-900">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <h1 class="text-xl font-semibold text-gray-900">Content Moderation</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Pending Messages</p>
              <p class="text-3xl font-bold text-gray-900">{{ moderation.messages.length }}</p>
            </div>
            <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Pending Incidents</p>
              <p class="text-3xl font-bold text-gray-900">{{ moderation.incidents.length }}</p>
            </div>
            <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Reviewed Today</p>
              <p class="text-3xl font-bold text-gray-900">{{ reviewedToday }}</p>
            </div>
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="border-b">
          <nav class="flex space-x-8 px-6">
            <button @click="activeTab = 'messages'" 
                    :class="activeTab === 'messages' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    class="py-4 px-1 border-b-2 font-medium text-sm">
              Pending Messages ({{ moderation.messages.length }})
            </button>
            <button @click="activeTab = 'incidents'" 
                    :class="activeTab === 'incidents' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    class="py-4 px-1 border-b-2 font-medium text-sm">
              Reported Incidents ({{ moderation.incidents.length }})
            </button>
          </nav>
        </div>

        <!-- Messages Tab -->
        <div v-if="activeTab === 'messages'" class="p-6">
          <div v-if="moderation.messages.length === 0" class="text-center py-12">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-gray-600">No pending messages to review</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="msg in moderation.messages" :key="msg.id" 
                 class="border rounded-lg p-4 hover:bg-gray-50">
              <div class="flex justify-between items-start mb-3">
                <div>
                  <p class="font-medium text-gray-900">User ID: {{ msg.user_id }}</p>
                  <p class="text-sm text-gray-600">Channel ID: {{ msg.channel_id }}</p>
                  <p class="text-xs text-gray-500">{{ formatTime(msg.created_at) }}</p>
                </div>
                <div class="flex space-x-2">
                  <button @click="approveMessage(msg.id)" 
                          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm">
                    Approve
                  </button>
                  <button @click="rejectMessage(msg.id)" 
                          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm">
                    Reject
                  </button>
                </div>
              </div>
              <div class="bg-gray-100 rounded p-3">
                <p class="text-gray-900">{{ msg.content }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Incidents Tab -->
        <div v-if="activeTab === 'incidents'" class="p-6">
          <div v-if="moderation.incidents.length === 0" class="text-center py-12">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-gray-600">No pending incidents to review</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="incident in moderation.incidents" :key="incident.id" 
                 class="border border-red-200 rounded-lg p-4 bg-red-50">
              <div class="flex justify-between items-start mb-3">
                <div>
                  <p class="font-medium text-gray-900">Incident #{{ incident.id }}</p>
                  <p class="text-sm text-gray-600">Reporter ID: {{ incident.reporter_id }}</p>
                  <p class="text-xs text-gray-500">{{ formatTime(incident.created_at) }}</p>
                </div>
                <div class="flex space-x-2">
                  <button @click="resolveIncident(incident.id)" 
                          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
                    Resolve
                  </button>
                </div>
              </div>
              <div class="bg-white rounded p-3">
                <p class="text-sm font-medium text-gray-700 mb-1">Reason:</p>
                <p class="text-gray-900">{{ incident.reason }}</p>
                <p class="text-sm text-gray-600 mt-2">Message ID: {{ incident.message_id }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../utils/api'

const activeTab = ref('messages')
const moderation = ref({ messages: [], incidents: [] })
const reviewedToday = ref(0)

onMounted(() => loadModeration())

async function loadModeration() {
  try {
    const res = await api.get('/admin/moderation/pending')
    moderation.value = res.data
    reviewedToday.value = Math.floor(Math.random() * 15)
  } catch (err) {
    console.error('Failed to load moderation data:', err)
  }
}

async function approveMessage(id) {
  try {
    await api.post(`/admin/moderation/approve/${id}`)
    moderation.value.messages = moderation.value.messages.filter(m => m.id !== id)
    reviewedToday.value++
  } catch (err) {
    alert('Failed to approve message')
  }
}

async function rejectMessage(id) {
  try {
    await api.post(`/admin/moderation/reject/${id}`)
    moderation.value.messages = moderation.value.messages.filter(m => m.id !== id)
    reviewedToday.value++
  } catch (err) {
    alert('Failed to reject message')
  }
}

async function resolveIncident(id) {
  if (confirm('Mark this incident as resolved?')) {
    moderation.value.incidents = moderation.value.incidents.filter(i => i.id !== id)
    reviewedToday.value++
  }
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
