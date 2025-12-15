import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import router from './router'
import App from './App.vue'
import './style.css'

// Import locales
import en from './locales/en.json'
import fr from './locales/fr.json'
import rw from './locales/rw.json'

// Create i18n instance
const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('locale') || 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    fr,
    rw
  }
})

// Create Pinia store
const pinia = createPinia()

// Create and mount app
const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(i18n)

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err, info)
}

// Global properties for debugging
if (import.meta.env.DEV) {
  app.config.globalProperties.$log = console.log
}

app.mount('#app')

// Service Worker registration for PWA features
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('SW registered: ', registration)
      })
      .catch((registrationError) => {
        console.log('SW registration failed: ', registrationError)
      })
  })
}

// Handle online/offline status
window.addEventListener('online', () => {
  console.log('App is online')
  // Reconnect chat if needed
})

window.addEventListener('offline', () => {
  console.log('App is offline')
  // Handle offline state
})

// Handle visibility change for chat optimization
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    console.log('App is hidden')
    // Reduce chat polling or pause real-time updates
  } else {
    console.log('App is visible')
    // Resume full functionality
  }
})