import { openDB } from 'idb'

let db

export async function initDB() {
  db = await openDB('rwanda-edu-db', 1, {
    upgrade(db) {
      if (!db.objectStoreNames.contains('messages')) {
        db.createObjectStore('messages', { keyPath: 'channelId' })
      }
      if (!db.objectStoreNames.contains('resources')) {
        db.createObjectStore('resources', { keyPath: 'id' })
      }
      if (!db.objectStoreNames.contains('announcements')) {
        db.createObjectStore('announcements', { keyPath: 'id' })
      }
    }
  })
}

export async function saveMessages(channelId, messages) {
  await db.put('messages', { channelId, messages, timestamp: Date.now() })
}

export async function getMessages(channelId) {
  const data = await db.get('messages', channelId)
  return data?.messages || []
}

export async function saveResource(resource) {
  await db.put('resources', resource)
}

export async function getResources() {
  return await db.getAll('resources')
}

export async function saveAnnouncement(announcement) {
  await db.put('announcements', announcement)
}

export async function getAnnouncements() {
  return await db.getAll('announcements')
}
