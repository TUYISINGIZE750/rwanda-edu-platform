<template>
  <div class="w-60 bg-gray-50 border-l border-gray-200 flex-shrink-0 hidden xl:block">
    <div class="p-4">
      <h3 class="text-sm font-semibold text-gray-900 mb-3">Online — {{ onlineUsers.length }}</h3>
      
      <div class="space-y-2">
        <div v-for="user in onlineUsers" :key="user.id" 
             class="flex items-center space-x-3 p-2 rounded hover:bg-gray-100 cursor-pointer">
          <div class="relative">
            <img 
              :src="user.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=random`"
              :alt="user.name"
              class="w-8 h-8 rounded-full"
            />
            <div class="absolute -bottom-1 -right-1 w-3 h-3 rounded-full border-2 border-white"
                 :class="getStatusColor(user.status)"></div>
          </div>
          
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">{{ user.name }}</p>
            <p class="text-xs text-gray-500 truncate">{{ user.role }}</p>
          </div>
          
          <div v-if="user.isTyping" class="flex space-x-1">
            <div class="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
            <div class="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
            <div class="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
          </div>
        </div>
      </div>
      
      <div v-if="offlineUsers.length > 0" class="mt-6">
        <h3 class="text-sm font-semibold text-gray-900 mb-3">Offline — {{ offlineUsers.length }}</h3>
        
        <div class="space-y-2">
          <div v-for="user in offlineUsers" :key="user.id" 
               class="flex items-center space-x-3 p-2 rounded hover:bg-gray-100 cursor-pointer opacity-60">
            <div class="relative">
              <img 
                :src="user.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=random`"
                :alt="user.name"
                class="w-8 h-8 rounded-full grayscale"
              />
              <div class="absolute -bottom-1 -right-1 w-3 h-3 bg-gray-400 rounded-full border-2 border-white"></div>
            </div>
            
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-600 truncate">{{ user.name }}</p>
              <p class="text-xs text-gray-400 truncate">{{ user.role }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  users: {
    type: Array,
    default: () => []
  },
  typingUsers: {
    type: Array,
    default: () => []
  }
})

const onlineUsers = computed(() => {
  return props.users
    .filter(user => user.status === 'online')
    .map(user => ({
      ...user,
      isTyping: props.typingUsers.some(tu => tu.userId === user.id)
    }))
    .sort((a, b) => {
      // Sort by typing first, then by name
      if (a.isTyping && !b.isTyping) return -1
      if (!a.isTyping && b.isTyping) return 1
      return a.name.localeCompare(b.name)
    })
})

const offlineUsers = computed(() => {
  return props.users
    .filter(user => user.status !== 'online')
    .sort((a, b) => a.name.localeCompare(b.name))
})

function getStatusColor(status) {
  switch (status) {
    case 'online':
      return 'bg-green-500'
    case 'away':
      return 'bg-yellow-500'
    case 'busy':
      return 'bg-red-500'
    default:
      return 'bg-gray-400'
  }
}
</script>

<style scoped>
@keyframes bounce {
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-2px);
  }
}

.animate-bounce {
  animation: bounce 1.4s infinite;
}
</style>