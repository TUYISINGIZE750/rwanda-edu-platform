// Rwanda timezone utilities (CAT/UTC+2)

export const RWANDA_TIMEZONE = 'Africa/Kigali'

export function formatRwandaTime(timestamp, format = 'full') {
  const date = new Date(timestamp)
  
  const options = {
    timeZone: RWANDA_TIMEZONE
  }
  
  switch (format) {
    case 'full':
      return date.toLocaleString('en-RW', {
        ...options,
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    case 'date':
      return date.toLocaleDateString('en-RW', {
        ...options,
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    case 'time':
      return date.toLocaleTimeString('en-RW', {
        ...options,
        hour: '2-digit',
        minute: '2-digit'
      })
    case 'relative':
      return formatRelativeTime(date)
    default:
      return date.toLocaleString('en-RW', options)
  }
}

export function formatRelativeTime(timestamp) {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)

  if (diff < 60) return 'Just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`
  
  return formatRwandaTime(date, 'date')
}

export function getRwandaNow() {
  return new Date().toLocaleString('en-RW', {
    timeZone: RWANDA_TIMEZONE
  })
}
