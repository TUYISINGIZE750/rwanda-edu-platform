<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <!-- Header -->
    <header class="bg-white/90 backdrop-blur-xl border-b border-indigo-200 shadow-lg sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg">
              <span class="text-2xl">👨‍💼</span>
            </div>
            <div>
              <h1 class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">DOS Dashboard</h1>
              <p class="text-xs text-gray-600">Deputy in charge of studies</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-right">
              <p class="text-sm font-semibold text-gray-900">{{ authStore.user?.full_name }}</p>
              <p class="text-xs text-gray-600">DOS Admin</p>
            </div>
            <button @click="authStore.logout(); $router.push('/login')" class="px-4 py-2 bg-red-500 text-white rounded-xl hover:bg-red-600 transition-all shadow-lg">
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="flex-1 overflow-y-auto">
      <div class="max-w-7xl mx-auto px-6 py-6">
        <!-- Stats Grid -->
        <div class="grid grid-cols-4 gap-4 mb-6">
          <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-lg border-2 border-indigo-200">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center text-2xl shadow-lg">👨‍🏫</div>
              <div>
                <p class="text-3xl font-bold text-gray-900">{{ stats.total_teachers }}</p>
                <p class="text-sm text-gray-600">Total Teachers</p>
              </div>
            </div>
          </div>

          <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-lg border-2 border-green-200">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center text-2xl shadow-lg">👥</div>
              <div>
                <p class="text-3xl font-bold text-gray-900">{{ stats.total_students }}</p>
                <p class="text-sm text-gray-600">Total Students</p>
              </div>
            </div>
          </div>

          <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-lg border-2 border-orange-200">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center text-2xl shadow-lg">📚</div>
              <div>
                <p class="text-3xl font-bold text-gray-900">{{ stats.total_classes }}</p>
                <p class="text-sm text-gray-600">Total Classes</p>
              </div>
            </div>
          </div>

          <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-lg border-2 border-purple-200">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center text-2xl shadow-lg">⭐</div>
              <div>
                <p class="text-3xl font-bold text-gray-900">{{ stats.class_teachers }}</p>
                <p class="text-sm text-gray-600">Class Teachers</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl p-6 mb-6 border-2 border-indigo-200">
          <h3 class="text-xl font-bold text-gray-900 mb-4">⚡ Quick Actions</h3>
          <div class="grid grid-cols-3 gap-4">
            <button @click="openCreateModal" class="p-6 border-2 border-dashed border-gray-300 rounded-2xl hover:border-indigo-500 hover:bg-indigo-50 transition-all group">
              <div class="text-center">
                <div class="w-16 h-16 bg-indigo-100 rounded-2xl flex items-center justify-center mx-auto mb-3 group-hover:bg-indigo-200 transition-all">
                  <span class="text-3xl">➕</span>
                </div>
                <p class="font-semibold text-gray-900">Create Teacher</p>
                <p class="text-xs text-gray-600 mt-1">Add new teacher account</p>
              </div>
            </button>

            <button @click="loadAllTeachers" class="p-6 border-2 border-dashed border-gray-300 rounded-2xl hover:border-green-500 hover:bg-green-50 transition-all group">
              <div class="text-center">
                <div class="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-3 group-hover:bg-green-200 transition-all">
                  <span class="text-3xl">👥</span>
                </div>
                <p class="font-semibold text-gray-900">Manage Teachers</p>
                <p class="text-xs text-gray-600 mt-1">View all teachers</p>
              </div>
            </button>

            <button @click="loadAllTeachers" class="p-6 border-2 border-dashed border-gray-300 rounded-2xl hover:border-orange-500 hover:bg-orange-50 transition-all group">
              <div class="text-center">
                <div class="w-16 h-16 bg-orange-100 rounded-2xl flex items-center justify-center mx-auto mb-3 group-hover:bg-orange-200 transition-all">
                  <span class="text-3xl">📚</span>
                </div>
                <p class="font-semibold text-gray-900">Assign Classes</p>
                <p class="text-xs text-gray-600 mt-1">Set class teachers</p>
              </div>
            </button>
          </div>
        </div>

        <!-- Recent Teachers -->
        <div class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl overflow-hidden border-2 border-indigo-200">
          <div class="p-6 border-b border-indigo-200 bg-gradient-to-r from-indigo-50 to-purple-50">
            <h3 class="text-xl font-bold text-gray-900">👨‍🏫 Recent Teachers</h3>
            <p class="text-sm text-gray-600">Latest teacher accounts created</p>
          </div>
          <div class="overflow-y-auto max-h-96 p-6">
            <div v-if="loading" class="text-center py-8">
              <div class="animate-spin h-12 w-12 border-4 border-indigo-500 border-t-transparent rounded-full mx-auto mb-4"></div>
              <p class="text-gray-600">Loading...</p>
            </div>
            <div v-else-if="recentTeachers.length === 0" class="text-center py-8">
              <div class="text-6xl mb-4">👨‍🏫</div>
              <p class="text-gray-600">No teachers yet</p>
            </div>
            <div v-else class="space-y-3">
              <div v-for="teacher in recentTeachers" :key="teacher.id" class="bg-gradient-to-r from-white to-indigo-50 rounded-2xl p-4 border-2 border-indigo-200 hover:border-indigo-400 hover:shadow-lg transition-all">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-400 to-purple-600 flex items-center justify-center text-white font-bold">
                      {{ teacher.full_name?.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <h4 class="font-bold text-gray-900">{{ teacher.full_name }}</h4>
                      <p class="text-sm text-gray-600">{{ teacher.email }}</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <span v-if="teacher.is_class_teacher" class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-semibold">
                      Class Teacher: {{ teacher.managed_class }}
                    </span>
                    <button @click="resetPassword(teacher)" class="px-3 py-1 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 text-xs">
                      Reset Password
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Create Teacher Modal -->
  <div v-if="showCreateModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click="showCreateModal = false">
    <div class="bg-white rounded-3xl w-full max-w-2xl shadow-2xl" @click.stop>
      <div class="p-6 bg-gradient-to-r from-indigo-500 to-purple-500">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-3xl font-bold text-white mb-2">➕ Create Teacher Account</h3>
            <p class="text-white/90">Add a new teacher to the system</p>
          </div>
          <button @click="showCreateModal = false" class="w-12 h-12 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      
      <div class="p-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
            <input v-model="newTeacher.full_name" type="text" class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-indigo-500 focus:outline-none" placeholder="Enter full name">
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Email</label>
            <input v-model="newTeacher.email" type="email" class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-indigo-500 focus:outline-none" placeholder="teacher@school.ac.rw">
          </div>
          
          <div class="flex items-center gap-3 p-4 bg-indigo-50 rounded-xl border-2 border-indigo-200">
            <input v-model="newTeacher.is_class_teacher" type="checkbox" id="classTeacher" class="w-5 h-5">
            <label for="classTeacher" class="text-sm font-semibold text-gray-900">Designate as Class Teacher</label>
          </div>
          
          <div v-if="newTeacher.is_class_teacher">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Assign to Class ({{ classes.length }} available)</label>
            <select v-model="newTeacher.managed_class_id" class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-indigo-500 focus:outline-none">
              <option :value="null">Select a class...</option>
              <option v-for="(cls, idx) in classes" :key="idx" :value="cls.name">{{ cls.name }}</option>
            </select>
            <p v-if="classes.length === 0" class="text-xs text-red-600 mt-1">⚠️ No classes available. Loading...</p>
            <button v-if="classes.length === 0" @click="loadClasses" type="button" class="mt-2 text-xs text-indigo-600 underline">Reload Classes</button>
          </div>
        </div>
        
        <div v-if="createdCredentials" class="mt-6 p-4 bg-green-50 border-2 border-green-300 rounded-xl">
          <h4 class="font-bold text-green-900 mb-2">✅ Teacher Created Successfully!</h4>
          <div class="space-y-2 text-sm">
            <p><span class="font-semibold">Email:</span> {{ createdCredentials.email }}</p>
            <p><span class="font-semibold">Password:</span> <span class="font-mono bg-white px-2 py-1 rounded">{{ createdCredentials.password }}</span></p>
            <p class="text-xs text-green-700 mt-2">⚠️ Save these credentials! The password won't be shown again.</p>
          </div>
        </div>
        
        <div class="flex gap-3 mt-6">
          <button @click="createTeacher" :disabled="creating" class="flex-1 px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-xl hover:from-indigo-600 hover:to-purple-600 transition-all shadow-lg font-semibold disabled:opacity-50">
            {{ creating ? 'Creating...' : 'Create Teacher' }}
          </button>
          <button @click="showCreateModal = false" class="px-6 py-3 bg-gray-200 text-gray-700 rounded-xl hover:bg-gray-300 transition-all font-semibold">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- All Teachers Modal -->
  <div v-if="showTeachersModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click="showTeachersModal = false">
    <div class="bg-white rounded-3xl w-full max-w-5xl max-h-[85vh] overflow-hidden shadow-2xl" @click.stop>
      <div class="p-6 bg-gradient-to-r from-green-500 to-emerald-500">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-3xl font-bold text-white mb-2">👥 All Teachers</h3>
            <p class="text-white/90">{{ allTeachers.length }} teachers in the system</p>
          </div>
          <button @click="showTeachersModal = false" class="w-12 h-12 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      
      <div class="overflow-y-auto max-h-[calc(85vh-140px)] p-6">
        <div v-if="allTeachers.length === 0" class="text-center py-16">
          <div class="text-8xl mb-4">👨‍🏫</div>
          <p class="text-2xl font-bold text-gray-900 mb-2">No teachers yet</p>
        </div>
        <div v-else class="space-y-3">
          <div v-for="teacher in allTeachers" :key="teacher.id" class="bg-gradient-to-r from-white to-green-50 rounded-2xl p-5 border-2 border-green-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <div class="w-14 h-14 rounded-full bg-gradient-to-br from-green-400 to-emerald-600 flex items-center justify-center text-white font-bold text-xl">
                  {{ teacher.full_name?.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <h4 class="text-lg font-bold text-gray-900">{{ teacher.full_name }}</h4>
                  <p class="text-sm text-gray-600">{{ teacher.email }}</p>
                  <div v-if="teacher.is_class_teacher" class="mt-1">
                    <span class="px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-semibold">
                      Class Teacher: {{ teacher.managed_class?.name }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <button v-if="!teacher.is_class_teacher" @click="assignClassTeacher(teacher)" class="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 text-sm">
                  Assign Class
                </button>
                <button @click="resetPassword(teacher)" class="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 text-sm">
                  Reset Password
                </button>
                <button @click="deactivateTeacher(teacher)" class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 text-sm">
                  Deactivate
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Assign Class Modal -->
  <div v-if="showAssignModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click="showAssignModal = false">
    <div class="bg-white rounded-3xl w-full max-w-2xl shadow-2xl" @click.stop>
      <div class="p-6 bg-gradient-to-r from-purple-500 to-pink-500">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-3xl font-bold text-white mb-2">⭐ Assign Class Teacher</h3>
            <p class="text-white/90">{{ selectedTeacher?.full_name }}</p>
          </div>
          <button @click="showAssignModal = false" class="w-12 h-12 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      
      <div class="p-6">
        <label class="block text-sm font-semibold text-gray-700 mb-2">Select Class</label>
        <select v-model="selectedClassId" class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-purple-500 focus:outline-none mb-6">
          <option :value="null">Select a class...</option>
          <option v-for="(cls, idx) in classes" :key="idx" :value="cls.name">{{ cls.name }}</option>
        </select>
        <p v-if="classes.length === 0" class="text-xs text-red-600 mb-4">No classes available. Check school trades configuration.</p>
        
        <div class="flex gap-3">
          <button @click="confirmAssignClass" :disabled="!selectedClassId || assigning" class="flex-1 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all shadow-lg font-semibold disabled:opacity-50">
            {{ assigning ? 'Assigning...' : 'Assign Class' }}
          </button>
          <button @click="showAssignModal = false" class="px-6 py-3 bg-gray-200 text-gray-700 rounded-xl hover:bg-gray-300 transition-all font-semibold">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../utils/api'

const router = useRouter()
const authStore = useAuthStore()

const stats = ref({
  total_teachers: 0,
  total_students: 0,
  total_classes: 0,
  class_teachers: 0
})
const recentTeachers = ref([])
const allTeachers = ref([])
const classes = ref([])
const loading = ref(true)
const showCreateModal = ref(false)
const showTeachersModal = ref(false)
const showAssignModal = ref(false)
const creating = ref(false)
const assigning = ref(false)
const selectedTeacher = ref(null)
const selectedClassId = ref(null)
const createdCredentials = ref(null)

const newTeacher = ref({
  full_name: '',
  email: '',
  is_class_teacher: false,
  managed_class_id: null
})

function openCreateModal() {
  if (classes.value.length === 0) {
    loadClasses()
  }
  showCreateModal.value = true
}

async function loadDashboard() {
  try {
    const response = await api.get('/dos/dashboard')
    stats.value = response.data.stats
    recentTeachers.value = response.data.recent_teachers
  } catch (err) {
    console.error('Failed to load dashboard:', err)
    alert('Failed to load dashboard')
  } finally {
    loading.value = false
  }
}

async function loadAllTeachers() {
  try {
    const response = await api.get('/dos/teachers')
    allTeachers.value = response.data
    showTeachersModal.value = true
  } catch (err) {
    console.error('Failed to load teachers:', err)
    alert('Failed to load teachers')
  }
}

async function loadClasses() {
  try {
    const response = await api.get('/dos/school-classes')
    classes.value = response.data.classes || []
    console.log('Loaded classes:', classes.value.length, classes.value)
  } catch (err) {
    console.error('Failed to load classes:', err)
    classes.value = []
  }
}

async function createTeacher() {
  if (!newTeacher.value.full_name || !newTeacher.value.email) {
    alert('Please fill in all required fields')
    return
  }
  
  if (newTeacher.value.is_class_teacher && !newTeacher.value.managed_class_id) {
    alert('Please select a class for the class teacher')
    return
  }
  
  creating.value = true
  createdCredentials.value = null
  
  try {
    const response = await api.post('/dos/create-teacher', newTeacher.value)
    createdCredentials.value = response.data.credentials
    
    // Reset form
    newTeacher.value = {
      full_name: '',
      email: '',
      is_class_teacher: false,
      managed_class_id: null
    }
    
    // Reload dashboard
    await loadDashboard()
  } catch (err) {
    console.error('Failed to create teacher:', err)
    alert(err.response?.data?.detail || 'Failed to create teacher')
  } finally {
    creating.value = false
  }
}

async function assignClassTeacher(teacher) {
  selectedTeacher.value = teacher
  selectedClassId.value = null
  
  if (classes.value.length === 0) {
    await loadClasses()
  }
  
  showAssignModal.value = true
}

async function confirmAssignClass() {
  if (!selectedClassId.value) return
  
  assigning.value = true
  try {
    await api.put(`/dos/teachers/${selectedTeacher.value.id}/set-class-teacher?class_name=${encodeURIComponent(selectedClassId.value)}`)
    alert('✅ Class teacher assigned successfully!')
    showAssignModal.value = false
    await loadDashboard()
    if (showTeachersModal.value) {
      await loadAllTeachers()
    }
  } catch (err) {
    console.error('Failed to assign class:', err)
    alert('Failed to assign class teacher')
  } finally {
    assigning.value = false
  }
}

async function resetPassword(teacher) {
  if (!confirm(`Reset password for ${teacher.full_name}?`)) return
  
  try {
    const response = await api.post(`/dos/teachers/${teacher.id}/reset-password`)
    const creds = response.data.credentials
    alert(`✅ Password reset!\n\nEmail: ${creds.email}\nNew Password: ${creds.password}\n\nPlease save this password!`)
  } catch (err) {
    console.error('Failed to reset password:', err)
    alert('Failed to reset password')
  }
}

async function deactivateTeacher(teacher) {
  if (!confirm(`Deactivate ${teacher.full_name}? They will no longer be able to log in.`)) return
  
  try {
    await api.delete(`/dos/teachers/${teacher.id}`)
    alert('✅ Teacher deactivated successfully!')
    await loadAllTeachers()
    await loadDashboard()
  } catch (err) {
    console.error('Failed to deactivate teacher:', err)
    alert('Failed to deactivate teacher')
  }
}

onMounted(async () => {
  if (!authStore.isAuthenticated || authStore.user?.role !== 'admin') {
    router.push('/login')
    return
  }
  
  await loadClasses()
  await loadDashboard()
})
</script>
