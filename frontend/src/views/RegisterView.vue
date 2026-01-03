<template>
  <div class="min-h-screen relative flex items-center justify-center p-4 overflow-hidden">
    <!-- Rotating Background Images -->
    <transition-group name="fade" tag="div" class="absolute inset-0 z-0">
      <div 
        v-for="(image, index) in backgroundImages" 
        :key="image"
        v-show="currentBgIndex === index"
        class="absolute inset-0 bg-cover bg-center"
        :style="{ backgroundImage: `url(${image})` }"
      >
        <div class="absolute inset-0 bg-gradient-to-br from-blue-900/90 via-indigo-900/85 to-purple-900/90 dark:from-black/95 dark:via-gray-900/95 dark:to-black/95"></div>
      </div>
    </transition-group>
    <!-- Back Button & Theme Toggle -->
    <div class="absolute top-4 left-4 z-20 flex items-center gap-2">
      <router-link to="/" class="flex items-center space-x-2 px-4 py-2 bg-white rounded-lg shadow-md hover:shadow-lg transition-all">
        <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span class="text-sm font-semibold text-gray-700">Back</span>
      </router-link>
      <button @click="toggleTheme" class="flex items-center space-x-2 px-4 py-2 bg-white/10 backdrop-blur-md rounded-lg shadow-md hover:bg-white/20 transition-all border border-white/20">
        <SunIcon v-if="isDark" class="w-5 h-5 text-white" />
        <MoonIcon v-else class="w-5 h-5 text-white" />
      </button>
    </div>

    <div class="w-full max-w-2xl bg-white/95 dark:bg-gray-800/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-100 dark:border-gray-700 relative z-10 transition-colors duration-300">
      <!-- Header -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-800 dark:to-indigo-900 px-6 py-3 text-center transition-colors duration-300">
        <h1 class="text-lg font-bold text-white">Student Registration</h1>
        <p class="text-blue-100 dark:text-blue-200 text-xs">Join TSSANYWHERE - Learn Anytime, Anywhere</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="p-4 space-y-3">
        <!-- Personal Info -->
        <div class="grid grid-cols-3 gap-2">
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">Full Name</label>
            <input v-model="form.full_name" type="text" class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-1 focus:ring-blue-500" required placeholder="Full name" />
          </div>
          
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">Email</label>
            <input v-model="form.email" type="email" class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-1 focus:ring-blue-500" required placeholder="your@email.com" />
          </div>
          
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">Password</label>
            <input v-model="form.password" type="password" class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-1 focus:ring-blue-500" required minlength="6" placeholder="••••••••" />
          </div>
        </div>

        <!-- Location -->
        <div class="grid grid-cols-3 gap-2">
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">Province</label>
            <select v-model="selectedProvince" @change="onProvinceChange" class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-1 focus:ring-blue-500" required>
              <option value="">Select Province</option>
              <option v-for="province in provinces" :key="province.name" :value="province.name">{{ province.name }}</option>
            </select>
          </div>
          
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">District</label>
            <select v-model="selectedDistrict" @change="onDistrictChange" class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-1 focus:ring-blue-500" required :disabled="!selectedProvince">
              <option value="">Select District</option>
              <option v-for="district in districts" :key="district.name" :value="district.name">{{ district.name }}</option>
            </select>
          </div>
          
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">School</label>
            <select v-model="form.school_id" @change="onSchoolChange" class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-1 focus:ring-blue-500" required :disabled="!selectedDistrict">
              <option value="">Select School</option>
              <option v-for="school in schools" :key="school.id" :value="school.id">{{ school.name }}</option>
            </select>
          </div>
        </div>

        <!-- Student Fields -->
        <div v-if="form.school_id && selectedSchool" class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">Trade</label>
            <select v-model="form.selected_trade" class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-1 focus:ring-blue-500" required>
              <option value="">Select Trade</option>
              <optgroup v-for="(trades, category) in TVET_TRADES" :key="category" :label="category">
                <option v-for="trade in trades" :key="trade" :value="trade" v-if="selectedSchool.trades.includes(trade)">{{ trade }}</option>
              </optgroup>
            </select>
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">Level</label>
            <select v-model="form.selected_level" class="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-1 focus:ring-blue-500" required>
              <option value="">Select Level</option>
              <option value="Level 1">Level 1</option>
              <option value="Level 2">Level 2</option>
              <option value="Level 3">Level 3</option>
              <option value="Level 4">Level 4</option>
              <option value="Level 5">Level 5</option>
              <option value="Level 6">Level 6</option>
            </select>
          </div>
        </div>

        <!-- Language -->
        <div>
          <label class="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">Language</label>
          <div class="grid grid-cols-3 gap-2">
            <label class="cursor-pointer">
              <input type="radio" v-model="form.locale" value="rw" class="peer sr-only" />
              <div class="px-2 py-1.5 text-xs text-center border-2 border-gray-300 rounded-lg peer-checked:border-blue-600 peer-checked:bg-blue-50">🇷🇼 Kinyarwanda</div>
            </label>
            <label class="cursor-pointer">
              <input type="radio" v-model="form.locale" value="en" class="peer sr-only" />
              <div class="px-2 py-1.5 text-xs text-center border-2 border-gray-300 rounded-lg peer-checked:border-blue-600 peer-checked:bg-blue-50">🇬🇧 English</div>
            </label>
            <label class="cursor-pointer">
              <input type="radio" v-model="form.locale" value="fr" class="peer sr-only" />
              <div class="px-2 py-1.5 text-xs text-center border-2 border-gray-300 rounded-lg peer-checked:border-blue-600 peer-checked:bg-blue-50">🇫🇷 Français</div>
            </label>
          </div>
        </div>

        <button type="submit" class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-2 rounded-lg font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all" :disabled="loading">
          <span v-if="!loading">Register →</span>
          <span v-else>Processing...</span>
        </button>
        
        <p v-if="error" class="text-red-600 text-xs text-center bg-red-50 p-2 rounded-lg">{{ error }}</p>
        
        <div class="space-y-2">
          <p class="text-center text-xs text-gray-600 dark:text-gray-400">
            Already have an account?
            <router-link to="/login" class="text-blue-600 hover:text-blue-700 font-semibold">Login</router-link>
          </p>
          <p class="text-center text-xs text-gray-600 dark:text-gray-400">
            <router-link to="/" class="text-blue-600 hover:text-blue-700 font-semibold">Back to Home</router-link>
          </p>
        </div>
      </form>
    </div>

    <!-- Success Dialog -->
    <div v-if="showSuccess" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-6 max-w-sm mx-4 text-center">
        <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
          <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-2">Success!</h3>
        <p class="text-sm text-gray-600 mb-4">Your account has been created.</p>
        <button @click="goToLogin" class="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700">Go to Login</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { TVET_TRADES } from '../data/trades'
