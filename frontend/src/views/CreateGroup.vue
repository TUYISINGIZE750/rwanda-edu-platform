<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-2xl mx-auto">
      <div class="bg-white rounded-lg shadow-lg p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900">Create New Group</h2>
          <button @click="$router.back()" class="text-gray-600 hover:text-gray-900">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="createGroup" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Group Name</label>
            <input v-model="form.name" type="text" required
                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                   placeholder="e.g., L5 SWD Advanced Programming">
            <p class="text-xs text-blue-600 mt-1">💡 Tip: Include level (L1-L6) and trade keyword for auto-assignment (e.g., "L5 SWD", "L3 Electronics")</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Department/Trade</label>
            <select v-model="form.department" required
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select Department/Trade</option>
              <optgroup v-for="(trades, category) in TVET_TRADES" :key="category" :label="category">
                <option v-for="trade in trades" :key="trade" :value="trade">{{ trade }}</option>
              </optgroup>
            </select>
            <p class="text-xs text-gray-500 mt-1">Students in this trade will be notified</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Group Type</label>
            <select v-model="form.type" required
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select type</option>
              <option value="CLASS">Class</option>
              <option value="CLUB">Club</option>
              <option value="TEAM">Team</option>
              <option value="SPECIAL">Special</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Grade/Level (Optional)</label>
            <input v-model.number="form.grade" type="number" min="1" max="6"
                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                   placeholder="e.g., 3">
          </div>

          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {{ error }}
          </div>

          <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
            <div class="font-semibold mb-1">✅ {{ success }}</div>
            <div v-if="assignedCount > 0" class="text-sm">
              🎓 {{ assignedCount }} students automatically assigned based on level and trade match
            </div>
          </div>

          <div class="flex space-x-4">
            <button type="submit" :disabled="loading"
                    class="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50">
              {{ loading ? 'Creating...' : 'Create Group' }}
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'
import { TVET_TRADES } from '../data/trades'

const router = useRouter()

const form = ref({
  name: '',
  type: '',
  department: '',
  grade: null
})

const loading = ref(false)
const error = ref('')
const success = ref('')
const assignedCount = ref(0)

async function createGroup() {
  loading.value = true
  error.value = ''
  success.value = ''
  assignedCount.value = 0
  
  try {
    const response = await api.post('/teacher/groups', form.value)
    success.value = response.data.message || 'Group created successfully!'
    assignedCount.value = response.data.students_assigned || 0
    
    setTimeout(() => {
      router.push('/teacher-dashboard')
    }, 2000)
  } catch (err) {
    console.error('Create group error:', err)
    error.value = err.response?.data?.detail || 'Failed to create group'
  } finally {
    loading.value = false
  }
}
</script>
