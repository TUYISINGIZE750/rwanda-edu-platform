<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-red-600 rounded-lg flex items-center justify-center mr-3">
              <ShieldCheckIcon class="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 class="text-xl font-semibold text-gray-900">Admin Dashboard</h1>
              <p class="text-xs text-green-600 font-medium">v2.0 - Latest (Notifications Enabled)</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">{{ authStore.user?.full_name }}</span>
            <button @click="authStore.logout" class="flex items-center gap-1 text-sm text-red-600 hover:text-red-700">
              <ArrowRightOnRectangleIcon class="w-4 h-4" />
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Welcome Section -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-2">School Administration</h2>
        <p class="text-gray-600">Manage your TVET institution</p>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
        <button @click="manageUsers" class="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 transition-colors">
          <div class="flex items-center justify-center mb-2">
            <UsersIcon class="w-6 h-6" />
          </div>
          <p class="text-sm font-medium">Manage Users</p>
        </button>

        <button @click="viewReports" class="bg-green-600 text-white p-4 rounded-lg hover:bg-green-700 transition-colors">
          <div class="flex items-center justify-center mb-2">
            <ChartBarIcon class="w-6 h-6" />
          </div>
          <p class="text-sm font-medium">Analytics</p>
        </button>

        <button @click="systemSettings" class="bg-purple-600 text-white p-4 rounded-lg hover:bg-purple-700 transition-colors">
          <div class="flex items-center justify-center mb-2">
            <Cog6ToothIcon class="w-6 h-6" />
          </div>
          <p class="text-sm font-medium">Settings</p>
        </button>

        <button @click="moderateContent" class="bg-yellow-600 text-white p-4 rounded-lg hover:bg-yellow-700 transition-colors">
          <div class="flex items-center justify-center mb-2">
            <CheckCircleIcon class="w-6 h-6" />
          </div>
          <p class="text-sm font-medium">Moderation</p>
        </button>

        <button @click="backupData" class="bg-gray-600 text-white p-4 rounded-lg hover:bg-gray-700 transition-colors">
          <div class="flex items-center justify-center mb-2">
            <ArrowDownTrayIcon class="w-6 h-6" />
          </div>
          <p class="text-sm font-medium">Backup</p>
        </button>
      </div>

      <!-- Stats Overview -->
      <div class="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
        <button @click="$router.push('/admin/users?role=STUDENT')" class="bg-white rounded-lg shadow p-6 hover:shadow-xl transition-all cursor-pointer text-left w-full">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <UsersIcon class="w-6 h-6 text-blue-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Students</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.total_students || 0 }}</p>
            </div>
          </div>
        </button>

        <button @click="$router.push('/admin/users?role=TEACHER')" class="bg-white rounded-lg shadow p-6 hover:shadow-xl transition-all cursor-pointer text-left w-full">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <BriefcaseIcon class="w-6 h-6 text-green-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Teachers</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.total_teachers || 0 }}</p>
            </div>
          </div>
        </button>

        <button @click="$router.push('/admin/users')" class="bg-white rounded-lg shadow p-6 hover:shadow-xl transition-all cursor-pointer text-left w-full">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <UserGroupIcon class="w-6 h-6 text-purple-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Active Groups</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.total_groups || 0 }}</p>
            </div>
          </div>
        </button>

        <button @click="$router.push('/admin/moderation')" class="bg-white rounded-lg shadow p-6 hover:shadow-xl transition-all cursor-pointer text-left w-full">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <ChatBubbleLeftRightIcon class="w-6 h-6 text-orange-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Messages</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.total_messages || 0 }}</p>
            </div>
          </div>
        </button>

        <button @click="$router.push('/admin/moderation')" class="bg-white rounded-lg shadow p-6 hover:shadow-xl transition-all cursor-pointer text-left w-full">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
              <ExclamationCircleIcon class="w-6 h-6 text-red-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Pending</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.pending_messages || 0 }}</p>
            </div>
          </div>
        </button>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Recent Activity -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Recent Activity</h3>
            </div>
            <div class="p-6">
              <div class="space-y-4">
                <div v-for="activity in recentActivity" :key="activity.id"
                     class="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
                  <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <UserIcon class="w-5 h-5 text-blue-600" />
                  </div>
                  <div class="flex-1">
                    <p class="text-sm font-medium text-gray-900">{{ activity.action }}</p>
                    <p class="text-sm text-gray-600">{{ activity.user }}</p>
                    <p class="text-xs text-gray-500 mt-1">{{ formatTime(activity.timestamp) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- System Status -->
        <div class="space-y-6">
          <!-- System Health -->
          <div class="bg-white rounded-lg shadow">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">System Health</h3>
            </div>
            <div class="p-6">
              <div class="space-y-4">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Server Status</span>
                  <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">Online</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Database</span>
                  <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">Healthy</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Storage</span>
                  <span class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">75% Used</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Backup</span>
                  <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">Up to Date</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Stats -->
          <div class="bg-white rounded-lg shadow">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Today's Summary</h3>
            </div>
            <div class="p-6">
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">New Registrations</span>
                  <span class="text-sm font-medium">{{ todayStats.newUsers || 0 }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Messages Sent</span>
                  <span class="text-sm font-medium">{{ todayStats.messagesSent || 0 }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Resources Uploaded</span>
                  <span class="text-sm font-medium">{{ todayStats.resourcesUploaded || 0 }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Active Sessions</span>
                  <span class="text-sm font-medium">{{ todayStats.activeSessions || 0 }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Alerts -->
          <div class="bg-white rounded-lg shadow">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">System Alerts</h3>
            </div>
            <div class="p-6">
              <div v-if="alerts.length === 0" class="text-center py-4">
                <p class="text-gray-600 text-sm">No alerts</p>
              </div>
              <div v-else class="space-y-3">
                <div v-for="alert in alerts" :key="alert.id"
                     class="p-3 rounded-lg" :class="alertClass(alert.type)">
                  <p class="text-sm font-medium">{{ alert.title }}</p>
                  <p class="text-xs mt-1">{{ alert.message }}</p>
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
import {
  ShieldCheckIcon,
  ArrowRightOnRectangleIcon,
  UsersIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  CheckCircleIcon,
  ArrowDownTrayIcon,
  BriefcaseIcon,
  UserGroupIcon,
  ChatBubbleLeftRightIcon,
  ExclamationCircleIcon,
  UserIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const stats = ref({})
const todayStats = ref({})
const recentActivity = ref([])
const alerts = ref([])
const loading = ref(true)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/admin-login')
    return
  }
  
  const userRole = authStore.user?.role?.toUpperCase()
  if (userRole !== 'ADMIN') {
    router.push('/admin-login')
    return
  }
  
  await loadDashboardData()
})

async function loadDashboardData() {
  try {
    // Load real stats from backend
    const statsRes = await api.get('/admin/dashboard')
    stats.value = {
      total_students: statsRes.data.users?.total_students || 0,
      total_teachers: statsRes.data.users?.total_teachers || 0,
      total_groups: statsRes.data.groups?.total || 0,
      total_messages: statsRes.data.messages?.total || 0,
      pending_messages: statsRes.data.messages?.pending_moderation || 0
    }
    
    // Load today's stats
    try {
      const activityRes = await api.get('/admin/activity/recent?hours=24')
      todayStats.value = {
        newUsers: 0,
        messagesSent: activityRes.data.messages || 0,
        resourcesUploaded: activityRes.data.resources || 0,
        activeSessions: 0
      }
    } catch (err) {
      console.error('Failed to load activity:', err)
      todayStats.value = { newUsers: 0, messagesSent: 0, resourcesUploaded: 0, activeSessions: 0 }
    }
    
    // Load recent activity
    recentActivity.value = [
      {
        id: 1,
        action: 'Dashboard loaded successfully',
        user: authStore.user?.full_name || 'Admin',
        timestamp: new Date()
      }
    ]
    
    alerts.value = []
    
  } catch (err) {
    console.error('Failed to load dashboard data:', err)
    // Set zeros on error
    stats.value = {
      total_students: 0,
      total_teachers: 0,
      total_groups: 0,
      total_messages: 0,
      pending_messages: 0
    }
    todayStats.value = { newUsers: 0, messagesSent: 0, resourcesUploaded: 0, activeSessions: 0 }
  } finally {
    loading.value = false
  }
}

function manageUsers() {
  router.push('/admin/users')
}

function viewReports() {
  router.push('/admin/reports')
}

function systemSettings() {
  router.push('/admin/settings')
}

function moderateContent() {
  router.push('/admin/moderation')
}

function backupData() {
  router.push('/admin/backup')
}

function alertClass(type) {
  switch (type) {
    case 'error': return 'bg-red-50 border border-red-200 text-red-800'
    case 'warning': return 'bg-yellow-50 border border-yellow-200 text-yellow-800'
    case 'info': return 'bg-blue-50 border border-blue-200 text-blue-800'
    default: return 'bg-gray-50 border border-gray-200 text-gray-800'
  }
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>