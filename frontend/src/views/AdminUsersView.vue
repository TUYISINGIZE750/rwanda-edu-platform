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
            <h1 class="text-xl font-semibold text-gray-900">Manage Users</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Filters -->
      <div class="bg-white rounded-lg shadow p-4 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input v-model="search" @input="loadUsers" placeholder="Search users..." 
                 class="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
          <select v-model="filterRole" @change="loadUsers" class="px-4 py-2 border rounded-lg">
            <option value="">All Roles</option>
            <option value="STUDENT">Students</option>
            <option value="TEACHER">Teachers</option>
            <option value="ADMIN">Admins</option>
          </select>
          <select v-model="filterGrade" @change="loadUsers" class="px-4 py-2 border rounded-lg">
            <option value="">All Grades</option>
            <option v-for="g in [1,2,3,4,5,6]" :key="g" :value="g">Level {{ g }}</option>
          </select>
          <button @click="showCreateModal = true" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
            Add User
          </button>
        </div>
      </div>

      <!-- Users Table -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Level</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ user.full_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ user.email }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs rounded-full" :class="roleClass(user.role)">
                  {{ user.role }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ user.grade || '-' }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs rounded-full" :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm space-x-2">
                <button @click="editUser(user)" class="text-blue-600 hover:text-blue-800">Edit</button>
                <button v-if="user.role === 'TEACHER'" @click="assignTeacher(user)" 
                        class="text-green-600 hover:text-green-800">Assign</button>
                <button v-if="user.role !== 'ADMIN'" @click="toggleStatus(user)" 
                        class="text-red-600 hover:text-red-800">
                  {{ user.is_active ? 'Deactivate' : 'Activate' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create User Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <h3 class="text-lg font-semibold mb-4">Add New User</h3>
        <div class="space-y-4">
          <input v-model="newUser.full_name" placeholder="Full Name" class="w-full px-4 py-2 border rounded-lg">
          <input v-model="newUser.email" type="email" placeholder="Email" class="w-full px-4 py-2 border rounded-lg">
          <input v-model="newUser.password" type="password" placeholder="Password" class="w-full px-4 py-2 border rounded-lg">
          <select v-model="newUser.role" @change="onRoleChange" class="w-full px-4 py-2 border rounded-lg">
            <option value="">Select Role</option>
            <option value="STUDENT">Student</option>
            <option value="TEACHER">Teacher</option>
            <option value="ADMIN">Admin</option>
          </select>
          
          <!-- Location Fields -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Province</label>
            <select v-model="newUser.province" @change="onProvinceChange" class="w-full px-4 py-2 border rounded-lg">
              <option value="">Select province...</option>
              <option v-for="prov in provinces" :key="prov" :value="prov">{{ prov }}</option>
            </select>
          </div>
          
          <div v-if="newUser.province">
            <label class="block text-sm font-medium text-gray-700 mb-2">District</label>
            <select v-model="newUser.district" @change="onDistrictChange" class="w-full px-4 py-2 border rounded-lg">
              <option value="">Select district...</option>
              <option v-for="dist in districts" :key="dist" :value="dist">{{ dist }}</option>
            </select>
          </div>
          
          <div v-if="newUser.district">
            <label class="block text-sm font-medium text-gray-700 mb-2">School</label>
            <select v-model="newUser.school_id" @change="onSchoolChange" class="w-full px-4 py-2 border rounded-lg">
              <option :value="null">Select school...</option>
              <option v-for="school in schools" :key="school.id" :value="school.id">
                {{ school.name }}
              </option>
            </select>
          </div>
          
          <!-- Student Fields -->
          <template v-if="newUser.role === 'STUDENT'">
            <input v-model.number="newUser.grade" type="number" placeholder="Level (1-6)" class="w-full px-4 py-2 border rounded-lg">
          </template>
          
          <!-- Teacher Fields -->
          <template v-if="newUser.role === 'TEACHER'">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Department/Trade</label>
              <select v-model="newUser.selected_trade" class="w-full px-4 py-2 border rounded-lg">
                <option value="">Select department...</option>
                <option v-for="trade in schoolTrades" :key="trade" :value="trade">{{ trade }}</option>
              </select>
              <p class="text-xs text-gray-500 mt-1">Teacher will see only students in this department</p>
            </div>
            
            <div class="flex items-center space-x-2">
              <input v-model="newUser.is_class_teacher" type="checkbox" id="newIsClassTeacher" 
                     @change="onClassTeacherChange" class="rounded">
              <label for="newIsClassTeacher" class="text-sm font-medium text-gray-700">
                Is Class Teacher? (Full permissions)
              </label>
            </div>
            
            <div v-if="newUser.is_class_teacher">
              <label class="block text-sm font-medium text-gray-700 mb-2">Managed Class</label>
              <select v-model="newUser.managed_class_id" class="w-full px-4 py-2 border rounded-lg">
                <option :value="null">Select class to manage...</option>
                <option v-for="group in availableClasses" :key="group.id" :value="group.id">
                  {{ group.name }} ({{ group.type }})
                </option>
              </select>
              <p class="text-xs text-gray-500 mt-1">Class teacher can create modules and manage students</p>
            </div>
          </template>
        </div>
        <div class="flex justify-end space-x-3 mt-6">
          <button @click="showCreateModal = false" class="px-4 py-2 text-gray-600 hover:text-gray-800">Cancel</button>
          <button @click="createUser" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Create</button>
        </div>
      </div>
    </div>

    <!-- Edit User Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-4">Edit User</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
            <input v-model="editingUser.full_name" class="w-full px-4 py-2 border rounded-lg">
          </div>
          <div v-if="editingUser.role === 'STUDENT'">
            <label class="block text-sm font-medium text-gray-700 mb-2">Level</label>
            <input v-model.number="editingUser.grade" type="number" min="1" max="6" class="w-full px-4 py-2 border rounded-lg">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select v-model="editingUser.is_active" class="w-full px-4 py-2 border rounded-lg">
              <option :value="1">Active</option>
              <option :value="0">Inactive</option>
            </select>
          </div>
        </div>
        <div class="flex justify-end space-x-3 mt-6">
          <button @click="showEditModal = false" class="px-4 py-2 text-gray-600 hover:text-gray-800">Cancel</button>
          <button @click="updateUser" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Save Changes</button>
        </div>
      </div>
    </div>

    <!-- Assign Teacher Modal -->
    <div v-if="showAssignModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-4">Assign Teacher to Class/Group</h3>
        <p class="text-sm text-gray-600 mb-4">Teacher: <strong>{{ assigningTeacher?.full_name }}</strong></p>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Select Class/Group</label>
            <select v-model="assignData.group_id" class="w-full px-4 py-2 border rounded-lg">
              <option value="">Choose a class or group...</option>
              <option v-for="group in availableGroups" :key="group.id" :value="group.id">
                {{ group.name }} ({{ group.type }})
              </option>
            </select>
          </div>
          <div class="flex items-center">
            <input v-model="assignData.is_class_teacher" type="checkbox" id="isClassTeacher" class="mr-2">
            <label for="isClassTeacher" class="text-sm font-medium text-gray-700">
              Assign as Class Teacher (full permissions)
            </label>
          </div>
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <p class="text-xs text-blue-800">
              ✓ Teacher will receive instant notification<br>
              ✓ Teacher will get immediate access to the class/group
            </p>
          </div>
        </div>
        <div class="flex justify-end space-x-3 mt-6">
          <button @click="showAssignModal = false" class="px-4 py-2 text-gray-600 hover:text-gray-800">Cancel</button>
          <button @click="submitAssignment" :disabled="!assignData.group_id" 
                  class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">
            Assign Teacher
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../utils/api'

const authStore = useAuthStore()
const users = ref([])
const search = ref('')
const filterRole = ref('')
const filterGrade = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showAssignModal = ref(false)
const newUser = ref({ 
  full_name: '', 
  email: '', 
  password: '', 
  role: '', 
  grade: null,
  province: '',
  district: '',
  school_id: null,
  selected_trade: '',
  selected_level: '',
  is_class_teacher: false,
  managed_class_id: null
})
const provinces = ref([])
const districts = ref([])
const schools = ref([])
const schoolTrades = ref([])
const availableClasses = ref([])
const editingUser = ref({ id: null, full_name: '', role: '', grade: null, is_active: 1 })
const assigningTeacher = ref(null)
const assignData = ref({ teacher_id: null, group_id: '', is_class_teacher: false })
const availableGroups = ref([])

onMounted(() => {
  loadUsers()
  loadProvinces()
})

async function loadProvinces() {
  try {
    const res = await api.get('/locations/provinces')
    provinces.value = res.data.map(p => p.name)
  } catch (err) {
    console.error('Failed to load provinces:', err)
  }
}

async function onProvinceChange() {
  districts.value = []
  schools.value = []
  newUser.value.district = ''
  newUser.value.school_id = null
  schoolTrades.value = []
  
  if (newUser.value.province) {
    try {
      const res = await api.get(`/locations/districts/${encodeURIComponent(newUser.value.province)}`)
      districts.value = res.data.map(d => d.name)
    } catch (err) {
      console.error('Failed to load districts:', err)
    }
  }
}

async function onDistrictChange() {
  schools.value = []
  newUser.value.school_id = null
  schoolTrades.value = []
  
  if (newUser.value.district) {
    try {
      const res = await api.get(`/locations/schools/district/${encodeURIComponent(newUser.value.province)}/${encodeURIComponent(newUser.value.district)}`)
      schools.value = res.data
      console.log('Loaded schools:', schools.value.length, schools.value)
    } catch (err) {
      console.error('Failed to load schools:', err)
    }
  }
}

async function onSchoolChange() {
  schoolTrades.value = []
  newUser.value.selected_trade = ''
  if (newUser.value.school_id) {
    console.log('Loading trades for school:', newUser.value.school_id)
    await loadSchoolTradesForSchool(newUser.value.school_id)
  }
}

async function loadSchoolTradesForSchool(schoolId) {
  try {
    const res = await api.get(`/teacher/school-info`)
    // For now, get trades from the selected school object
    const selectedSchool = schools.value.find(s => s.id === schoolId)
    schoolTrades.value = selectedSchool?.trades || []
    console.log('Loaded trades:', schoolTrades.value)
  } catch (err) {
    console.error('Failed to load school trades:', err)
    // Fallback: try to get from school object
    const selectedSchool = schools.value.find(s => s.id === schoolId)
    schoolTrades.value = selectedSchool?.trades || []
  }
}

async function loadUsers() {
  try {
    const params = new URLSearchParams()
    if (search.value) params.append('search', search.value)
    if (filterRole.value) params.append('role', filterRole.value)
    if (filterGrade.value) params.append('grade', filterGrade.value)
    
    const res = await api.get(`/admin/users?${params}`)
    users.value = res.data
  } catch (err) {
    console.error('Failed to load users:', err)
  }
}

async function createUser() {
  try {
    const payload = {
      full_name: newUser.value.full_name,
      email: newUser.value.email,
      password: newUser.value.password,
      role: newUser.value.role,
      school_id: newUser.value.school_id,
      province: newUser.value.province,
      district: newUser.value.district,
      locale: 'en'
    }
    
    if (newUser.value.role === 'STUDENT' && newUser.value.grade) {
      payload.grade = newUser.value.grade
    }
    
    if (newUser.value.role === 'TEACHER') {
      payload.selected_trade = newUser.value.selected_trade || null
      payload.is_class_teacher = newUser.value.is_class_teacher
      payload.managed_class_id = newUser.value.managed_class_id || null
    }
    
    await api.post('/admin/users', payload)
    alert('User created successfully!')
    showCreateModal.value = false
    newUser.value = { 
      full_name: '', 
      email: '', 
      password: '', 
      role: '', 
      grade: null,
      province: '',
      district: '',
      school_id: null,
      selected_trade: '',
      selected_level: '',
      is_class_teacher: false,
      managed_class_id: null
    }
    loadUsers()
  } catch (err) {
    const errorMsg = err.response?.data?.detail
    if (Array.isArray(errorMsg)) {
      alert(errorMsg.map(e => `${e.loc?.join('.')}: ${e.msg}`).join('\n'))
    } else {
      alert(errorMsg || 'Failed to create user')
    }
  }
}

async function onRoleChange() {
  if (newUser.value.role === 'TEACHER' && newUser.value.is_class_teacher) {
    await loadAvailableClasses()
  }
}

async function onClassTeacherChange() {
  if (newUser.value.is_class_teacher) {
    await loadAvailableClasses()
  } else {
    newUser.value.managed_class_id = null
  }
}

async function loadAvailableClasses() {
  try {
    const res = await api.get('/admin/groups/available')
    availableClasses.value = res.data.filter(g => g.type === 'CLASS')
  } catch (err) {
    console.error('Failed to load classes:', err)
  }
}

async function toggleStatus(user) {
  try {
    await api.put(`/admin/users/${user.id}`, { is_active: user.is_active ? 0 : 1 })
    loadUsers()
  } catch (err) {
    alert('Failed to update user status')
  }
}

function editUser(user) {
  editingUser.value = {
    id: user.id,
    full_name: user.full_name,
    role: user.role,
    grade: user.grade,
    is_active: user.is_active ? 1 : 0
  }
  showEditModal.value = true
}

async function updateUser() {
  try {
    await api.put(`/admin/users/${editingUser.value.id}`, {
      full_name: editingUser.value.full_name,
      grade: editingUser.value.grade,
      is_active: editingUser.value.is_active
    })
    showEditModal.value = false
    loadUsers()
  } catch (err) {
    alert('Failed to update user')
  }
}

function roleClass(role) {
  const classes = {
    STUDENT: 'bg-blue-100 text-blue-800',
    TEACHER: 'bg-green-100 text-green-800',
    ADMIN: 'bg-purple-100 text-purple-800'
  }
  return classes[role] || 'bg-gray-100 text-gray-800'
}

async function assignTeacher(teacher) {
  assigningTeacher.value = teacher
  assignData.value = { teacher_id: teacher.id, group_id: '', is_class_teacher: false }
  
  // Load available groups
  try {
    const res = await api.get('/admin/groups/available')
    availableGroups.value = res.data
    showAssignModal.value = true
  } catch (err) {
    alert('Failed to load groups')
  }
}

async function submitAssignment() {
  try {
    const res = await api.post('/admin/assign-teacher', assignData.value)
    alert(res.data.message + '\n\nTeacher has been notified instantly!')
    showAssignModal.value = false
    loadUsers()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to assign teacher')
  }
}
</script>
