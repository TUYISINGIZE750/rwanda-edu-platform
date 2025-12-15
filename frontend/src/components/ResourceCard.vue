<template>
  <div class="card hover:shadow-md transition-shadow">
    <div class="flex items-start gap-3">
      <div v-if="!settingsStore.liteMode" class="w-12 h-12 bg-gray-200 rounded flex-shrink-0"></div>
      <div class="flex-1">
        <h4 class="font-semibold">{{ resource.title }}</h4>
        <p class="text-sm text-gray-600">{{ formatSize(resource.size) }}</p>
        <a :href="resource.url" target="_blank" class="text-primary text-sm mt-2 inline-block">
          Download
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSettingsStore } from '../stores/settings'

const settingsStore = useSettingsStore()
const props = defineProps(['resource'])

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}
</script>
