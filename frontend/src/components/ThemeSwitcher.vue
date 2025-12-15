<template>
  <div class="relative">
    <button @click="showMenu = !showMenu" 
            class="p-2 rounded-full transition-all transform hover:scale-110"
            :class="themeColors[currentTheme].button">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
      </svg>
    </button>
    
    <div v-if="showMenu" class="absolute right-0 mt-2 w-64 bg-white rounded-2xl shadow-2xl border-2 border-gray-200 p-4 z-50">
      <h3 class="font-bold text-gray-900 mb-3 text-sm">Choose Theme</h3>
      <div class="space-y-2">
        <button v-for="(theme, key) in themes" :key="key"
                @click="setTheme(key)"
                class="w-full p-3 rounded-xl flex items-center gap-3 transition-all transform hover:scale-105"
                :class="currentTheme === key ? 'ring-2 ring-offset-2' : 'hover:bg-gray-50'"
                :style="{ backgroundColor: theme.preview, color: theme.text, ringColor: theme.ring }">
          <span class="text-2xl">{{ theme.icon }}</span>
          <div class="flex-1 text-left">
            <p class="font-semibold text-sm">{{ theme.name }}</p>
            <p class="text-xs opacity-75">{{ theme.desc }}</p>
          </div>
          <svg v-if="currentTheme === key" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const showMenu = ref(false)
const currentTheme = ref('light')

const themes = {
  light: {
    name: 'Light Mode',
    desc: 'Clean & bright',
    icon: '☀️',
    preview: '#f3f4f6',
    text: '#111827',
    ring: '#3b82f6'
  },
  dark: {
    name: 'Dark Mode',
    desc: 'Easy on eyes',
    icon: '🌙',
    preview: '#1f2937',
    text: '#f9fafb',
    ring: '#60a5fa'
  },
  vibrant: {
    name: 'Vibrant',
    desc: 'Colorful & fun',
    icon: '🎨',
    preview: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    text: '#ffffff',
    ring: '#a78bfa'
  },
  ocean: {
    name: 'Ocean',
    desc: 'Cool & calm',
    icon: '🌊',
    preview: 'linear-gradient(135deg, #667eea 0%, #06b6d4 100%)',
    text: '#ffffff',
    ring: '#06b6d4'
  },
  sunset: {
    name: 'Sunset',
    desc: 'Warm & cozy',
    icon: '🌅',
    preview: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
    text: '#ffffff',
    ring: '#f59e0b'
  }
}

const themeColors = {
  light: { button: 'bg-gray-200 text-gray-700 hover:bg-gray-300' },
  dark: { button: 'bg-gray-800 text-white hover:bg-gray-700' },
  vibrant: { button: 'bg-gradient-to-r from-purple-500 to-pink-500 text-white' },
  ocean: { button: 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white' },
  sunset: { button: 'bg-gradient-to-r from-orange-500 to-red-500 text-white' }
}

function setTheme(theme) {
  currentTheme.value = theme
  localStorage.setItem('chat-theme', theme)
  document.documentElement.setAttribute('data-theme', theme)
  showMenu.value = false
  
  // Apply theme to body class for better CSS control
  document.body.className = document.body.className.replace(/theme-\w+/g, '')
  document.body.classList.add(`theme-${theme}`)
  
  const root = document.documentElement
  if (theme === 'dark') {
    root.style.setProperty('--bg-primary', '#111827')
    root.style.setProperty('--bg-secondary', '#1f2937')
    root.style.setProperty('--text-primary', '#f9fafb')
    root.style.setProperty('--text-secondary', '#d1d5db')
    root.style.backgroundColor = '#111827'
  } else if (theme === 'vibrant') {
    root.style.setProperty('--bg-primary', '#667eea')
    root.style.setProperty('--bg-secondary', '#764ba2')
    root.style.setProperty('--text-primary', '#ffffff')
    root.style.setProperty('--text-secondary', '#e0e7ff')
    root.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  } else if (theme === 'ocean') {
    root.style.setProperty('--bg-primary', '#0891b2')
    root.style.setProperty('--bg-secondary', '#06b6d4')
    root.style.setProperty('--text-primary', '#ffffff')
    root.style.setProperty('--text-secondary', '#cffafe')
    root.style.background = 'linear-gradient(135deg, #0891b2 0%, #06b6d4 100%)'
  } else if (theme === 'sunset') {
    root.style.setProperty('--bg-primary', '#f59e0b')
    root.style.setProperty('--bg-secondary', '#ef4444')
    root.style.setProperty('--text-primary', '#ffffff')
    root.style.setProperty('--text-secondary', '#fef3c7')
    root.style.background = 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)'
  } else {
    root.style.setProperty('--bg-primary', '#ffffff')
    root.style.setProperty('--bg-secondary', '#f3f4f6')
    root.style.setProperty('--text-primary', '#111827')
    root.style.setProperty('--text-secondary', '#6b7280')
    root.style.backgroundColor = '#ffffff'
  }
}

onMounted(() => {
  const saved = localStorage.getItem('chat-theme') || 'light'
  setTheme(saved)
  
  // Close menu when clicking outside
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

function handleClickOutside(event) {
  if (!event.target.closest('.relative')) {
    showMenu.value = false
  }
}
</script>
