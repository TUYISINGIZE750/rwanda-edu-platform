import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../utils/api-new'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const token = ref(localStorage.getItem('token') || null)
  
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  
  async function login(email, password) {
    const response = await api.post('/auth/login', { email, password })
    token.value = response.data.access_token
    user.value = response.data.user
    localStorage.setItem('token', token.value)
    localStorage.setItem('user', JSON.stringify(user.value))
    api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }
  
  async function fetchUser() {
    if (token.value && !user.value) {
      try {
        const response = await api.get('/auth/me')
        user.value = response.data
        localStorage.setItem('user', JSON.stringify(user.value))
        return user.value
      } catch (error) {
        console.error('Failed to fetch user:', error)
        logout()
        throw error
      }
    }
    return user.value
  }
  
  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete api.defaults.headers.common['Authorization']
    window.location.href = '/login'
  }
  
  async function initAuth() {
    if (token.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      if (!user.value) {
        try {
          await fetchUser()
        } catch (error) {
          // User will be logged out by fetchUser on error
          return false
        }
      }
      return true
    }
    return false
  }
  
  return { user, token, isAuthenticated, login, logout, initAuth, fetchUser }
})
