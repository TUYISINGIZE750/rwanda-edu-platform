import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://rwanda-edu-platform.onrender.com/api/v1',
  timeout: 30000,  // Increased timeout for Render
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(config => {
  console.log('API Request:', config.method?.toUpperCase(), config.url)
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.config?.url, error.response?.status || error.code)
    
    // Handle network errors specifically
    if (error.code === 'ERR_NETWORK' || error.code === 'ERR_BLOCKED_BY_CLIENT') {
      console.error('Network/blocking error detected:', error.message)
    }
    
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api