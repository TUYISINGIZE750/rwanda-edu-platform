<template>
  <div class="min-h-screen bg-white">
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center min-h-screen bg-white">
      <div class="text-center">
        <div class="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
        <p class="text-gray-600">Loading dashboard...</p>
      </div>
    </div>
    
    <!-- Route to appropriate dashboard -->
    <div v-else class="bg-white">
      <StudentDashboard v-if="authStore.user?.role?.toLowerCase() === 'student'" />
      <TeacherDashboard v-else-if="authStore.user?.role?.toLowerCase() === 'teacher'" />
      <AdminDashboard v-else-if="authStore.user?.role?.toLowerCase() === 'admin' && authStore.user?.school_id" />
      <div v-else-if="authStore.user?.role?.toLowerCase() === 'admin'" class="flex items-center justify-center min-h-screen bg-white">
        <div class="text-center">
          <p class="text-gray-600 mb-4">Please select your assigned school</p>
          <button @click="$router.push('/admin/school-selection')" class="bg-red-600 text-white px-4 py-2 rounded-lg">
            Select School
          </button>
        </div>
      </div>
      <div v-else class="flex items-center justify-center min-h-screen bg-white">
        <div class="text-center">
          <p class="text-red-600 mb-4">Invalid user role: {{ authStore.user?.role }}</p>
          <button @click="authStore.logout" class="bg-red-600 text-white px-4 py-2 rounded-lg">
            Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import StudentDashboard from './StudentDashboard.vue'
import TeacherDashboard from './TeacherDashboard.vue'
import AdminDashboard from './AdminDashboard.vue'

const authStore = useAuthStore()
const router = useRouter()
const loading = ref(true)

onMounted(async () => {
  try {
    // Ensure user is authenticated
    if (!authStore.isAuthenticated) {
      router.push('/login')
      return
    }
    
    // If user data is already available, no need to wait
    if (authStore.user) {
      loading.value = false
      return
    }
    
    // Initialize auth and wait for user data
    await authStore.initAuth()
    
  } catch (err) {
    console.error('Failed to initialize dashboard:', err)
    authStore.logout()
  } finally {
    loading.value = false
  }
})
</script>
