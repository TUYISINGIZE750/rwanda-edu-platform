<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-2xl mx-auto">
      <div class="bg-white rounded-lg shadow-lg p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900">Start New Session</h2>
          <button @click="$router.back()" class="text-gray-600 hover:text-gray-900">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="startSession" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Session Title</label>
            <input v-model="form.title" type="text" required
                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                   placeholder="e.g., Practical Workshop - Welding">
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Select Group</label>
            <select v-model="form.groupId" required
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
              <option value="">Select a group</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">
                {{ group.name }}
              </option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Start Time</label>
              <input v-model="form.startTime" type="datetime-local" required
                     class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Duration (hours)</label>
              <input v-model.number="form.duration" type="number" min="0.5" step="0.5" required
                     class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Location</label>
            <input v-model="form.location" type="text" required
                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                   placeholder="e.g., Workshop A - Building 2">
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea v-model="form.description" rows="3" required
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                      placeholder="What will be covered in this session?"></textarea>
          </div>

          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {{ error }}
          </div>

          <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
            {{ success }}
          </div>

          <div class="flex space-x-4">
            <button type="submit" :disabled="loading"
                    class="flex-1 bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 disabled:opacity-50">
              {{ loading ? 'Creating...' : 'Start Session' }}
            </button>
            <button type="button" @click="$router.back()"
                    class="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50">
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
import api from '../utils/api'

const router = useRouter()

const form = ref({
  title: '',
  groupId: '',
  startTime: '',
  duration: 2,
  location: '',
  description: ''
})

const groups = ref([])
const loading = ref(false)
const error = ref('')
const success = ref('')

onMounted(async () => {
  try {
    const response = await api.get('/teacher/dashboard')
    groups.value = response.data.groups || []
  } catch (err) {
    console.error('Failed to load groups:', err)
  }
})

async function startSession() {
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    // Mock session creation - would need backend endpoint
    await new Promise(resolve => setTimeout(resolve, 1000))
    success.value = 'Session created successfully!'
    
    setTimeout(() => {
      router.push('/teacher-dashboard')
    }, 1500)
  } catch (err) {
    error.value = 'Failed to create session'
  } finally {
    loading.value = false
  }
}
</script>
