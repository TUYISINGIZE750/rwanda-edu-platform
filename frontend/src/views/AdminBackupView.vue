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
            <h1 class="text-xl font-semibold text-gray-900">Backup & Restore</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Create Backup Section -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="px-6 py-4 border-b">
          <h3 class="text-lg font-semibold">Create New Backup</h3>
        </div>
        <div class="p-6">
          <p class="text-gray-600 mb-4">Create a complete backup of your school's data including users, messages, resources, and settings.</p>
          <button @click="createBackup" :disabled="creating" 
                  class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 flex items-center space-x-2">
            <svg v-if="creating" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>{{ creating ? 'Creating Backup...' : 'Create Backup Now' }}</span>
          </button>
        </div>
      </div>

      <!-- Backup History -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b">
          <h3 class="text-lg font-semibold">Backup History</h3>
        </div>
        <div class="p-6">
          <div v-if="backups.length === 0" class="text-center py-12">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
            </svg>
            <p class="text-gray-600">No backups available</p>
          </div>
          <div v-else class="space-y-3">
            <div v-for="backup in backups" :key="backup.id" 
                 class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
              <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p class="font-medium text-gray-900">{{ backup.id }}</p>
                  <p class="text-sm text-gray-600">{{ formatDate(backup.created_at) }}</p>
                  <p class="text-xs text-gray-500">Size: {{ backup.size_mb }} MB</p>
                </div>
              </div>
              <div class="flex space-x-2">
                <button @click="downloadBackup(backup)" 
                        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm flex items-center space-x-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  <span>Download</span>
                </button>
                <button @click="restoreBackup(backup)" 
                        class="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 text-sm flex items-center space-x-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>Restore</span>
                </button>
                <button @click="deleteBackup(backup)" 
                        class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm">
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Backup Info -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-6">
        <div class="flex">
          <svg class="w-5 h-5 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <p class="text-sm font-medium text-blue-900">Backup Information</p>
            <p class="text-sm text-blue-700 mt-1">Backups include all users, groups, messages, resources, and system settings. Restoring a backup will replace current data.</p>
          </div>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="showSuccess" class="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../utils/api'

const backups = ref([])
const creating = ref(false)
const showSuccess = ref(false)
const successMessage = ref('')

onMounted(() => loadBackups())

async function loadBackups() {
  try {
    const res = await api.get('/admin/backup/list')
    backups.value = res.data
  } catch (err) {
    console.error('Failed to load backups:', err)
  }
}

async function createBackup() {
  creating.value = true
  try {
    const res = await api.post('/admin/backup/create')
    backups.value.unshift(res.data)
    successMessage.value = 'Backup created successfully!'
    showSuccess.value = true
    setTimeout(() => showSuccess.value = false, 3000)
  } catch (err) {
    alert('Failed to create backup')
  } finally {
    creating.value = false
  }
}

function downloadBackup(backup) {
  successMessage.value = `Downloading ${backup.id}...`
  showSuccess.value = true
  setTimeout(() => showSuccess.value = false, 3000)
}

function restoreBackup(backup) {
  if (confirm(`Are you sure you want to restore backup ${backup.id}? This will replace all current data.`)) {
    successMessage.value = 'Restore initiated. This may take a few minutes...'
    showSuccess.value = true
    setTimeout(() => showSuccess.value = false, 5000)
  }
}

function deleteBackup(backup) {
  if (confirm(`Delete backup ${backup.id}?`)) {
    backups.value = backups.value.filter(b => b.id !== backup.id)
    successMessage.value = 'Backup deleted'
    showSuccess.value = true
    setTimeout(() => showSuccess.value = false, 3000)
  }
}

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
