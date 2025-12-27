<template>
  <div class="min-h-screen relative overflow-hidden flex items-center justify-center p-6 dark:bg-gray-900 transition-colors duration-300">
    <!-- Back Button -->
    <router-link to="/" class="fixed top-4 left-4 z-50 flex items-center gap-2 px-4 py-2 bg-white/90 dark:bg-gray-800/90 backdrop-blur-md rounded-xl shadow-lg hover:shadow-xl transition-all border border-gray-200 dark:border-gray-700">
      <svg class="w-5 h-5 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
      </svg>
      <span class="text-sm font-semibold text-gray-700 dark:text-gray-300">Back</span>
    </router-link>
    
    <!-- Theme Toggle -->
    <button @click="toggleTheme" class="fixed top-4 right-4 z-50 p-3 bg-white/90 dark:bg-gray-800/90 backdrop-blur-md rounded-xl shadow-lg hover:shadow-xl transition-all border border-gray-200 dark:border-gray-700">
      <SunIcon v-if="isDark" class="w-6 h-6 text-yellow-500" />
      <MoonIcon v-else class="w-6 h-6 text-indigo-600" />
    </button>
    
    <!-- Rotating Background Images -->
    <div class="absolute inset-0 z-0">
      <div 
        v-for="(image, index) in backgroundImages" 
        :key="index"
        v-show="currentBgIndex === index"
        class="absolute inset-0 bg-cover bg-center transition-opacity duration-1000"
        :style="{ backgroundImage: `url('${image}')` }"
      >
        <div class="absolute inset-0 bg-gradient-to-br from-blue-900/80 via-indigo-900/75 to-purple-900/80 dark:from-black/90 dark:via-gray-900/90 dark:to-black/90"></div>
      </div>
    </div>

    <div class="relative z-10 w-full max-w-3xl bg-white/95 dark:bg-gray-800/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 overflow-hidden transition-colors duration-300">
      <!-- Header -->
      <div class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 px-6 py-5 text-center">
        <div class="flex items-center justify-center gap-2 mb-2">
          <div class="w-10 h-10 bg-white/20 backdrop-blur-lg rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
            </svg>
          </div>
        </div>
        <h1 class="text-2xl font-bold text-white mb-1">Student Registration</h1>
        <p class="text-blue-100 text-sm">Join Rwanda's Premier TVET Education Platform</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="p-6 space-y-5">
        <!-- Personal Info -->
        <div>
          <h3 class="text-base font-bold text-gray-900 mb-3 flex items-center gap-2">
            <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Personal Information
          </h3>
          <div class="grid grid-cols-3 gap-3">
            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">Full Name</label>
              <input v-model="form.full_name" type="text" class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all" required placeholder="Enter your full name" />
            </div>
            
            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">Email Address</label>
              <input v-model="form.email" type="email" class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all" required placeholder="your@email.com" />
            </div>

            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">Password</label>
              <input v-model="form.password" type="password" class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all" required minlength="6" placeholder="••••••••" />
            </div>
          </div>
        </div>

        <!-- Location -->
        <div>
          <h3 class="text-base font-bold text-gray-900 mb-3 flex items-center gap-2">
            <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            School Location
          </h3>
          <div class="grid grid-cols-3 gap-3">
            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">Province</label>
              <select v-model="selectedProvince" @change="onProvinceChange" class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all" required>
                <option value="">Select Province</option>
                <option v-for="province in provinces" :key="province.name" :value="province.name">{{ province.name }}</option>
              </select>
            </div>
            
            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">District</label>
              <select v-model="selectedDistrict" @change="onDistrictChange" class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all" required :disabled="!selectedProvince">
                <option value="">Select District</option>
                <option v-for="district in districts" :key="district.name" :value="district.name">{{ district.name }}</option>
              </select>
            </div>
            
            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">School</label>
              <select v-model="form.school_id" @change="onSchoolChange" class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all" required :disabled="!selectedDistrict">
                <option value="">Select School</option>
                <option v-for="school in schools" :key="school.id" :value="school.id">{{ school.name }}</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Student Fields -->
        <div v-if="form.school_id && selectedSchool">
          <h3 class="text-base font-bold text-gray-900 mb-3 flex items-center gap-2">
            <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            Academic Details
          </h3>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">Trade Program</label>
              <select v-model="form.selected_trade" class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all" required>
                <option value="">Select Trade</option>
                <option v-for="trade in selectedSchool.trades" :key="trade" :value="trade">{{ trade }}</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">Level</label>
              <select v-model="form.selected_level" class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all" required>
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
        </div>

        <!-- Language -->
        <div>
          <h3 class="text-base font-bold text-gray-900 mb-3 flex items-center gap-2">
            <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
            </svg>
            Preferred Language
          </h3>
          <div class="grid grid-cols-3 gap-3">
            <label class="cursor-pointer">
              <input type="radio" v-model="form.locale" value="rw" class="peer sr-only" />
              <div class="px-3 py-2.5 text-sm text-center border-2 border-gray-300 rounded-lg peer-checked:border-blue-600 peer-checked:bg-blue-50 transition-all hover:border-blue-400">
                <div class="text-2xl mb-1">🇷🇼</div>
                <div class="font-semibold text-xs">Kinyarwanda</div>
              </div>
            </label>
            <label class="cursor-pointer">
              <input type="radio" v-model="form.locale" value="en" class="peer sr-only" />
              <div class="px-3 py-2.5 text-sm text-center border-2 border-gray-300 rounded-lg peer-checked:border-blue-600 peer-checked:bg-blue-50 transition-all hover:border-blue-400">
                <div class="text-2xl mb-1">🇬🇧</div>
                <div class="font-semibold text-xs">English</div>
              </div>
            </label>
            <label class="cursor-pointer">
              <input type="radio" v-model="form.locale" value="fr" class="peer sr-only" />
              <div class="px-3 py-2.5 text-sm text-center border-2 border-gray-300 rounded-lg peer-checked:border-blue-600 peer-checked:bg-blue-50 transition-all hover:border-blue-400">
                <div class="text-2xl mb-1">🇫🇷</div>
                <div class="font-semibold text-xs">Français</div>
              </div>
            </label>
          </div>
        </div>

        <button type="submit" class="w-full bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white py-2.5 rounded-lg font-semibold text-base hover:shadow-xl transform hover:scale-[1.01] transition-all disabled:opacity-50 disabled:cursor-not-allowed" :disabled="loading">
          <span v-if="!loading" class="flex items-center justify-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Create My Account
          </span>
          <span v-else class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Processing...
          </span>
        </button>
        
        <p v-if="error" class="text-red-600 text-sm text-center bg-red-50 p-3 rounded-lg border-2 border-red-200 font-medium">
          {{ error }}
        </p>
        
        <div class="space-y-2">
          <p class="text-center text-sm text-gray-600">
            Already have an account?
            <router-link to="/login" class="text-blue-600 hover:text-blue-700 font-semibold hover:underline ml-1">
              Sign In Here
            </router-link>
          </p>
          <p class="text-center text-sm text-gray-600">
            <router-link to="/" class="text-blue-600 hover:text-blue-700 font-semibold hover:underline">
              Back to Home
            </router-link>
          </p>
        </div>
      </form>
    </div>
    
    <!-- Success Dialog -->
    <div v-if="showSuccess" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-3xl p-10 max-w-md mx-4 text-center shadow-2xl transform animate-bounce-in">
        <div class="w-20 h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>
        <h3 class="text-3xl font-bold text-gray-900 mb-3">Welcome Aboard! 🎉</h3>
        <p class="text-gray-600 text-lg mb-8">Your account has been created successfully. You're now part of Rwanda's TVET community!</p>
        <button @click="goToLogin" class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 px-6 rounded-xl font-bold text-lg hover:shadow-xl transform hover:scale-105 transition-all">
          Continue to Login →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../utils/axios'
