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
            <h1 class="text-xl font-semibold text-gray-900">Analytics & Reports</h1>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Overview Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Total Users</p>
              <p class="text-3xl font-bold text-gray-900">{{ analytics.total_users || 0 }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
            </div>
          </div>
          <p class="text-xs text-green-600 mt-2">+{{ analytics.new_users_this_month || 0 }} this month</p>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Messages</p>
              <p class="text-3xl font-bold text-gray-900">{{ totalMessages }}</p>
            </div>
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
          </div>
          <p class="text-xs text-gray-600 mt-2">Last 7 days</p>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Avg Daily Activity</p>
              <p class="text-3xl font-bold text-gray-900">{{ avgDaily }}</p>
            </div>
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
          <p class="text-xs text-gray-600 mt-2">Messages per day</p>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Peak Day</p>
              <p class="text-3xl font-bold text-gray-900">{{ peakDay }}</p>
            </div>
            <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <p class="text-xs text-gray-600 mt-2">Highest activity</p>
        </div>
      </div>

      <!-- Activity Chart -->
      <div class="bg-white rounded-lg shadow p-6 mb-8">
        <h3 class="text-lg font-semibold mb-4">Daily Activity (Last 7 Days)</h3>
        <div class="h-64 flex items-end justify-between space-x-2">
          <div v-for="day in analytics.daily_activity" :key="day.date" class="flex-1 flex flex-col items-center">
            <div class="w-full bg-blue-500 rounded-t hover:bg-blue-600 transition-colors" 
                 :style="{ height: `${(day.messages / maxMessages) * 100}%` }"
                 :title="`${day.messages} messages`">
            </div>
            <p class="text-xs text-gray-600 mt-2">{{ formatDate(day.date) }}</p>
            <p class="text-xs font-semibold text-gray-900">{{ day.messages }}</p>
          </div>
        </div>
      </div>

      <!-- Top Performers -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Top Students -->
        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-4 border-b">
            <h3 class="text-lg font-semibold">Top Students</h3>
          </div>
          <div class="p-6">
            <div class="space-y-3">
              <div v-for="(student, idx) in engagement.top_students" :key="student.id" 
                   class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div class="flex items-center space-x-3">
                  <span class="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {{ idx + 1 }}
                  </span>
                  <span class="text-sm font-medium">{{ student.name }}</span>
                </div>
                <span class="text-sm text-gray-600">{{ student.messages }} msgs</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Teachers -->
        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-4 border-b">
            <h3 class="text-lg font-semibold">Top Teachers</h3>
          </div>
          <div class="p-6">
            <div class="space-y-3">
              <div v-for="(teacher, idx) in engagement.top_teachers" :key="teacher.id" 
                   class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div class="flex items-center space-x-3">
                  <span class="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {{ idx + 1 }}
                  </span>
                  <span class="text-sm font-medium">{{ teacher.name }}</span>
                </div>
                <span class="text-sm text-gray-600">{{ teacher.messages }} msgs</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Channels -->
        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-4 border-b">
            <h3 class="text-lg font-semibold">Top Channels</h3>
          </div>
          <div class="p-6">
            <div class="space-y-3">
              <div v-for="(channel, idx) in engagement.top_channels" :key="channel.id" 
                   class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div class="flex items-center space-x-3">
                  <span class="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {{ idx + 1 }}
                  </span>
                  <span class="text-sm font-medium">{{ channel.name }}</span>
                </div>
                <span class="text-sm text-gray-600">{{ channel.messages }} msgs</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../utils/api'

const analytics = ref({ daily_activity: [], total_users: 0, new_users_this_month: 0 })
const engagement = ref({ top_students: [], top_teachers: [], top_channels: [] })

onMounted(async () => {
  await Promise.all([loadAnalytics(), loadEngagement()])
})

async function loadAnalytics() {
  try {
    const res = await api.get('/admin/analytics/overview')
    analytics.value = res.data
  } catch (err) {
    console.error('Failed to load analytics:', err)
  }
}

async function loadEngagement() {
  try {
    const res = await api.get('/admin/reports/engagement?days=7')
    engagement.value = res.data
  } catch (err) {
    console.error('Failed to load engagement:', err)
  }
}

const totalMessages = computed(() => {
  return analytics.value.daily_activity.reduce((sum, day) => sum + day.messages, 0)
})

const avgDaily = computed(() => {
  const total = totalMessages.value
  const days = analytics.value.daily_activity.length || 1
  return Math.round(total / days)
})

const maxMessages = computed(() => {
  return Math.max(...analytics.value.daily_activity.map(d => d.messages), 1)
})

const peakDay = computed(() => {
  if (!analytics.value.daily_activity.length) return 0
  return Math.max(...analytics.value.daily_activity.map(d => d.messages))
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}
</script>
