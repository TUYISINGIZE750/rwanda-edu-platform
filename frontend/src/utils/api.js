import axios from 'axios'

// Production backend URL
const PRODUCTION_API = 'https://rwanda-edu-platform.onrender.com/api/v1'

const getBaseURL = () => {
  // Always use production API for deployed frontend
  if (window.location.hostname.includes('pages.dev') || window.location.hostname.includes('tssanywhere')) {
    console.log('🌐 Using Production API:', PRODUCTION_API)
    return PRODUCTION_API
  }
  
  // Local development
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
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
