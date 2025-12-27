// Keep backend alive by pinging every 10 minutes
const BACKEND_URL = 'https://rwanda-edu-platform.onrender.com'
const PING_INTERVAL = 10 * 60 * 1000 // 10 minutes

let pingInterval = null

export function startKeepAlive() {
  if (pingInterval) return
  
  const ping = async () => {
    try {
      await fetch(`${BACKEND_URL}/health`, { method: 'GET' })
    } catch (error) {
      // Silent fail
    }
  }
  
  ping()
  pingInterval = setInterval(ping, PING_INTERVAL)
}

export function stopKeepAlive() {
  if (pingInterval) {
    clearInterval(pingInterval)
    pingInterval = null
  }
}
