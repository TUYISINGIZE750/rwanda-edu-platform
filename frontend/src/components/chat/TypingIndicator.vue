<template>
  <div v-if="typingUsers.length > 0" class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-500">
    <div class="flex space-x-1">
      <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
      <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
      <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
    </div>
    <span>{{ typingText }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  typingUsers: {
    type: Array,
    default: () => []
  }
})

const typingText = computed(() => {
  const users = props.typingUsers
  if (users.length === 1) {
    return `${users[0].name} is typing...`
  } else if (users.length === 2) {
    return `${users[0].name} and ${users[1].name} are typing...`
  } else if (users.length > 2) {
    return `${users[0].name} and ${users.length - 1} others are typing...`
  }
  return ''
})
</script>

<style scoped>
@keyframes bounce {
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-6px);
  }
}

.animate-bounce {
  animation: bounce 1.4s infinite;
}
</style>