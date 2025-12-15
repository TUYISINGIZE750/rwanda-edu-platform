<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm p-4 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto flex items-center gap-4">
        <button @click="$router.back()" class="text-blue-600 hover:text-blue-700">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <h1 class="text-xl font-bold">Student Profile</h1>
      </div>
    </nav>

    <main class="max-w-5xl mx-auto p-6">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
      </div>

      <div v-else-if="student" class="space-y-6">
        <!-- Profile Header -->
        <div class="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg shadow-lg p-8 text-white">
          <div class="flex items-center space-x-6">
            <div class="w-24 h-24 bg-white rounded-full flex items-center justify-center">
              <span class="text-blue-600 font-bold text-4xl">{{ student.full_name.charAt(0) }}</span>
            </div>
            <div class="flex-1">
              <h2 class="text-3xl font-bold mb-2">{{ student.full_name }}</h2>
              <p class="text-blue-100 mb-1">{{ student.email }}</p>
              <div class="flex items-center space-x-4 mt-3">
                <span class="bg-blue-500 px-3 py-1 rounded-full text-sm">{{ student.role }}</span>
                <span class="bg-blue-500 px-3 py-1 rounded-full text-sm">Active</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white rounded-lg shadow p-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500">Attendance</p>
                <p class="text-lg font-bold text-gray-900">92%</p>
              </div>
            </div>
          </div>
          <div class="bg-white rounded-lg shadow p-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500">Assignments</p>
                <p class="text-lg font-bold text-gray-900">8/10</p>
              </div>
            </div>
          </div>
          <div class="bg-white rounded-lg shadow p-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500">Progress</p>
                <p class="text-lg font-bold text-gray-900">78%</p>
              </div>
            </div>
          </div>
          <div class="bg-white rounded-lg shadow p-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500">Grade</p>
                <p class="text-lg font-bold text-gray-900">B+</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Left Column -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Academic Info -->
            <div class="bg-white rounded-lg shadow">
              <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Academic Information</h3>
              </div>
              <div class="p-6 space-y-4">
                <div class="flex items-center justify-between py-3 border-b border-gray-100">
                  <span class="text-gray-600">Trade</span>
                  <span class="font-medium text-gray-900">{{ student.selected_trade || 'Not specified' }}</span>
                </div>
                <div class="flex items-center justify-between py-3 border-b border-gray-100">
                  <span class="text-gray-600">Level</span>
                  <span class="font-medium text-gray-900">{{ student.selected_level || 'Not specified' }}</span>
                </div>
                <div class="flex items-center justify-between py-3 border-b border-gray-100">
                  <span class="text-gray-600">School ID</span>
                  <span class="font-medium text-gray-900">{{ student.school_id }}</span>
                </div>
                <div class="flex items-center justify-between py-3">
                  <span class="text-gray-600">Enrollment Date</span>
                  <span class="font-medium text-gray-900">{{ formatDate(student.created_at) }}</span>
                </div>
              </div>
            </div>

            <!-- Recent Activity -->
            <div class="bg-white rounded-lg shadow">
              <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Recent Activity</h3>
              </div>
              <div class="p-6">
                <div class="space-y-4">
                  <div class="flex items-start space-x-3">
                    <div class="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                    <div class="flex-1">
                      <p class="text-sm text-gray-900">Submitted assignment: Welding Safety</p>
                      <p class="text-xs text-gray-500">2 hours ago</p>
                    </div>
                  </div>
                  <div class="flex items-start space-x-3">
                    <div class="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                    <div class="flex-1">
                      <p class="text-sm text-gray-900">Attended practical session</p>
                      <p class="text-xs text-gray-500">1 day ago</p>
                    </div>
                  </div>
                  <div class="flex items-start space-x-3">
                    <div class="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                    <div class="flex-1">
                      <p class="text-sm text-gray-900">Downloaded resource: Study Guide</p>
                      <p class="text-xs text-gray-500">2 days ago</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="space-y-6">
            <!-- Contact Info -->
            <div class="bg-white rounded-lg shadow">
              <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Contact</h3>
              </div>
              <div class="p-6 space-y-4">
                <div class="flex items-center space-x-3">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span class="text-sm text-gray-600">{{ student.email }}</span>
                </div>
                <div class="flex items-center space-x-3">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span class="text-sm text-gray-600">{{ student.province }}, {{ student.district }}</span>
                </div>
              </div>
            </div>

            <!-- Quick Actions -->
            <div class="bg-white rounded-lg shadow">
              <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Actions</h3>
              </div>
              <div class="p-6 space-y-3">
                <button class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 flex items-center justify-center space-x-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                  <span>Send Message</span>
                </button>
                <button class="w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-50 flex items-center justify-center space-x-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span>View Reports</span>
                </button>
              </div>
            </div>

            <!-- Groups -->
            <div class="bg-white rounded-lg shadow">
              <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Groups</h3>
              </div>
              <div class="p-6">
                <div class="space-y-2">
                  <div class="flex items-center space-x-2 text-sm">
                    <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                    <span class="text-gray-700">Level 3 Electronics</span>
                  </div>
                  <div class="flex items-center space-x-2 text-sm">
                    <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span class="text-gray-700">Practical Workshop</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../utils/api'

const route = useRoute()
const studentId = route.params.studentId

const student = ref(null)
const loading = ref(true)

onMounted(async () => {
  await loadStudent()
})

async function loadStudent() {
  try {
    const response = await api.get(`/teacher/students/${studentId}`)
    student.value = response.data
  } catch (err) {
    console.error('Failed to load student:', err)
  } finally {
    loading.value = false
  }
}

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleDateString('en-US', { 
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>
