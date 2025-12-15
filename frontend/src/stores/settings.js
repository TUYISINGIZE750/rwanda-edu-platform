import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  const liteMode = ref(localStorage.getItem('liteMode') === 'true')
  const locale = ref(localStorage.getItem('locale') || 'rw')
  const highContrast = ref(localStorage.getItem('highContrast') === 'true')
  
  function toggleLiteMode() {
    liteMode.value = !liteMode.value
    localStorage.setItem('liteMode', liteMode.value)
  }
  
  function setLocale(newLocale) {
    locale.value = newLocale
    localStorage.setItem('locale', newLocale)
  }
  
  function toggleHighContrast() {
    highContrast.value = !highContrast.value
    localStorage.setItem('highContrast', highContrast.value)
  }
  
  return { liteMode, locale, highContrast, toggleLiteMode, setLocale, toggleHighContrast }
})
