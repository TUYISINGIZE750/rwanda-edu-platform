<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 via-indigo-50 to-blue-50 p-8">
    <div class="max-w-4xl mx-auto">
      <div class="bg-white rounded-3xl shadow-2xl overflow-hidden border-2 border-purple-200">
        <div class="p-8 bg-gradient-to-r from-purple-600 to-indigo-600">
          <h1 class="text-4xl font-bold text-white mb-2">🔐 Super Admin Panel</h1>
          <p class="text-purple-100">Generate DOS credentials for all TVET/TSS schools</p>
        </div>
        
        <div class="p-8 space-y-6">
          <!-- Stats -->
          <div v-if="stats" class="grid grid-cols-3 gap-4">
            <div class="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 border-2 border-green-200">
              <div class="text-4xl mb-2">✅</div>
              <p class="text-3xl font-bold text-green-900">{{ stats.created }}</p>
              <p class="text-sm text-green-700">Created</p>
            </div>
            <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border-2 border-blue-200">
              <div class="text-4xl mb-2">⏭️</div>
              <p class="text-3xl font-bold text-blue-900">{{ stats.skipped }}</p>
              <p class="text-sm text-blue-700">Skipped</p>
            </div>
            <div class="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6 border-2 border-purple-200">
              <div class="text-4xl mb-2">📊</div>
              <p class="text-3xl font-bold text-purple-900">{{ stats.total }}</p>
              <p class="text-sm text-purple-700">Total Schools</p>
            </div>
          </div>
          
          <!-- Actions -->
          <div class="space-y-4">
            <button @click="generateAccounts" :disabled="generating" 
                    class="w-full p-6 bg-gradient-to-r from-purple-500 to-indigo-500 text-white rounded-2xl hover:from-purple-600 hover:to-indigo-600 transition-all shadow-lg disabled:opacity-50 flex items-center justify-center gap-3">
              <svg v-if="!generating" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              <svg v-else class="animate-spin w-6 h-6" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span class="text-xl font-bold">{{ generating ? 'Generating...' : 'Generate DOS Accounts' }}</span>
            </button>
            
            <button @click="downloadPDF" :disabled="downloading"
                    class="w-full p-6 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-2xl hover:from-green-600 hover:to-emerald-600 transition-all shadow-lg disabled:opacity-50 flex items-center justify-center gap-3">
              <svg v-if="!downloading" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <svg v-else class="animate-spin w-6 h-6" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span class="text-xl font-bold">{{ downloading ? 'Generating PDF...' : '📄 Download Credentials PDF' }}</span>
            </button>
          </div>
          
          <!-- Success Message -->
          <div v-if="successMessage" class="bg-green-50 border-2 border-green-300 rounded-2xl p-6">
            <div class="flex items-center gap-3">
              <div class="text-4xl">✅</div>
              <div>
                <h3 class="text-lg font-bold text-green-900">{{ successMessage }}</h3>
                <p class="text-sm text-green-700 mt-1">All DOS accounts have been created successfully</p>
              </div>
            </div>
          </div>
          
          <!-- Error Message -->
          <div v-if="errorMessage" class="bg-red-50 border-2 border-red-300 rounded-2xl p-6">
            <div class="flex items-center gap-3">
              <div class="text-4xl">❌</div>
              <div>
                <h3 class="text-lg font-bold text-red-900">Error</h3>
                <p class="text-sm text-red-700 mt-1">{{ errorMessage }}</p>
              </div>
            </div>
          </div>
          
          <!-- Instructions -->
          <div class="bg-blue-50 border-2 border-blue-200 rounded-2xl p-6">
            <h3 class="text-lg font-bold text-blue-900 mb-3">📋 Instructions</h3>
            <ol class="space-y-2 text-sm text-blue-800">
              <li><strong>1. Generate DOS Accounts:</strong> Creates admin accounts for all 165 TVET/TSS schools</li>
              <li><strong>2. Download PDF:</strong> Generates a PDF document with all credentials organized by province</li>
              <li><strong>3. Distribute:</strong> Share the PDF with each school's administration</li>
              <li><strong>4. Login:</strong> DOS admins use the admin login portal with their credentials</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../utils/api'

const generating = ref(false)
const downloading = ref(false)
const stats = ref(null)
const successMessage = ref('')
const errorMessage = ref('')

async function generateAccounts() {
  generating.value = true
  successMessage.value = ''
  errorMessage.value = ''
  
  try {
    const response = await api.post('/super-admin/generate-dos-accounts', {}, { timeout: 120000 })
    stats.value = {
      created: response.data.created,
      skipped: response.data.skipped,
      total: response.data.total
    }
    successMessage.value = `Successfully generated ${response.data.created} new DOS accounts!`
  } catch (err) {
    console.error('Error generating accounts:', err)
    if (err.code === 'ECONNABORTED') {
      errorMessage.value = 'Request timeout. Accounts may have been created. Try downloading the PDF.'
    } else {
      errorMessage.value = err.response?.data?.detail || 'Failed to generate accounts'
    }
  } finally {
    generating.value = false
  }
}

async function downloadPDF() {
  downloading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  
  try {
    const response = await api.get('/super-admin/download-dos-credentials', {
      responseType: 'blob',
      timeout: 120000
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `dos_credentials_${new Date().toISOString().split('T')[0]}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    
    successMessage.value = 'PDF downloaded successfully!'
  } catch (err) {
    console.error('Error downloading PDF:', err)
    errorMessage.value = err.code === 'ECONNABORTED' ? 'Request timeout. Please try again.' : 'Failed to download PDF'
  } finally {
    downloading.value = false
  }
}
</script>