import { MoonIcon, SunIcon } from '@heroicons/vue/24/outline'

const router = useRouter()

const form = ref({
  email: '',
  password: '',
  full_name: '',
  role: 'student',
  school_id: '',
  grade: null,
  locale: 'en',
  selected_trade: '',
  selected_level: ''
})

const selectedProvince = ref('')
const selectedDistrict = ref('')
const provinces = ref([])
const districts = ref([])
const schools = ref([])
const selectedSchool = ref(null)
const loadingSchools = ref(false)
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

const API_URL = 'https://rwanda-edu-platform.onrender.com/api/v1'

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
  
  await loadProvinces()
})

onUnmounted(() => {
  if (bgIntervalId) {
    clearInterval(bgIntervalId)
  }
})

async function loadProvinces() {
  try {
    const response = await axios.get(`${API_URL}/locations/provinces`)
    provinces.value = response.data
  } catch (err) {
    console.error('Error loading provinces:', err)
  }
}

async function onProvinceChange() {
  selectedDistrict.value = ''
  districts.value = []
  schools.value = []
  form.value.school_id = ''
  
  if (selectedProvince.value) {
    try {
      const response = await axios.get(`${API_URL}/locations/districts/${selectedProvince.value}`)
      districts.value = response.data
    } catch (err) {
      console.error('Error loading districts:', err)
    }
  }
}

