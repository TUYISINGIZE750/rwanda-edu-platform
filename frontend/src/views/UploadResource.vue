<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-2xl mx-auto">
      <div class="bg-white rounded-lg shadow-lg p-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold text-gray-900">Upload Resource</h2>
          <button @click="$router.back()" class="text-gray-600 hover:text-gray-900">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="uploadResource" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Resource Title</label>
            <input v-model="form.title" type="text" required
                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                   placeholder="e.g., Electronics Study Guide">
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Select Group</label>
            <select v-model="form.groupId" required
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
              <option value="">Select a group</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">
                {{ group.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Resource Type</label>
            <select v-model="form.type" required
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
              <option value="">Select type</option>
              <option value="pdf">PDF Document</option>
              <option value="video">Video</option>
              <option value="document">Document</option>
              <option value="link">External Link</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Upload File</label>
            <input type="file" @change="handleFileChange" :required="!form.editId"
                   accept=".pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.mp4,.mp3,.zip"
                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
            <p class="text-xs text-gray-500 mt-1">
              💾 Supported: PDF, Word, PowerPoint, Excel, Videos, Audio, ZIP
              <span v-if="form.editId" class="text-orange-600"> (Leave empty to keep existing file)</span>
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description (Optional)</label>
            <textarea v-model="form.description" rows="3"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="Brief description of the resource"></textarea>
          </div>

          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {{ error }}
          </div>

          <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
            {{ success }}
          </div>

          <div class="flex space-x-4">
            <button type="submit" :disabled="loading"
                    class="flex-1 bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 disabled:opacity-50">
              {{ loading ? (form.editId ? 'Updating...' : 'Uploading...') : (form.editId ? 'Update Resource' : 'Upload Resource') }}
            </button>
            <button type="button" @click="$router.back()"
                    class="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'

const router = useRouter()

const form = ref({
  title: '',
  groupId: '',
  type: '',
  description: '',
  file: null,
  editId: null
})

const groups = ref([])
const loading = ref(false)
const error = ref('')
const success = ref('')

onMounted(async () => {
  try {
    const response = await api.get('/teacher/dashboard')
    groups.value = response.data.groups || []
    
    // Check if editing existing resource
    const editId = router.currentRoute.value.query.edit
    if (editId) {
      const resResponse = await api.get(`/teacher/resources/${editId}`)
      const resource = resResponse.data
      form.value.title = resource.title
      form.value.groupId = resource.group_id
      form.value.type = resource.type
      form.value.description = resource.description || ''
      form.value.editId = editId
    }
  } catch (err) {
    console.error('Failed to load data:', err)
  }
})

function handleFileChange(event) {
  form.value.file = event.target.files[0]
}

async function uploadResource() {
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    const formData = new FormData()
    formData.append('group_id', form.value.groupId)
    formData.append('title', form.value.title)
    formData.append('type', form.value.type)
    formData.append('description', form.value.description || '')
    if (form.value.file) {
      formData.append('file', form.value.file)
    }
    
    if (form.value.editId) {
      // Update existing resource
      await api.put(`/teacher/resources/${form.value.editId}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      success.value = 'Resource updated successfully!'
    } else {
      // Create new resource
      await api.post('/teacher/resources', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      success.value = 'Resource uploaded successfully!'
    }
    
    setTimeout(() => {
      router.push('/my-resources')
    }, 1500)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to upload resource'
  } finally {
    loading.value = false
  }
}
</script>
