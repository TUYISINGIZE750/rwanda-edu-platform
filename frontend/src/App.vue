<template>
  <div :class="{ 'lite-mode': settingsStore.liteMode }" class="min-h-screen">
    <router-view />
  </div>
</template>

<script setup>
import { useSettingsStore } from './stores/settings'

const settingsStore = useSettingsStore()
</script>
