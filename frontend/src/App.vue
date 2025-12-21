<template>
  <div :class="{ 'lite-mode': settingsStore.liteMode }" class="min-h-screen">
    <ServerWakeUp v-if="showWakeUp" />
    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSettingsStore } from './stores/settings'
import ServerWakeUp from './components/ServerWakeUp.vue'

const settingsStore = useSettingsStore()
const showWakeUp = ref(false)

onMounted(() => {
  const lastWakeUp = localStorage.getItem('lastServerWakeUp')
  const now = Date.now()
  
  // Show wake-up if last wake was more than 15 minutes ago
  if (!lastWakeUp || now - parseInt(lastWakeUp) > 15 * 60 * 1000) {
    showWakeUp.value = true
    localStorage.setItem('lastServerWakeUp', now.toString())
  }
})
</script>
