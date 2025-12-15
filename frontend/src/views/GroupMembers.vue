<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm p-4">
      <div class="max-w-7xl mx-auto flex items-center gap-4">
        <button @click="$router.back()" class="text-blue-600 hover:text-blue-700">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <h1 class="text-xl font-bold">Group Members</h1>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto p-6">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="mt-2 text-gray-600">Loading members...</p>
      </div>

      <div v-else>
        <div class="bg-white rounded-lg shadow mb-6 p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ groupName }}</h2>
          <p class="text-gray-600">{{ students.length }} students enrolled</p>
        </div>

        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Student List</h3>
          </div>
          
          <div v-if="students.length === 0" class="p-6 text-center">
            <p class="text-gray-600">No students in this group</p>
          </div>

          <div v-else class="divide-y divide-gray-200">
            <div v-for="student in students" :key="student.id" 
                 class="p-6 hover:bg-gray-50 transition-colors">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                    <span class="text-blue-600 font-semibold text-lg">
                      {{ student.full_name.charAt(0) }}
                    </span>
                  </div>
                  <div>
                    <h4 class="font-medium text-gray-900">{{ student.full_name }}</h4>
                    <p class="text-sm text-gray-600">{{ student.email }}</p>
                    <p class="text-xs text-gray-500 mt-1">
                      {{ student.selected_trade }} - {{ student.selected_level }}
                    </p>
                  </div>
                </div>
                <button @click="viewProfile(student.id)" class="text-blue-600 hover:text-blue-700 text-sm font-medium">
                  View Profile
                </button>
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
import { useRoute, useRouter } from 'vue-router'
import api from '../utils/api'

const router = useRouter()

const route = useRoute()
const groupId = route.params.groupId

const students = ref([])
const groupName = ref('')
const loading = ref(true)

onMounted(async () => {
  await loadMembers()
})

async function loadMembers() {
  try {
    const response = await api.get(`/teacher/groups/${groupId}/students`)
    students.value = response.data
    groupName.value = `Group ${groupId}`
  } catch (err) {
    console.error('Failed to load members:', err)
  } finally {
    loading.value = false
  }
}

function viewProfile(studentId) {
  router.push(`/students/${studentId}/profile`)
}
</script>
