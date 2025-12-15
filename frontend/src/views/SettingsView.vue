<template>
  <div class="min-h-screen">
    <nav class="bg-white shadow-sm p-4">
      <div class="max-w-7xl mx-auto flex items-center gap-4">
        <router-link to="/" class="text-primary">←</router-link>
        <h1 class="text-xl font-bold">{{ t('nav.settings') }}</h1>
      </div>
    </nav>
    
    <main class="max-w-2xl mx-auto p-4 space-y-4">
      <div class="card">
        <h2 class="font-semibold mb-3">{{ t('settings.language') }}</h2>
        <select v-model="locale" @change="changeLocale" class="input">
          <option value="rw">Kinyarwanda</option>
          <option value="en">English</option>
          <option value="fr">Français</option>
        </select>
      </div>
      
      <div class="card">
        <label class="flex items-center justify-between">
          <span class="font-semibold">{{ t('settings.liteMode') }}</span>
          <input type="checkbox" v-model="liteMode" @change="settingsStore.toggleLiteMode" class="w-5 h-5" />
        </label>
        <p class="text-sm text-gray-600 mt-2">Reduces data usage for slow connections</p>
      </div>
      
      <div class="card">
        <label class="flex items-center justify-between">
          <span class="font-semibold">{{ t('settings.highContrast') }}</span>
          <input type="checkbox" v-model="highContrast" @change="settingsStore.toggleHighContrast" class="w-5 h-5" />
        </label>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSettingsStore } from '../stores/settings'

const { t, locale: i18nLocale } = useI18n()
const settingsStore = useSettingsStore()

const locale = ref(settingsStore.locale)
const liteMode = ref(settingsStore.liteMode)
const highContrast = ref(settingsStore.highContrast)

function changeLocale() {
  settingsStore.setLocale(locale.value)
  i18nLocale.value = locale.value
}
</script>
