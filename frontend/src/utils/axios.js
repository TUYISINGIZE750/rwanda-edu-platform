import axios from 'axios'

const API_URL = 'https://rwanda-edu-platform.onrender.com/api/v1'

const axiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default axiosInstance
