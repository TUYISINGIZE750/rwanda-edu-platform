<template>
  <div class="min-h-screen bg-white">
    <!-- Navigation Header -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-600 rounded-lg flex items-center justify-center text-white font-bold text-lg shadow-md">
              RTB
            </div>
            <span class="text-xl font-bold text-gray-900">TSSANYWHERE</span>
          </div>
          <div class="flex items-center gap-6">
            <NotificationBell />
            <div class="text-right">
              <p class="text-sm font-semibold text-gray-900">{{ authStore.user?.full_name }}</p>
              <p class="text-xs text-gray-500">Teacher</p>
            </div>
            <button @click="authStore.logout(); $router.push('/login')" class="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-all text-sm font-medium">
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white py-20">
      <div class="max-w-7xl mx-auto px-8">
        <div class="max-w-2xl">
          <h1 class="text-5xl font-bold mb-4">Welcome back, {{ authStore.user?.full_name?.split(' ')[0] }}</h1>
          <p class="text-xl text-gray-300 mb-8">Manage your classes, inspire students, and track progress all in one place</p>
          <div v-if="isClassTeacher" class="flex gap-4">
            <button @click="openCreateClassModal" class="px-8 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-semibold transition-all">
              Create Class
            </button>
            <button @click="showCreateGroupModal = true" class="px-8 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-semibold transition-all">
              Create Group
            </button>
          </div>
          <div v-else-if="!hasPermissions" class="bg-yellow-600 bg-opacity-20 border border-yellow-500 rounded-lg p-4">
            <p class="text-yellow-200">⏳ Waiting for class or group assignment from your administrator</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-8 py-16">
      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
        <div class="bg-white border border-gray-200 rounded-lg p-8 hover:shadow-lg transition-all">
          <div class="flex items-center justify-between mb-4">
            <div class="text-4xl font-bold text-gray-900">{{ groups.length }}</div>
            <div class="text-4xl">📚</div>
          </div>
          <p class="text-gray-600 font-medium">Active Classes</p>
          <p class="text-sm text-gray-500 mt-2">Manage your teaching modules</p>
        </div>

        <div class="bg-white border border-gray-200 rounded-lg p-8 hover:shadow-lg transition-all">
          <div class="flex items-center justify-between mb-4">
            <div class="text-4xl font-bold text-gray-900">{{ totalStudents }}</div>
            <div class="text-4xl">👥</div>
          </div>
          <p class="text-gray-600 font-medium">Total Students</p>
          <p class="text-sm text-gray-500 mt-2">Across all your classes</p>
        </div>

        <div class="bg-white border border-gray-200 rounded-lg p-8 hover:shadow-lg transition-all">
          <div class="flex items-center justify-between mb-4">
            <div class="text-4xl font-bold text-gray-900">{{ resources.length }}</div>
            <div class="text-4xl">📄</div>
          </div>
          <p class="text-gray-600 font-medium">Resources</p>
          <p class="text-sm text-gray-500 mt-2">Uploaded materials</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <section class="mb-16">
        <h2 class="text-2xl font-bold text-gray-900 mb-8">Quick Actions</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button @click="openCreateClassModal" class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-all text-center group">
            <div class="text-4xl mb-3">➕</div>
            <p class="font-semibold text-gray-900 group-hover:text-orange-600">Create Class</p>
            <p class="text-xs text-gray-500 mt-1">Add new class</p>
          </button>

          <button @click="showCreateGroupModal = true" class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-all text-center group">
            <div class="text-4xl mb-3">👥</div>
            <p class="font-semibold text-gray-900 group-hover:text-orange-600">Create Group</p>
            <p class="text-xs text-gray-500 mt-1">New club or discussion</p>
          </button>

          <button @click="$router.push('/upload-resource')" class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-all text-center group">
            <div class="text-4xl mb-3">📤</div>
            <p class="font-semibold text-gray-900 group-hover:text-orange-600">Upload Resource</p>
            <p class="text-xs text-gray-500 mt-1">Share materials</p>
          </button>
        </div>
      </section>

      <!-- Classes Section -->
      <section>
        <h2 class="text-2xl font-bold text-gray-900 mb-8">My Classes, Groups & Clubs</h2>
        <div v-if="loading" class="text-center py-12">
          <div class="animate-spin h-12 w-12 border-4 border-orange-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p class="text-gray-600">Loading classes...</p>
        </div>

        <div v-else-if="groups.length === 0 && !hasPermissions" class="bg-white border border-gray-200 rounded-lg p-12 text-center">
          <div class="text-6xl mb-4">⏳</div>
          <p class="text-xl font-semibold text-gray-900 mb-2">Waiting for Assignment</p>
          <p class="text-gray-600 mb-6">You haven't been assigned to any classes or groups yet. Please contact your administrator (DOS) or class teacher for assignment.</p>
        </div>

        <div v-else-if="groups.length === 0 && isClassTeacher" class="bg-white border border-gray-200 rounded-lg p-12 text-center">
          <div class="text-6xl mb-4">📚</div>
          <p class="text-xl font-semibold text-gray-900 mb-2">No classes, groups or clubs yet</p>
          <p class="text-gray-600 mb-6">Create your first class or group to get started</p>
          <div class="flex gap-3 justify-center">
            <button @click="openCreateClassModal" class="px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-semibold transition-all">
              Create Class
            </button>
            <button @click="showCreateGroupModal = true" class="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-semibold transition-all">
              Create Group
            </button>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="group in groups" :key="group.id" 
               @click="$router.push(`/hubs/${group.id}`)"
               class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg hover:border-orange-300 transition-all cursor-pointer">
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="text-lg font-bold text-gray-900">{{ group.name }}</h3>
                <p class="text-sm text-gray-600 mt-1">{{ group.member_count }} students • {{ group.type }}</p>
              </div>
              <div class="text-3xl">{{ getIcon(group.type) }}</div>
            </div>
            <div class="pt-4 border-t border-gray-200">
              <p class="text-sm text-gray-500">Click to open</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Create Module Modal -->
    <div v-if="showCreateModuleModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click="showCreateModuleModal = false">
      <div class="bg-white rounded-lg w-full max-w-2xl shadow-2xl" @click.stop>
        <div class="p-8 border-b border-gray-200">
          <h3 class="text-2xl font-bold text-gray-900">Create Class</h3>
          <p class="text-gray-600 mt-1">Create a new class for your students</p>
        </div>
        
        <div class="p-8 space-y-6">
          <div>
            <label class="block text-sm font-semibold text-gray-900 mb-2">Class Name</label>
            <input v-model="newModule.name" type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-orange-500 focus:outline-none" placeholder="e.g., L5 Software Development">
            <p class="text-xs text-gray-500 mt-1">Include level (L1-L6) and department for auto-assignment</p>
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-900 mb-2">Department/Trade</label>
            <select v-model="newModule.department" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-orange-500 focus:outline-none">
              <option value="">Select department...</option>
              <option v-for="dept in schoolDepartments" :key="dept" :value="dept">
                {{ dept }}
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Departments available at your school</p>
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-900 mb-2">Level</label>
            <select v-model="newModule.grade" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-orange-500 focus:outline-none">
              <option :value="null">Select level...</option>
              <option :value="1">Level 1</option>
              <option :value="2">Level 2</option>
              <option :value="3">Level 3</option>
              <option :value="4">Level 4</option>
              <option :value="5">Level 5</option>
              <option :value="6">Level 6</option>
            </select>
          </div>
        </div>
        
        <div class="p-8 border-t border-gray-200 flex gap-3">
          <button @click="createModule" class="flex-1 px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-semibold transition-all">
            Create Class
          </button>
          <button @click="showCreateModuleModal = false" class="px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-900 rounded-lg font-semibold transition-all">
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Create Group Modal -->
    <div v-if="showCreateGroupModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click="showCreateGroupModal = false">
      <div class="bg-white rounded-lg w-full max-w-2xl shadow-2xl" @click.stop>
        <div class="p-8 border-b border-gray-200">
          <h3 class="text-2xl font-bold text-gray-900">Create Group/Club</h3>
          <p class="text-gray-600 mt-1">Create a new group or club for students</p>
        </div>
        
        <div class="p-8 space-y-6">
          <div>
            <label class="block text-sm font-semibold text-gray-900 mb-2">Group/Club Name</label>
            <input v-model="newGroup.name" type="text" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-orange-500 focus:outline-none" placeholder="e.g., Science Club">
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-900 mb-2">Type</label>
            <select v-model="newGroup.type" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-orange-500 focus:outline-none">
              <option value="CLUB">Club</option>
              <option value="GROUP">Group</option>
              <option value="DISCUSSION">Discussion</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-900 mb-2">Description</label>
            <textarea v-model="newGroup.description" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-orange-500 focus:outline-none" placeholder="Brief description"></textarea>
          </div>
        </div>
        
        <div class="p-8 border-t border-gray-200 flex gap-3">
          <button @click="createGroup" class="flex-1 px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-semibold transition-all">
            Create Group
          </button>
          <button @click="showCreateGroupModal = false" class="px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-900 rounded-lg font-semibold transition-all">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../utils/api'
