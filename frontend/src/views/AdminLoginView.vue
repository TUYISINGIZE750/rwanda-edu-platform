<template>
  <div class="min-h-screen bg-gradient-to-br from-red-50 via-white to-red-100 flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden">
      <!-- Header -->
      <div class="bg-gradient-to-r from-red-600 to-red-700 px-8 py-8 text-center">
        <div class="w-16 h-16 bg-white rounded-2xl flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-white mb-2">DOS Portal</h1>
        <p class="text-red-100">Deputy of Studies Access</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="p-8 space-y-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
            <input 
              v-model="form.email" 
              type="email" 
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all" 
              required 
              placeholder="Enter your DOS email"
              :class="{ 'border-red-300': error }"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <input 
              v-model="form.password" 
              type="password" 
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all" 
              required 
              placeholder="Enter your password"
              :class="{ 'border-red-300': error }"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Province</label>
            <select v-model="selectedProvince" @change="onProvinceChange" required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent">
              <option value="">Select Province</option>
              <option v-for="province in provinces" :key="province.name" :value="province.name">
                {{ province.name }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">District</label>
            <select v-model="selectedDistrict" @change="onDistrictChange" required :disabled="!selectedProvince"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent">
              <option value="">Select District</option>
              <option v-for="district in districts" :key="district.name" :value="district.name">
                {{ district.name }}
              </option>
            </select>
          </div>

          <div v-if="selectedDistrict">
            <label class="block text-sm font-medium text-gray-700 mb-2">School</label>
            <select v-model="selectedSchoolId" required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent">
              <option value="">Select School</option>
              <option v-for="school in schools" :key="school.id" :value="school.id">
                {{ school.name }} ({{ school.type }})
              </option>
            </select>
            <div v-if="selectedDistrict" class="mt-2">
              <p v-if="loadingSchools" class="text-xs text-red-600 flex items-center">
                <svg class="animate-spin w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Loading schools...
              </p>
              <p v-else-if="schools.length > 0" class="text-xs text-green-600">✓ {{ schools.length }} schools available</p>
            </div>
          </div>
        </div>

        <button 
          type="submit" 
          class="w-full bg-gradient-to-r from-red-600 to-red-700 text-white py-3 px-4 rounded-lg font-semibold hover:from-red-700 hover:to-red-800 focus:ring-4 focus:ring-red-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02]" 
          :disabled="loading || !selectedSchoolId"
        >
          <span v-if="!loading">Sign In as DOS</span>
          <span v-else class="flex items-center justify-center">
            <svg class="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Signing In...
          </span>
        </button>
        
        <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-red-700 text-sm">{{ error }}</p>
          </div>
        </div>
        
        <div class="text-center">
          <p class="text-sm text-gray-600">
            Not a DOS? 
            <router-link to="/login" class="text-red-600 hover:text-red-700 font-semibold hover:underline transition-colors">
              Regular Login
            </router-link>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: ''
})

const selectedProvince = ref('')
const selectedDistrict = ref('')
const selectedSchoolId = ref('')
const provinces = ref([])
const districts = ref([])
const schools = ref([])
const loadingSchools = ref(false)
const loading = ref(false)
const error = ref('')

const API_URL = 'https://rwanda-edu-platform.onrender.com'

onMounted(async () => {
  await loadProvinces()
})

async function loadProvinces() {
  try {
    const response = await axios.get(`${API_URL}/api/v1/locations/provinces`)
    provinces.value = response.data
  } catch (err) {
    console.error('Error loading provinces:', err)
  }
}

async function onProvinceChange() {
  selectedDistrict.value = ''
  districts.value = []
  schools.value = []
  selectedSchoolId.value = ''
  
  if (selectedProvince.value) {
    try {
      const response = await axios.get(`${API_URL}/api/v1/locations/districts/${selectedProvince.value}`)
      districts.value = response.data
    } catch (err) {
      console.error('Error loading districts:', err)
    }
  }
}

async function onDistrictChange() {
  schools.value = []
  selectedSchoolId.value = ''
  
  if (!selectedDistrict.value || !selectedProvince.value) return
  
  loadingSchools.value = true
  
  try {
    let apiProvince = selectedProvince.value
    if (apiProvince === 'Southern Province') apiProvince = 'South'
    if (apiProvince === 'Western Province') apiProvince = 'West'
    if (apiProvince === 'Northern Province') apiProvince = 'North'
    if (apiProvince === 'Eastern Province') apiProvince = 'East'
    if (apiProvince === 'Kigali City') apiProvince = 'Kigali city'
    
    const response = await fetch(`${API_URL}/api/v1/schools-by-district/district/${apiProvince}/${selectedDistrict.value}`)
    const data = await response.json()
    
    schools.value = data.schools || []
  } catch (error) {
    console.error('API Error:', error)
    schools.value = []
  } finally {
    loadingSchools.value = false
  }
}

async function handleLogin() {
  loading.value = true
  error.value = ''
  
  try {
    await authStore.login(form.value.email, form.value.password)
    
    // Verify user is admin
    if (authStore.user?.role?.toLowerCase() !== 'admin') {
      error.value = 'Access denied. DOS credentials required.'
      authStore.logout()
      return
    }
    
    // Update user with selected school
    const selectedSchool = schools.value.find(s => s.id === parseInt(selectedSchoolId.value))
    const updatedUser = {
      ...authStore.user,
      school_id: parseInt(selectedSchoolId.value),
      province: selectedProvince.value,
      district: selectedDistrict.value,
      school_name: selectedSchool.name
    }
    
    localStorage.setItem('user', JSON.stringify(updatedUser))
    authStore.user = updatedUser
    
    router.push('/dos-dashboard')
    
  } catch (err) {
    console.error('Login error:', err)
    error.value = err.response?.data?.detail || 'Invalid DOS credentials'
  } finally {
    loading.value = false
  }
}
</script>