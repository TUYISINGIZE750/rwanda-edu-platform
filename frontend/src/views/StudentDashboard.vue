<template>
  <div class="min-h-screen flex flex-col relative bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <!-- Animated Background Effects -->
    <div class="fixed inset-0 pointer-events-none overflow-hidden z-0">
      <div class="absolute top-0 left-0 w-[600px] h-[600px] rounded-full opacity-40 blur-3xl animate-blob bg-blue-200"></div>
      <div class="absolute bottom-0 right-0 w-[700px] h-[700px] rounded-full opacity-40 blur-3xl animate-blob bg-purple-200" style="animation-delay: 2s;"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full opacity-30 blur-3xl animate-blob bg-indigo-200" style="animation-delay: 4s;"></div>
    </div>

    <!-- Modern Header -->
    <header class="bg-white/90 backdrop-blur-xl border-b border-indigo-200 shadow-lg sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg">
              <span class="text-2xl">👨‍🎓</span>
            </div>
            <div>
              <h1 class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">TSSANYWHERE</h1>
              <p class="text-xs text-gray-600 font-medium">Student Dashboard - Learn Anytime, Anywhere</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <NotificationBell />
            <div class="text-right">
              <p class="text-sm font-semibold text-gray-900">{{ authStore.user?.full_name }}</p>
              <p class="text-xs text-gray-600">Student</p>
            </div>
            <button @click="logout" class="px-4 py-2 bg-red-500 text-white rounded-xl hover:bg-red-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="flex-1 overflow-y-auto relative z-10">
      <div class="max-w-7xl mx-auto px-6 py-6">
        <!-- Welcome Banner -->
        <div class="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-3xl p-8 mb-6 text-white shadow-2xl">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-3xl font-bold mb-2 flex items-center gap-3">
                Welcome back, {{ authStore.user?.full_name?.split(' ')[0] }}!
                <span class="text-4xl">👋</span>
              </h2>
              <p class="text-white/90">{{ authStore.user?.selected_level }} • {{ authStore.user?.selected_trade }}</p>
            </div>
            <svg class="w-24 h-24 text-white/20" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
            </svg>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="grid grid-cols-4 gap-4 mb-6">
          <div @click="scrollToClasses" class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all cursor-pointer transform hover:scale-105 border-2 border-transparent hover:border-indigo-300">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C6.5 6.253 2 10.998 2 17.25c0 5.079 3.855 9.26 8.75 9.589m0-13c5.5 0 10 4.745 10 10.25 0 5.079-3.855 9.26-8.75 9.589m0 0A8.997 8.997 0 0012 21.75c-4.694 0-8.776-2.235-11.306-5.726m0 0a8.997 8.997 0 0122.612 0c0 5.287-3.46 9.817-8.306 11.552m0 0A9.01 9.01 0 0012 0c-4.87 0-9.065 2.25-11.938 5.726" />
                </svg>
              </div>
              <div>
                <p class="text-3xl font-bold text-gray-900">{{ stats.groups_count }}</p>
                <p class="text-sm text-gray-600">My Classes</p>
              </div>
            </div>
          </div>

          <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all cursor-pointer transform hover:scale-105 border-2 border-transparent hover:border-green-300">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </div>
              <div>
                <p class="text-3xl font-bold text-gray-900">{{ stats.unread_messages }}</p>
                <p class="text-sm text-gray-600">Unread Messages</p>
              </div>
            </div>
          </div>

          <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all cursor-pointer transform hover:scale-105 border-2 border-transparent hover:border-orange-300">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C6.5 6.253 2 10.998 2 17.25c0 5.079 3.855 9.26 8.75 9.589m0-13c5.5 0 10 4.745 10 10.25 0 5.079-3.855 9.26-8.75 9.589m0 0A8.997 8.997 0 0012 21.75c-4.694 0-8.776-2.235-11.306-5.726m0 0a8.997 8.997 0 0122.612 0c0 5.287-3.46 9.817-8.306 11.552m0 0A9.01 9.01 0 0012 0c-4.87 0-9.065 2.25-11.938 5.726" />
                </svg>
              </div>
              <div>
                <p class="text-3xl font-bold text-gray-900">{{ stats.resources_count }}</p>
                <p class="text-sm text-gray-600">Resources</p>
              </div>
            </div>
          </div>

          <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all cursor-pointer transform hover:scale-105 border-2 border-transparent hover:border-purple-300">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-3xl font-bold text-gray-900">{{ stats.active_sessions }}</p>
                <p class="text-sm text-gray-600">Active Sessions</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Grid -->
        <div class="grid grid-cols-3 gap-6 pb-6">
          <!-- Classes List -->
          <div class="col-span-2 bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl overflow-hidden border-2 border-indigo-200">
            <div class="p-6 border-b border-indigo-200 bg-gradient-to-r from-indigo-50 to-purple-50">
              <h3 class="text-xl font-bold text-gray-900">📚 My Classes</h3>
              <p class="text-sm text-gray-600">{{ groups.length }} active classes</p>
            </div>
            <div class="overflow-y-auto max-h-96 p-6">
              <div v-if="loading" class="flex items-center justify-center h-full">
                <div class="text-center">
                  <div class="animate-spin h-12 w-12 border-4 border-indigo-500 border-t-transparent rounded-full mx-auto mb-4"></div>
                  <p class="text-gray-600">Loading classes...</p>
                </div>
              </div>
              
              <div v-else-if="groups.length === 0" class="flex items-center justify-center h-full">
                <div class="text-center">
                  <div class="text-6xl mb-4">📚</div>
                  <p class="text-gray-600 font-medium">No classes yet</p>
                </div>
              </div>
              
              <div v-else class="space-y-4">
                <div v-for="group in groups" :key="group.id" 
                     @click="$router.push(`/hubs/${group.id}`)"
                     class="bg-gradient-to-r from-white to-indigo-50 rounded-2xl p-5 border-2 border-indigo-200 hover:border-indigo-400 hover:shadow-xl transition-all cursor-pointer transform hover:scale-105">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-4">
                      <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center text-3xl shadow-lg">
                        #
                      </div>
                      <div>
                        <h4 class="text-lg font-bold text-gray-900">{{ group.name }}</h4>
                        <p class="text-sm text-gray-600">{{ group.member_count }} students • {{ group.channels_count }} channels</p>
                      </div>
                    </div>
                    <svg class="w-6 h-6 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Recent Activity -->
            <div class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl overflow-hidden border-2 border-green-200">
              <div class="p-4 border-b border-green-200 bg-gradient-to-r from-green-50 to-emerald-50">
                <h3 class="text-lg font-bold text-gray-900">📊 Recent Activity</h3>
              </div>
              <div class="p-4 space-y-3 max-h-96 overflow-y-auto">
                <div v-if="groups.length === 0" class="text-center py-8 text-gray-500">
                  <div class="text-4xl mb-2">📋</div>
                  <p class="text-sm">No recent activity</p>
                </div>
                <div v-else v-for="(group, idx) in groups.slice(0, 5)" :key="idx"
                     class="bg-gradient-to-r from-white to-green-50 rounded-xl p-4 border-2 border-green-200 hover:border-green-400 hover:shadow-lg transition-all">
                  <div class="flex items-start gap-3">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-600 flex items-center justify-center text-white font-bold flex-shrink-0">
                      {{ group.name?.charAt(0).toUpperCase() }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900">{{ group.name }}</p>
                      <p class="text-xs text-gray-600 mt-1">{{ group.unread_count }} unread messages</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
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
import api from '../utils/api'
import NotificationBell from '../components/NotificationBell.vue'

const router = useRouter()
const authStore = useAuthStore()

const groups = ref([])
const stats = ref({
  groups_count: 0,
  unread_messages: 0,
  resources_count: 0,
  active_sessions: 0
})
const loading = ref(false)

function scrollToClasses() {
  window.scrollTo({ top: 600, behavior: 'smooth' })
}

async function logout() {
  authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  if (authStore.user?.role?.toLowerCase() !== 'student') {
    router.push('/teacher-dashboard')
    return
  }
  
  try {
    loading.value = true
    const response = await api.get('/student/dashboard')
    groups.value = response.data.groups || []
    stats.value = response.data.stats || {}
  } catch (err) {
    console.error('Failed to load dashboard:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
@keyframes blob {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}
.animate-blob { animation: blob 7s infinite; }
</style>