import NotificationBell from '../components/NotificationBell.vue'

const router = useRouter()
const authStore = useAuthStore()

const groups = ref([])
const resources = ref([])
const loading = ref(false)
const hasPermissions = ref(true)
const isClassTeacher = ref(false)
const schoolDepartments = ref([])
const showCreateModuleModal = ref(false)
const showCreateGroupModal = ref(false)
const newModule = ref({ name: '', department: '', grade: null })
const newGroup = ref({ name: '', description: '', type: 'CLUB' })

const totalStudents = computed(() => {
  return groups.value.reduce((sum, group) => sum + (group.member_count || 0), 0)
})

function getIcon(type) {
  const icons = {
    'CLASS': '📖',
    'CLUB': '🎯',
    'GROUP': '👥',
    'DISCUSSION': '💬'
  }
  return icons[type] || '📚'
}

async function createModule() {
  if (!newModule.value.name) {
    alert('Please enter class name')
    return
  }
  
  try {
    const response = await api.post('/teacher/groups', {
      name: newModule.value.name,
      type: 'CLASS',
      department: newModule.value.department || null,
      grade: newModule.value.grade
    })
    
    alert(response.data.message || 'Class created successfully!')
    newModule.value = { name: '', department: '', grade: null }
    showCreateModuleModal.value = false
    await loadDashboard()
  } catch (err) {
    console.error('Failed to create class:', err)
    alert(err.response?.data?.detail || 'Failed to create class')
  }
}

