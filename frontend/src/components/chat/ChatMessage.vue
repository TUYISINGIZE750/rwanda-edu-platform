<template>
  <div class="group relative" :class="{ 'flex-row-reverse': isOwnMessage }">
    <div class="flex items-start space-x-3" :class="{ 'flex-row-reverse space-x-reverse': isOwnMessage }">
      <!-- Avatar -->
      <div v-if="!isOwnMessage" class="flex-shrink-0">
        <img 
          :src="message.sender?.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(message.sender?.name || 'User')}&background=random`"
          :alt="message.sender?.name"
          class="w-8 h-8 rounded-full"
        />
      </div>

      <!-- Message Content -->
      <div class="flex-1 max-w-xs sm:max-w-md lg:max-w-lg">
        <!-- Sender name and timestamp -->
        <div v-if="!isOwnMessage" class="flex items-center space-x-2 mb-1">
          <span class="text-sm font-medium text-gray-900">{{ message.sender?.name || 'Unknown User' }}</span>
          <span class="text-xs text-gray-500">{{ formatTime(message.created_at || message.timestamp) }}</span>
        </div>

        <!-- Message bubble -->
        <div 
          class="relative px-4 py-2 rounded-2xl shadow-sm"
          :class="messageBubbleClass"
        >
          <!-- Text content -->
          <div v-if="message.type === 'text'" class="text-sm" :class="textClass">
            <div v-if="message.deleted" class="italic opacity-60">
              This message was deleted
            </div>
            <div v-else>
              {{ message.content }}
              <div v-if="message.edited" class="text-xs opacity-60 mt-1">(edited)</div>
            </div>
          </div>

          <!-- Media content -->
          <div v-else-if="isMediaMessage" class="space-y-2">
            <!-- Image preview -->
            <div v-if="isImage" class="relative">
              <img 
                :src="message.content" 
                :alt="message.filename || 'Image'"
                class="max-w-full h-auto rounded-lg max-h-64 object-cover"
              />
            </div>

            <!-- Video preview -->
            <div v-else-if="isVideo" class="relative">
              <video 
                :src="message.content"
                class="max-w-full h-auto rounded-lg max-h-64"
                controls
              />
            </div>

            <!-- Audio player -->
            <div v-else-if="isAudio" class="flex items-center gap-2">
              <svg class="w-6 h-6" :class="isOwnMessage ? 'text-blue-100' : 'text-gray-600'" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 3v9.28c-.47-.46-1.12-.75-1.84-.75-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3V7h4V3h-4z"/>
              </svg>
              <audio 
                :src="message.content"
                controls
                class="flex-1"
              />
            </div>

            <!-- File download -->
            <div v-else class="flex items-center gap-2 p-2 bg-opacity-20 rounded-lg" :class="isOwnMessage ? 'bg-blue-200' : 'bg-gray-200'">
              <svg class="w-6 h-6 flex-shrink-0" :class="isOwnMessage ? 'text-blue-100' : 'text-gray-600'" fill="currentColor" viewBox="0 0 24 24">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-8-6z"/>
              </svg>
              <a 
                :href="message.content" 
                :download="message.filename || 'download'"
                :class="isOwnMessage ? 'text-blue-100 hover:text-white' : 'text-gray-700 hover:text-gray-900'"
                class="text-sm font-medium underline"
              >
                {{ message.filename || 'Download file' }}
              </a>
            </div>

            <!-- Filename if available -->
            <div v-if="message.filename" class="text-xs opacity-70 mt-1">
              {{ message.filename }}
            </div>
          </div>

          <!-- Message status for own messages -->
          <div v-if="isOwnMessage" class="flex items-center justify-end mt-1 space-x-1">
            <span class="text-xs" :class="timestampClass">{{ formatTime(message.created_at || message.timestamp) }}</span>
            <div class="flex items-center">
              <!-- Sending -->
              <svg v-if="message.status === 'sending'" class="w-3 h-3 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <!-- Sent -->
              <svg v-else-if="message.status === 'sent'" class="w-3 h-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <!-- Read -->
              <svg v-else-if="message.status === 'read'" class="w-3 h-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13l4 4L23 7" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../../stores/auth'

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

const authStore = useAuthStore()

const currentUserId = computed(() => authStore.user?.id || '1')
const isOwnMessage = computed(() => props.message.sender_id === currentUserId.value)

const messageBubbleClass = computed(() => {
  if (isOwnMessage.value) {
    return 'bg-blue-500 text-white ml-auto'
  }
  return 'bg-white border border-gray-200'
})

const textClass = computed(() => {
  return isOwnMessage.value ? 'text-white' : 'text-gray-900'
})

const timestampClass = computed(() => {
  return isOwnMessage.value ? 'text-blue-100' : 'text-gray-500'
})

const isImage = computed(() => {
  const content = props.message.content || ''
  return /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(content) || props.message.type === 'image'
})

const isVideo = computed(() => {
  const content = props.message.content || ''
  return /\.(mp4|webm|ogg|mov|avi)$/i.test(content) || props.message.type === 'video'
})

const isAudio = computed(() => {
  const content = props.message.content || ''
  return /\.(mp3|wav|ogg|m4a|flac)$/i.test(content) || props.message.type === 'audio'
})

const isMediaMessage = computed(() => {
  return isImage.value || isVideo.value || isAudio.value || (props.message.type && props.message.type !== 'text')
})

function formatTime(timestamp) {
  if (!timestamp) return 'Just now'
  
  const date = new Date(timestamp)
  if (isNaN(date.getTime())) return 'Just now'
  
  const now = new Date()
  const diffInHours = (now - date) / (1000 * 60 * 60)
  
  if (diffInHours < 24) {
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    })
  } else {
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    })
  }
}
</script>