async function onDistrictChange() {
  schools.value = []
  form.value.school_id = ''
  
  if (!selectedDistrict.value || !selectedProvince.value) return
  
  loadingSchools.value = true
  
  try {
    const url = `${API_URL}/schools-by-district/district/${selectedProvince.value}/${selectedDistrict.value}`
    const response = await fetch(url)
    const data = await response.json()
    schools.value = data.schools || []
  } catch (error) {
    schools.value = []
  } finally {
    loadingSchools.value = false
  }
}

function onSchoolChange() {
  const school = schools.value.find(s => s.id === parseInt(form.value.school_id))
  selectedSchool.value = school
  form.value.selected_trade = ''
  form.value.selected_level = ''
  
  console.log('🏫 School selected:', school?.name)
  console.log('📚 School trades:', school?.trades)
  console.log('📊 Trades count:', school?.trades?.length || 0)
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
      grade: form.value.role === 'student' ? null : (form.value.grade ? parseInt(form.value.grade) : null),
      locale: form.value.locale,
      selected_trade: form.value.selected_trade || null,
      selected_level: form.value.selected_level || null
    }
    
    const response = await axios.post(`${API_URL}/auth/register`, payload)
    if (response.status === 200) {
      showSuccess.value = true
    }
  } catch (err) {
    console.error('Registration error:', err.response?.data)
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

<style scoped>
@keyframes float-rotate {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
  33% {
    transform: translateY(-20px) translateX(10px) rotate(5deg);
  }
  66% {
    transform: translateY(-10px) translateX(-10px) rotate(-5deg);
  }
  100% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
}

@keyframes float-rotate-reverse {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
  33% {
    transform: translateY(-15px) translateX(-15px) rotate(-8deg);
  }
  66% {
    transform: translateY(-25px) translateX(15px) rotate(8deg);
  }
  100% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
}

@keyframes float-rotate-slow {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) translateX(20px) rotate(10deg);
  }
  100% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
}

@keyframes float-rotate-delayed {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
  40% {
    transform: translateY(-18px) translateX(-12px) rotate(-6deg);
  }
  80% {
    transform: translateY(-8px) translateX(12px) rotate(6deg);
  }
  100% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
}

@keyframes bounce-in {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.animate-float-rotate {
  animation: float-rotate 8s ease-in-out infinite;
}

.animate-float-rotate-reverse {
  animation: float-rotate-reverse 10s ease-in-out infinite;
}

.animate-float-rotate-slow {
  animation: float-rotate-slow 12s ease-in-out infinite;
}

.animate-float-rotate-delayed {
  animation: float-rotate-delayed 9s ease-in-out infinite;
}

.animate-bounce-in {
  animation: bounce-in 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
</style>