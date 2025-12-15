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
            <h1 class="text-xl font-semibold text-gray-900">System Settings</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- School Information -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="px-6 py-4 border-b">
          <h3 class="text-lg font-semibold">School Information</h3>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">School Name</label>
            <input v-model="settings.school_name" class="w-full px-4 py-2 border rounded-lg" readonly>
          </div>
        </div>
      </div>

      <!-- Moderation Settings -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="px-6 py-4 border-b">
          <h3 class="text-lg font-semibold">Moderation Settings</h3>
        </div>
        <div class="p-6 space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium">Enable Message Moderation</p>
              <p class="text-sm text-gray-600">All messages require approval before posting</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input v-model="settings.moderation_enabled" type="checkbox" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium">Auto-approve Teacher Messages</p>
              <p class="text-sm text-gray-600">Teacher messages bypass moderation</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input v-model="settings.auto_approve_teachers" type="checkbox" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium">Auto-approve DM Requests</p>
              <p class="text-sm text-gray-600">Student DM requests are automatically approved</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input v-model="settings.dm_request_auto_approve" type="checkbox" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>

      <!-- File Upload Settings -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="px-6 py-4 border-b">
          <h3 class="text-lg font-semibold">File Upload Settings</h3>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Max File Size (MB)</label>
            <input v-model.number="settings.max_file_size_mb" type="number" class="w-full px-4 py-2 border rounded-lg">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Allowed File Types</label>
            <div class="flex flex-wrap gap-2">
              <span v-for="type in settings.allowed_file_types" :key="type" 
                    class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                {{ type }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Session Settings -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="px-6 py-4 border-b">
          <h3 class="text-lg font-semibold">Session Settings</h3>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Session Timeout (minutes)</label>
            <input v-model.number="settings.session_timeout_minutes" type="number" class="w-full px-4 py-2 border rounded-lg">
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div class="flex justify-end">
        <button @click="saveSettings" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          Save Settings
        </button>
      </div>

      <!-- Success Message -->
      <div v-if="showSuccess" class="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg">
        Settings saved successfully!
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../utils/api'

const settings = ref({
  school_name: '',
  moderation_enabled: true,
  auto_approve_teachers: true,
  dm_request_auto_approve: false,
  max_file_size_mb: 10,
  allowed_file_types: [],
  session_timeout_minutes: 60
})

const showSuccess = ref(false)

onMounted(async () => {
  try {
    const res = await api.get('/admin/settings')
    settings.value = res.data
  } catch (err) {
    console.error('Failed to load settings:', err)
  }
})

async function saveSettings() {
  try {
    await api.put('/admin/settings', settings.value)
    showSuccess.value = true
    setTimeout(() => showSuccess.value = false, 3000)
  } catch (err) {
    alert('Failed to save settings')
  }
}
</script>
