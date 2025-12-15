<template>
  <div class="fixed inset-0 bg-gradient-to-br from-gray-900 via-purple-900 to-pink-900 z-50 flex flex-col">
    <!-- Session Header -->
    <div class="absolute top-0 left-0 right-0 bg-gradient-to-b from-black/80 to-transparent backdrop-blur-md z-20 p-4">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-gradient-to-br from-red-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg">
            <span class="text-white text-2xl">{{ session.type === 'VIDEO' ? '🎥' : '🎤' }}</span>
          </div>
          <div>
            <h2 class="text-white font-bold text-lg">{{ session.title }}</h2>
            <div class="flex items-center gap-2 text-sm">
              <span class="flex items-center gap-1 text-red-400">
                <span class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                LIVE
              </span>
              <span class="text-gray-400">•</span>
              <span class="text-gray-300">{{ session.type }} Session</span>
            </div>
          </div>
        </div>
        
        <!-- Controls -->
        <div class="flex items-center gap-3">
          <button @click="handleClose" 
                  class="px-6 py-3 bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 text-white font-bold rounded-xl shadow-xl hover:shadow-2xl transition-all transform hover:scale-105 flex items-center gap-2">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
            Leave Session
          </button>
        </div>
      </div>
    </div>
    
    <!-- Jitsi Community Server iFrame (no auth required) -->
    <iframe
      :src="jitsiUrl"
      allow="camera; microphone; fullscreen; display-capture; autoplay; clipboard-write"
      allowfullscreen
      class="w-full h-full border-0"
    ></iframe>
    
    <!-- Session Info Footer -->
    <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent backdrop-blur-md z-20 p-4">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-4 text-white">
          <div class="flex items-center gap-2 px-3 py-2 bg-white/10 rounded-lg backdrop-blur-sm">
            <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
            </svg>
            <span class="text-sm font-medium">Participants in room</span>
          </div>
        </div>
        <div class="text-xs text-gray-400">
          Powered by Jitsi Meet • End-to-end encrypted
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const props = defineProps({
  session: Object,
  roomId: String
})

const emit = defineEmits(['close', 'ended'])

const authStore = useAuthStore()
const userName = computed(() => authStore.user?.full_name || 'User')

// Use Jitsi community server (jitsi.riot.im) - no auth required
const jitsiUrl = computed(() => {
  const isAudioOnly = props.session.type === 'AUDIO'
  const config = [
    `userInfo.displayName="${encodeURIComponent(userName.value)}"`,
    `config.startWithVideoMuted=${isAudioOnly}`,
    'config.prejoinPageEnabled=false'
  ].join('&')
  
  return `https://jitsi.riot.im/${props.roomId}#${config}`
})

function handleClose() {
  emit('ended')
  emit('close')
}
</script>