async function createGroup() {
  if (!newGroup.value.name) {
    alert('Please enter group name')
    return
  }
  
  try {
    const response = await api.post('/teacher/groups', {
      name: newGroup.value.name,
      type: newGroup.value.type,
      description: newGroup.value.description || null
    })
    
    alert(response.data.message || 'Group created successfully!')
    newGroup.value = { name: '', description: '', type: 'CLUB' }
    showCreateGroupModal.value = false
    await loadDashboard()
  } catch (err) {
    console.error('Failed to create group:', err)
    alert(err.response?.data?.detail || 'Failed to create group')
  }
}

async function loadDashboard() {
  try {
    loading.value = true
    const response = await api.get('/teacher/dashboard')
    groups.value = response.data.groups || []
    resources.value = response.data.resources || []
    
    // Check if teacher has permissions
    const user = authStore.user
    if (user.is_class_teacher && user.managed_class_id) {
      // Class teacher - can manage their class
      hasPermissions.value = true
      isClassTeacher.value = true
    } else if (groups.value.length > 0) {
      // Regular teacher with group assignments
      hasPermissions.value = true
      isClassTeacher.value = false
    } else {
      // No permissions yet
      hasPermissions.value = false
      isClassTeacher.value = false
    }
    
    // Load school departments/trades if class teacher
    if (isClassTeacher.value || groups.value.length > 0) {
      await loadSchoolDepartments()
    }
  } catch (err) {
    console.error('Failed to load dashboard:', err)
  } finally {
    loading.value = false
  }
}

async function loadSchoolDepartments() {
  try {
    console.log('Loading departments for school_id:', authStore.user.school_id)
    const response = await api.get(`/locations/schools/${authStore.user.school_id}`)
    console.log('School API response:', response.data)
    
    if (response.data.trades && response.data.trades.length > 0) {
      schoolDepartments.value = response.data.trades
      console.log('Loaded departments from API:', schoolDepartments.value)
    } else {
      throw new Error('No trades found for school')
    }
  } catch (err) {
    console.warn('School not found or no trades, using default TVET trades:', err.message)
    schoolDepartments.value = [
      'Software Development',
      'Computer Systems and Architecture',
      'Land Surveying',
      'Electronics',
      'Electrical Installation',
      'Plumbing',
      'Mechanical Engineering',
      'Civil Engineering',
      'Automotive Technology',
      'Welding and Metal Fabrication',
      'Carpentry and Joinery',
      'Masonry',
      'Hospitality Management',
      'Culinary Arts',
      'Agriculture',
      'Animal Husbandry'
    ]
    console.log('Using fallback departments:', schoolDepartments.value.length)
  }
}

async function openCreateClassModal() {
  // Load departments first, then show modal
  if (schoolDepartments.value.length === 0) {
    await loadSchoolDepartments()
  }
  // Small delay to ensure state updates
  await new Promise(resolve => setTimeout(resolve, 100))
  showCreateModuleModal.value = true
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  await loadDashboard()
})
</script>

<style scoped>
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
