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
      <svg v-if="isDark" class="w-6 h-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
      <svg v-else class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
      </svg>
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

    <div class="relative z-10 w-full max-w-md bg-white/95 dark:bg-gray-800/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 overflow-hidden transition-colors duration-300">
      <!-- Header -->
      <div class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 px-6 py-8 text-center">
        <div class="flex items-center justify-center gap-2 mb-3">
          <div class="w-16 h-16 bg-white/20 backdrop-blur-lg rounded-xl flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
            </svg>
          </div>
        </div>
        <h1 class="text-3xl font-bold text-white mb-2">TSSANYWHERE</h1>
        <p class="text-blue-100 text-sm">Learn Anytime, Anywhere</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="p-8 space-y-6">
        <div>
          <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Email Address</label>
          <input 
            v-model="form.email" 
            type="email" 
            class="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-all" 
            required 
            placeholder="Enter your email"
          />
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Password</label>
          <input 
            v-model="form.password" 
            type="password" 
            class="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-all" 
            required 
            placeholder="Enter your password"
          />
        </div>

        <button 
          type="submit" 
          class="w-full bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white py-3 rounded-lg font-semibold text-base hover:shadow-xl transform hover:scale-[1.01] transition-all disabled:opacity-50 disabled:cursor-not-allowed" 
          :disabled="loading"
        >
          <span v-if="!loading">Sign In</span>
          <span v-else class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Signing In...
          </span>
        </button>
        
        <p v-if="error" class="text-red-600 dark:text-red-400 text-sm text-center bg-red-50 dark:bg-red-900/20 p-3 rounded-lg border-2 border-red-200 dark:border-red-800 font-medium">
          {{ error }}
        </p>
        
        <div class="text-center space-y-2">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Don't have an account?
            <router-link to="/register" class="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-semibold hover:underline ml-1">
              Create Account
            </router-link>
          </p>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            DOS/Admin?
            <router-link to="/admin-login" class="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 font-semibold hover:underline ml-1">
              DOS Portal
            </router-link>
          </p>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            <router-link to="/" class="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-semibold hover:underline">
              Back to Home
            </router-link>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: ''
})

const loading = ref(false)
const error = ref('')
const isDark = ref(false)
const currentBgIndex = ref(0)
let bgIntervalId = null

const backgroundImages = ref([
  '/images to use/DSC_0106.JPG',
  '/images to use/IMG-20241006-WA0079.jpg',
  '/images to use/IMG-20241006-WA0051.jpg',
  '/images to use/home_page_3.jpg'
])

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

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
  
  bgIntervalId = setInterval(() => {
    currentBgIndex.value = (currentBgIndex.value + 1) % backgroundImages.value.length
  }, 4000)
})

onUnmounted(() => {
  if (bgIntervalId) {
    clearInterval(bgIntervalId)
  }
})

async function handleLogin() {
  loading.value = true
  error.value = ''
  
  try {
    await authStore.login(form.value.email, form.value.password)
    
    const role = authStore.user?.role?.toLowerCase()
    if (role === 'admin') {
      router.push('/dos-dashboard')
    } else if (role === 'teacher') {
      router.push('/teacher-dashboard')
    } else if (role === 'student') {
      router.push('/student-dashboard')
    } else {
      router.push('/home')
    }
  } catch (err) {
    console.error('Login error:', err)
    error.value = err.response?.data?.detail || 'Invalid email or password'
  } finally {
    loading.value = false
  }
}
</script>
