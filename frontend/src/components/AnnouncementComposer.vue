<template>
  <div class="card">
    <h3 class="font-semibold mb-3">Create Announcement</h3>
    <form @submit.prevent="submitAnnouncement" class="space-y-3">
      <textarea
        v-model="content"
        placeholder="Write your announcement..."
        class="input"
        rows="4"
        required
      ></textarea>
      
      <div class="flex items-center gap-4">
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="scheduled" />
          <span class="text-sm">Schedule for later</span>
        </label>
        
        <input
          v-if="scheduled"
          v-model="scheduledAt"
          type="datetime-local"
          class="input text-sm"
        />
      </div>
      
      <button type="submit" class="btn btn-primary">Post Announcement</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../utils/api'

const props = defineProps(['channelId'])
const emit = defineEmits(['posted'])

const content = ref('')
const scheduled = ref(false)
const scheduledAt = ref('')

async function submitAnnouncement() {
  await api.post('/messages/', {
    channel_id: props.channelId,
    content: content.value,
    scheduled_at: scheduled.value ? scheduledAt.value : null
  })
  
  content.value = ''
  scheduled.value = false
  scheduledAt.value = ''
  emit('posted')
}
</script>
