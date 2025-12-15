<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm p-4">
      <div class="max-w-7xl mx-auto flex items-center gap-4">
        <button @click="$router.back()" class="text-blue-600 hover:text-blue-700">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <h1 class="text-xl font-bold">Reports & Analytics</h1>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto p-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-sm font-medium text-gray-600 mb-2">Total Students</h3>
          <p class="text-3xl font-bold text-gray-900">{{ stats.totalStudents }}</p>
          <p class="text-sm text-green-600 mt-2">↑ 12% from last month</p>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-sm font-medium text-gray-600 mb-2">Active Groups</h3>
          <p class="text-3xl font-bold text-gray-900">{{ stats.activeGroups }}</p>
          <p class="text-sm text-blue-600 mt-2">{{ stats.totalGroups }} total</p>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-sm font-medium text-gray-600 mb-2">Engagement Rate</h3>
          <p class="text-3xl font-bold text-gray-900">{{ stats.engagementRate }}%</p>
          <p class="text-sm text-green-600 mt-2">↑ 5% from last week</p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Group Activity</h3>
          <div class="space-y-3">
            <div v-for="group in groupActivity" :key="group.name" class="flex items-center justify-between">
              <span class="text-sm text-gray-700">{{ group.name }}</span>
              <div class="flex items-center gap-2">
                <div class="w-32 bg-gray-200 rounded-full h-2">
                  <div class="bg-blue-600 h-2 rounded-full" :style="{width: group.activity + '%'}"></div>
                </div>
                <span class="text-sm text-gray-600">{{ group.activity }}%</span>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Recent Sessions</h3>
          <div class="space-y-3">
            <div v-for="session in recentSessions" :key="session.id" class="border-l-4 border-purple-500 pl-3">
              <p class="text-sm font-medium text-gray-900">{{ session.title }}</p>
              <p class="text-xs text-gray-500">{{ session.date }} • {{ session.attendance }} students</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../utils/api'

const stats = ref({
  totalStudents: 0,
  activeGroups: 0,
  totalGroups: 0,
  engagementRate: 0
})

const groupActivity = ref([
  { name: 'Level 3 Electronics', activity: 85 },
  { name: 'Welding Basics', activity: 72 },
  { name: 'Carpentry Advanced', activity: 68 },
  { name: 'Plumbing Level 2', activity: 55 }
])

const recentSessions = ref([
  { id: 1, title: 'Safety Training', date: 'Today, 10:00 AM', attendance: 24 },
  { id: 2, title: 'Practical Workshop', date: 'Yesterday, 2:00 PM', attendance: 18 },
  { id: 3, title: 'Theory Class', date: '2 days ago', attendance: 22 }
])

onMounted(async () => {
  try {
    const response = await api.get('/teacher/dashboard')
    stats.value.totalStudents = response.data.stats.total_students
    stats.value.totalGroups = response.data.stats.groups_count
    stats.value.activeGroups = response.data.stats.groups_count
    stats.value.engagementRate = 78
  } catch (err) {
    console.error('Failed to load reports:', err)
  }
})
</script>
