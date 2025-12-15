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
            <h1 class="text-xl font-semibold text-gray-900">Module Management</h1>
          </div>
          <button @click="showCreateModule = true" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
            Create Module
          </button>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Modules List -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">School Modules</h3>
        </div>
        <div class="p-6">
          <div v-if="modules.length === 0" class="text-center py-8">
            <p class="text-gray-600">No modules created yet</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="module in modules" :key="module.id" 
                 class="border border-gray-200 rounded-lg p-4">
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <h4 class="font-medium text-gray-900">{{ module.name }}</h4>
                  <p class="text-sm text-gray-600 mt-1">{{ module.description }}</p>
                  <div class="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                    <span>{{ module.trade }} - Level {{ module.level }}</span>
                    <span>{{ module.lessons?.length || 0 }} lessons</span>
                    <span v-if="module.assigned_teacher">Assigned to: {{ module.assigned_teacher }}</span>
                  </div>
                </div>
                <div class="flex space-x-2">
                  <button @click="assignModule(module)" class="text-blue-600 hover:text-blue-700 text-sm">
                    Assign
                  </button>
                  <button @click="editModule(module)" class="text-green-600 hover:text-green-700 text-sm">
                    Edit
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Module Modal -->
    <div v-if="showCreateModule" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg max-w-2xl w-full mx-4 max-h-96 overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-medium text-gray-900">Create New Module</h3>
          <button @click="showCreateModule = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <form @submit.prevent="createModule" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Module Name</label>
            <input v-model="moduleForm.name" type="text" required
                   class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Trade</label>
            <select v-model="moduleForm.trade" required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="">Select Trade</option>
              <option v-for="trade in schoolTrades" :key="trade" :value="trade">
                {{ trade }}
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Trades available at {{ authStore.user?.school_name }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Level</label>
            <select v-model="moduleForm.level" required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="">Select Level</option>
              <option value="1">Level 1</option>
              <option value="2">Level 2</option>
              <option value="3">Level 3</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea v-model="moduleForm.description" rows="3"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"></textarea>
          </div>
          <div class="flex space-x-3">
            <button type="submit" class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700">
              Create Module
            </button>
            <button type="button" @click="showCreateModule = false" 
                    class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Assign Module Modal -->
    <div v-if="showAssignModule" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg max-w-md w-full mx-4">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-medium text-gray-900">Assign Module</h3>
          <button @click="showAssignModule = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6">
          <div class="mb-4">
            <p class="text-sm text-gray-600">Assigning: <strong>{{ selectedModule?.name }}</strong></p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Select Teacher</label>
            <select v-model="assignForm.teacher_id" required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
              <option value="">Select Teacher</option>
              <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
                {{ teacher.full_name }} ({{ teacher.email }})
              </option>
            </select>
          </div>
          <div class="flex space-x-3 mt-6">
            <button @click="confirmAssignment" class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700">
              Assign Module
            </button>
            <button @click="showAssignModule = false" 
                    class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancel
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
import { useAuthStore } from '../stores/auth'
import api from '../utils/api-new'

const router = useRouter()
const authStore = useAuthStore()

const modules = ref([])
const teachers = ref([])
const schoolTrades = ref([])
const showCreateModule = ref(false)
const showAssignModule = ref(false)
const selectedModule = ref(null)

const moduleForm = ref({
  name: '',
  trade: '',
  level: '',
  description: ''
})

const assignForm = ref({
  teacher_id: ''
})

onMounted(async () => {
  if (authStore.user?.role?.toLowerCase() !== 'admin') {
    router.push('/home')
    return
  }
  
  await loadModules()
  await loadTeachers()
  await loadSchoolTrades()
})

async function loadModules() {
  try {
    const response = await api.get('/admin/modules')
    modules.value = response.data || []
  } catch (err) {
    console.error('Failed to load modules:', err)
  }
}

async function loadTeachers() {
  try {
    const response = await api.get('/admin/teachers')
    teachers.value = response.data || []
  } catch (err) {
    console.error('Failed to load teachers:', err)
  }
}

async function loadSchoolTrades() {
  try {
    const response = await api.get(`/admin/school-trades/${authStore.user.school_id}`)
    schoolTrades.value = response.data || []
  } catch (err) {
    console.error('Failed to load school trades:', err)
    // Fallback to default trades if API fails
    schoolTrades.value = ['Electronics', 'Welding', 'Automotive', 'Construction', 'ICT']
  }
}

async function createModule() {
  try {
    await api.post('/admin/modules', moduleForm.value)
    showCreateModule.value = false
    moduleForm.value = { name: '', trade: '', level: '', description: '' }
    await loadModules()
  } catch (err) {
    console.error('Failed to create module:', err)
  }
}

function assignModule(module) {
  selectedModule.value = module
  showAssignModule.value = true
}

async function confirmAssignment() {
  try {
    await api.post(`/admin/modules/${selectedModule.value.id}/assign`, {
      teacher_id: assignForm.value.teacher_id
    })
    showAssignModule.value = false
    assignForm.value = { teacher_id: '' }
    await loadModules()
  } catch (err) {
    console.error('Failed to assign module:', err)
  }
}

function editModule(module) {
  // Navigate to module edit page
  router.push(`/admin/modules/${module.id}/edit`)
}
</script>