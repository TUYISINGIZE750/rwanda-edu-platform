<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm p-4 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto flex items-center gap-4">
        <button @click="$router.back()" class="text-blue-600 hover:text-blue-700">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <h1 class="text-xl font-bold">My Resources</h1>
        <button @click="$router.push('/upload-resource')" class="ml-auto bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          Upload New
        </button>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto p-6">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="mt-2 text-gray-600">Loading resources...</p>
      </div>

      <div v-else-if="resources.length === 0" class="text-center py-12">
        <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-gray-600 text-lg mb-4">No resources uploaded yet</p>
        <button @click="$router.push('/upload-resource')" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
          Upload Your First Resource
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="resource in resources" :key="resource.id" 
             class="bg-white rounded-lg shadow hover:shadow-lg transition-shadow">
          <div class="p-6">
            <div class="flex items-start justify-between mb-4">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg v-if="resource.type === 'pdf'" class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                <svg v-else-if="resource.type === 'video'" class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                <svg v-else class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <span class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">{{ resource.type }}</span>
            </div>
            
            <h3 class="font-semibold text-gray-900 mb-2">{{ resource.title }}</h3>
            <p class="text-sm text-gray-600 mb-3">{{ resource.description || 'No description' }}</p>
            
            <div class="flex items-center text-xs text-gray-500 mb-4">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              {{ resource.group_name }}
            </div>
            
            <div class="pt-4 border-t border-gray-100">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs text-gray-500">{{ formatDate(resource.created_at) }}</span>
              </div>
              <div class="flex gap-2">
                <a v-if="resource.url" :href="resource.url" target="_blank" 
                   class="flex-1 text-center bg-blue-50 text-blue-600 px-3 py-2 rounded hover:bg-blue-100 text-sm font-medium">
                  Download
                </a>
                <button @click="editResource(resource)" 
                        class="flex-1 bg-gray-50 text-gray-700 px-3 py-2 rounded hover:bg-gray-100 text-sm font-medium">
                  Edit
                </button>
                <button @click="deleteResource(resource.id)" 
                        class="bg-red-50 text-red-600 px-3 py-2 rounded hover:bg-red-100 text-sm font-medium">
                  Delete
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
import { useRouter } from 'vue-router'
import api from '../utils/api'

const router = useRouter()
const resources = ref([])
const loading = ref(true)

onMounted(async () => {
  await loadResources()
})

async function loadResources() {
  try {
    const response = await api.get('/teacher/resources')
    resources.value = response.data
  } catch (err) {
    console.error('Failed to load resources:', err)
  } finally {
    loading.value = false
  }
}

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleDateString('en-US', { 
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function editResource(resource) {
  console.log('Edit resource clicked:', resource)
  // Navigate to upload page with resource data for editing
  router.push({
    path: '/upload-resource',
    query: { edit: resource.id }
  })
}

async function deleteResource(resourceId) {
  console.log('Delete resource clicked:', resourceId)
  if (!confirm('Are you sure you want to delete this resource?')) return
  
  try {
    await api.delete(`/teacher/resources/${resourceId}`)
    alert('Resource deleted successfully')
    await loadResources()
  } catch (err) {
    console.error('Failed to delete resource:', err)
    alert('Failed to delete resource')
  }
}
</script>
