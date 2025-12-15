import axios from 'axios'

// Auto-detect hostname for network access (works on phone too!)
const getBaseURL = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  // Use current hostname so it works on laptop and phone
  const hostname = window.location.hostname
  const baseURL = `http://${hostname}:8080/api/v1`
  console.log('🌐 API Base URL:', baseURL)
  return baseURL
}

const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 30000, // Increased timeout for network requests
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  console.log('📤 API Request:', config.method.toUpperCase(), config.url)
  return config
})

api.interceptors.response.use(
  response => {
    console.log('✅ API Response:', response.config.url, response.status)
    return response
  },
  error => {
    console.error('❌ API Error:', error.config?.url, error.message)
    if (error.response) {
      console.error('Response status:', error.response.status)
      console.error('Response data:', error.response.data)
    }
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
