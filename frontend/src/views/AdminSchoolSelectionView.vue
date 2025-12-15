<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden">
      <div class="bg-gradient-to-r from-red-600 to-red-700 px-8 py-6 text-center">
        <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center mx-auto mb-3">
          <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-white mb-1">DOS School Selection</h1>
        <p class="text-red-100 text-sm">Select your assigned school</p>
      </div>
      
      <form @submit.prevent="selectSchool" class="p-8 space-y-6">
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

        <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
          <p class="text-red-600 text-sm">{{ error }}</p>
        </div>

        <button type="submit" :disabled="!selectedSchoolId || loading"
                class="w-full bg-gradient-to-r from-red-600 to-red-700 text-white py-3 px-4 rounded-lg font-semibold hover:from-red-700 hover:to-red-800 disabled:opacity-50">
          <span v-if="!loading">Continue to Dashboard</span>
          <span v-else class="flex items-center justify-center">
            <svg class="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Setting up...
          </span>
        </button>
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

const selectedProvince = ref('')
const selectedDistrict = ref('')
const selectedSchoolId = ref('')
const provinces = ref([])
const districts = ref([])
const schools = ref([])
const loadingSchools = ref(false)
const loading = ref(false)
const error = ref('')

const API_URL = 'http://localhost:8080'

onMounted(async () => {
  if (authStore.user?.role?.toLowerCase() !== 'admin') {
    router.push('/login')
    return
  }
  await loadProvinces()
})

async function loadProvinces() {
  try {
    const response = await axios.get(`${API_URL}/api/v1/locations/provinces`)
    provinces.value = response.data
  } catch (err) {
    console.error('Error loading provinces:', err)
    error.value = 'Failed to load provinces'
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
      error.value = 'Failed to load districts'
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
    error.value = 'Failed to load schools'
  } finally {
    loadingSchools.value = false
  }
}

async function selectSchool() {
  loading.value = true
  error.value = ''
  
  try {
    const selectedSchool = schools.value.find(s => s.id === parseInt(selectedSchoolId.value))
    
    // Update user's school assignment
    const updatedUser = {
      ...authStore.user,
      school_id: parseInt(selectedSchoolId.value),
      province: selectedProvince.value,
      district: selectedDistrict.value,
      school_name: selectedSchool.name
    }
    
    // Store school selection
    localStorage.setItem('user', JSON.stringify(updatedUser))
    authStore.user = updatedUser
    
    router.push('/home')
    
  } catch (err) {
    console.error('School selection error:', err)
    error.value = 'Failed to select school'
  } finally {
    loading.value = false
  }
}
</script>