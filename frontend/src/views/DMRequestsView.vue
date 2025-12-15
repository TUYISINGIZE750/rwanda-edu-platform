<template>
  <div class="min-h-screen">
    <nav class="bg-white shadow-sm p-4">
      <div class="max-w-7xl mx-auto flex items-center gap-4">
        <router-link to="/" class="text-primary">←</router-link>
        <h1 class="text-xl font-bold">{{ t('dm.request') }}</h1>
      </div>
    </nav>
    
    <main class="max-w-4xl mx-auto p-4">
      <div v-if="authStore.user?.role === 'student'" class="card mb-4">
        <h2 class="font-semibold mb-4">{{ t('dm.request') }}</h2>
        <form @submit.prevent="submitRequest" class="space-y-3">
          <input v-model="topic" :placeholder="t('dm.topic')" class="input" required />
          <textarea v-model="reason" :placeholder="t('dm.reason')" class="input" rows="3" required></textarea>
          <button type="submit" class="btn btn-primary">{{ t('messages.send') }}</button>
        </form>
      </div>
      
      <div v-if="authStore.user?.role === 'teacher'" class="space-y-4">
        <h2 class="font-semibold text-lg">{{ t('messages.pending') }}</h2>
        <div v-for="req in requests" :key="req.id" class="card">
          <p class="font-medium">{{ req.topic }}</p>
          <p class="text-sm text-gray-600 mt-1">{{ req.reason }}</p>
          <div class="flex gap-2 mt-3">
            <button @click="approveRequest(req.id, true)" class="btn btn-primary text-sm">{{ t('dm.approve') }}</button>
            <button @click="approveRequest(req.id, false)" class="btn btn-secondary text-sm">{{ t('dm.reject') }}</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../stores/auth'
import api from '../utils/api'

const { t } = useI18n()
const authStore = useAuthStore()

const topic = ref('')
const reason = ref('')
const requests = ref([])

onMounted(async () => {
  if (authStore.user?.role === 'teacher') {
    const response = await api.get('/dm-requests/pending')
    requests.value = response.data
  }
})

async function submitRequest() {
  await api.post('/dm-requests/', {
    teacher_id: 1,
    topic: topic.value,
    reason: reason.value
  })
  topic.value = ''
  reason.value = ''
}

async function approveRequest(id, approved) {
  await api.post(`/dm-requests/${id}/approve`, { approved, window_hours: 48 })
  requests.value = requests.value.filter(r => r.id !== id)
}
</script>
