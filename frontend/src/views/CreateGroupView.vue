<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <button @click="$router.go(-1)" class="text-gray-600 hover:text-gray-900">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <h1 class="text-xl font-semibold text-gray-900">Create New Group</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white rounded-lg shadow p-8">
        <form @submit.prevent="createGroup" class="space-y-6">
          <!-- Group Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Group Name</label>
            <input v-model="form.name" type="text" required
                   class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                   placeholder="e.g., Electronics Level 2, Welding Basics">
          </div>

          <!-- Department/Trade Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Department/Trade</label>
            <select v-model="form.department" required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Department/Trade</option>
              <option v-for="trade in availableTrades" :key="trade" :value="trade">
                {{ trade }}
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Students in this trade will be notified of new resources</p>
          </div>

          <!-- Assigned Module -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Select Module</label>
            <select v-model="form.module_id" required @change="onModuleChange"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Module</option>
              <option v-for="module in assignedModules" :key="module.id" :value="module.id">
                {{ module.name }} ({{ module.trade }} - Level {{ module.level }})
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Only modules assigned to you by DOS are available</p>
          </div>

          <!-- Module Info (Auto-filled) -->
          <div v-if="selectedModule" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 class="font-medium text-blue-900 mb-2">Module Information</h4>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span class="text-blue-700 font-medium">Trade:</span>
                <span class="text-blue-600 ml-2">{{ selectedModule.trade }}</span>
              </div>
              <div>
                <span class="text-blue-700 font-medium">Level:</span>
                <span class="text-blue-600 ml-2">Level {{ selectedModule.level }}</span>
              </div>
              <div class="col-span-2">
                <span class="text-blue-700 font-medium">Description:</span>
                <p class="text-blue-600 mt-1">{{ selectedModule.description }}</p>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea v-model="form.description" rows="3"
                      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Brief description of the group purpose..."></textarea>
          </div>

          <!-- Default Channels -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-3">Default Channels</label>
            <div class="space-y-2">
              <label v-for="channel in defaultChannels" :key="channel.name" class="flex items-center">
                <input type="checkbox" v-model="channel.selected" class="mr-3 h-4 w-4 text-blue-600">
                <span class="text-sm text-gray-700">{{ channel.name }} - {{ channel.description }}</span>
              </label>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-red-600 text-sm">{{ error }}</p>
          </div>

          <!-- Success Message -->
          <div v-if="success" class="bg-green-50 border border-green-200 rounded-lg p-4">
            <p class="text-green-600 text-sm">{{ success }}</p>
          </div>

          <!-- Submit Button -->
          <div class="flex space-x-4">
            <button type="submit" :disabled="loading"
                    class="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed">
              <span v-if="!loading">Create Group</span>
              <span v-else class="flex items-center justify-center">
                <svg class="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating...
              </span>
            </button>
            <button type="button" @click="$router.go(-1)"
                    class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../utils/api-new'

const router = useRouter()
const authStore = useAuthStore()

const assignedModules = ref([])
const selectedModule = ref(null)
const availableTrades = ref([])

const form = ref({
  name: '',
  module_id: '',
  department: '',
  description: ''
})

const defaultChannels = ref([
  { name: 'general', description: 'General discussion', selected: true },
  { name: 'announcements', description: 'Important announcements', selected: true },
  { name: 'assignments', description: 'Assignment submissions', selected: false },
  { name: 'resources', description: 'Learning materials', selected: false },
  { name: 'questions', description: 'Q&A and help', selected: false }
])

const loading = ref(false)
const error = ref('')
const success = ref('')

onMounted(async () => {
  await loadAssignedModules()
  await loadAvailableTrades()
})

async function loadAssignedModules() {
  try {
    const response = await api.get('/teacher/assigned-modules')
    assignedModules.value = response.data || []
  } catch (err) {
    console.error('Failed to load assigned modules:', err)
    error.value = 'Failed to load assigned modules'
  }
}

async function loadAvailableTrades() {
  try {
    const user = authStore.user
    console.log('Loading trades for school:', user?.school_id)
    if (user && user.school_id) {
      const response = await api.get(`/registration/trades/${user.school_id}`)
      console.log('Trades response:', response.data)
      if (response.data.success && response.data.trades) {
        availableTrades.value = response.data.trades.map(t => typeof t === 'string' ? t : t.name)
      }
    }
  } catch (err) {
    console.error('Failed to load trades:', err)
    // Fallback: use common TVET trades
    availableTrades.value = [
      'Electronics',
      'Welding',
      'Plumbing',
      'Carpentry',
      'Masonry',
      'Automotive',
      'ICT',
      'Hospitality',
      'Agriculture'
    ]
  }
}

function onModuleChange() {
  selectedModule.value = assignedModules.value.find(m => m.id === parseInt(form.value.module_id))
}

async function createGroup() {
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    const selectedChannels = defaultChannels.value
      .filter(ch => ch.selected)
      .map(ch => ({ name: ch.name, description: ch.description }))
    
    const payload = {
      name: form.value.name,
      module_id: parseInt(form.value.module_id),
      department: form.value.department,
      description: form.value.description,
      channels: selectedChannels
    }
    
    const response = await api.post('/groups', payload)
    
    success.value = 'Group created successfully!'
    
    // Redirect to the new group after 2 seconds
    setTimeout(() => {
      router.push(`/hubs/${response.data.id}`)
    }, 2000)
    
  } catch (err) {
    console.error('Failed to create group:', err)
    error.value = err.response?.data?.detail || 'Failed to create group. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>