import { MoonIcon, SunIcon } from '@heroicons/vue/24/outline'

const router = useRouter()

const form = ref({
  email: '',
  password: '',
  full_name: '',
  role: 'STUDENT',
  school_id: '',
  locale: 'rw',
  selected_trade: '',
  selected_level: ''
})

const selectedProvince = ref('')
const selectedDistrict = ref('')
const provinces = ref([])
const districts = ref([])
const schools = ref([])
const selectedSchool = ref(null)
const loading = ref(false)
const error = ref('')
const showSuccess = ref(false)
const isDark = ref(false)
const currentBgIndex = ref(0)
let bgIntervalId = null

const backgroundImages = ref([
  '/images to use/DSC_0106.JPG',
  '/images to use/IMG-20241006-WA0079.jpg',
  '/images to use/IMG-20241006-WA0051.jpg',
  '/images to use/home_page_3.jpg'
])

const API_URL = 'https://rwanda-edu-platform.onrender.com'
// Updated: 2025-12-27

function toggleTheme() {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(async () => {
  // Initialize theme
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
  
  // Start background rotation
  bgIntervalId = setInterval(() => {
    currentBgIndex.value = (currentBgIndex.value + 1) % backgroundImages.value.length
  }, 4000)
  
  try {
    const response = await axios.get(`${API_URL}/api/v1/locations/provinces`)
    provinces.value = response.data
  } catch (err) {
    console.error('Error loading provinces:', err)
  }
})

onUnmounted(() => {
  if (bgIntervalId) {
    clearInterval(bgIntervalId)
  }
})

async function onProvinceChange() {
  selectedDistrict.value = ''
  districts.value = []
  schools.value = []
  form.value.school_id = ''
  
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
  form.value.school_id = ''
  selectedSchool.value = null
  
  if (selectedDistrict.value && selectedProvince.value) {
    try {
      const response = await axios.get(`${API_URL}/api/v1/registration/schools/${selectedProvince.value}/${selectedDistrict.value}`)
      schools.value = response.data.schools
    } catch (err) {
      console.error('Error loading schools:', err)
      error.value = 'Failed to load schools'
    }
  }
}

function onSchoolChange() {
  const school = schools.value.find(s => s.id === parseInt(form.value.school_id))
  selectedSchool.value = school
  form.value.selected_trade = ''
  form.value.selected_level = ''
}

async function handleRegister() {
  loading.value = true
  error.value = ''
  
  try {
    const payload = {
      full_name: form.value.full_name,
      email: form.value.email,
      password: form.value.password,
      role: form.value.role,
      school_id: parseInt(form.value.school_id),
      province: selectedProvince.value,
      district: selectedDistrict.value,
      locale: form.value.locale,
      selected_trade: form.value.selected_trade || null,
      selected_level: form.value.selected_level || null
    }
    
    const response = await axios.post(`${API_URL}/api/v1/auth/register`, payload)
    if (response.status === 200) {
      showSuccess.value = true
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed'
  } finally {
    loading.value = false
  }
}

function goToLogin() {
  showSuccess.value = false
  router.push('/login')
}
</script>

<!-- Force refresh -->


<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 2s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}
</style>
" / /   F o r c e   r e b u i l d "      
 