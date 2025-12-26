// Keep backend alive by pinging every 10 minutes
const BACKEND_URL = import.meta.env.VITE_API_URL || 'https://your-backend-url.com'
const PING_INTERVAL = 10 * 60 * 1000 // 10 minutes

let pingInterval = null

export function startKeepAlive() {
  if (pingInterval) return
  
  const ping = async () => {
    try {
      await fetch(`${BACKEND_URL}/health`, { method: 'GET' })
      console.log('[Keep-Alive] Backend pinged')
    } catch (error) {
      console.warn('[Keep-Alive] Ping failed:', error.message)
    }
  }
  
  ping() // Initial ping
  pingInterval = setInterval(ping, PING_INTERVAL)
}

export function stopKeepAlive() {
  if (pingInterval) {
    clearInterval(pingInterval)
    pingInterval = null
  }
}
