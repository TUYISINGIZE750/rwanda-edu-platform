import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8080/api/v1',
  timeout: 10000,
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
    console.error('API Error:', error.config?.url, error.response?.status)
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api