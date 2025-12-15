<template>
  <div class="fixed bottom-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg p-2 text-xs text-gray-600 shadow-lg border">
    <div class="flex items-center space-x-2">
      <span class="text-green-600 font-medium">v{{ appVersion }}</span>
      <span>•</span>
      <span>Vue {{ vueVersion }}</span>
      <button @click="checkForUpdates" class="text-blue-600 hover:text-blue-700 ml-2">
        🔄
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { version as vueVersion } from 'vue'

const appVersion = ref('1.0.0')

const checkForUpdates = () => {
  console.log('Checking for updates...')
  // This would trigger the update process
}

onMounted(() => {
  // Get app version from package.json if available
  appVersion.value = '1.0.0'
})
</script>