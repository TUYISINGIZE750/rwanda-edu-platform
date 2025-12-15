<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <button @click="$router.go(-1)" class="text-gray-600 hover:text-gray-900">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <div>
              <h1 class="text-xl font-semibold text-gray-900">{{ group?.name }}</h1>
              <p class="text-sm text-gray-600">{{ channel?.name }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <button v-if="authStore.user?.role === 'TEACHER'" @click="showMembers = true" 
                    class="text-gray-600 hover:text-gray-900">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </button>
            <span class="text-sm text-gray-600">{{ authStore.user?.full_name }}</span>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Channels Sidebar -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Channels</h3>
            </div>
            <div class="p-4">
              <div v-if="loadingChannels" class="text-center py-4">
                <div class="animate-spin h-6 w-6 border-2 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
              </div>
              <div v-else class="space-y-2">
                <button v-for="ch in channels" :key="ch.id"
                        @click="selectChannel(ch.id)"
                        class="w-full text-left p-3 rounded-lg hover:bg-gray-50 transition-colors"
                        :class="{ 'bg-blue-50 border-l-4 border-blue-500': ch.id === channelId }">
                  <div class="flex justify-between items-center">
                    <span class="font-medium text-gray-900"># {{ ch.name }}</span>
                    <span v-if="ch.unread_count > 0" 
                          class="bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                      {{ ch.unread_count }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 mt-1">{{ ch.description }}</p>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Messages Area -->
        <div class="lg:col-span-3">
          <div class="bg-white rounded-lg shadow h-[600px] flex flex-col">
            <!-- Messages Header -->
            <div class="px-6 py-4 border-b border-gray-200">
              <div class="flex justify-between items-center">
                <div>
                  <h3 class="text-lg font-medium text-gray-900"># {{ channel?.name }}</h3>
                  <p class="text-sm text-gray-600">{{ channel?.description }}</p>
                </div>
                <div class="flex space-x-2">
                  <button v-if="authStore.user?.role !== 'STUDENT'" @click="uploadResource"
                          class="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                    Upload Resource
                  </button>
                </div>
              </div>
            </div>

            <!-- Messages List -->
            <div class="flex-1 overflow-y-auto p-6 space-y-4" ref="messagesContainer">
              <div v-if="loadingMessages" class="text-center py-8">
                <div class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
                <p class="mt-2 text-gray-600">Loading messages...</p>
              </div>
              
              <div v-else-if="messages.length === 0" class="text-center py-8">
                <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <p class="text-gray-600">No messages yet</p>
                <p class="text-sm text-gray-500 mt-1">Be the first to start the conversation!</p>
              </div>
              
              <div v-else>
                <div v-for="message in messages" :key="message.id" class="flex space-x-3">
                  <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <span class="text-sm font-medium text-blue-600">
                      {{ message.author_name?.charAt(0)?.toUpperCase() }}
                    </span>
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center space-x-2 mb-1">
                      <span class="font-medium text-gray-900">{{ message.author_name }}</span>
                      <span class="text-xs text-gray-500">{{ formatTime(message.created_at) }}</span>
                      <span v-if="message.status === 'pending'" 
                            class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
                        Pending Approval
                      </span>
                    </div>
                    <div class="text-gray-700">
                      <p>{{ message.content }}</p>
                      <div v-if="message.attachments?.length > 0" class="mt-2 space-y-2">
                        <div v-for="(attachment, idx) in message.attachments" :key="idx">
                          <!-- Image Preview -->
                          <div v-if="attachment.type === 'image'" class="rounded-lg overflow-hidden border">
                            <img :src="`http://localhost:8080${attachment.url}`" 
                                 :alt="attachment.filename"
                                 @click="openImageViewer(`http://localhost:8080${attachment.url}`, message.author_name, message.created_at, attachment)"
                                 class="max-w-md w-full h-auto cursor-pointer hover:opacity-90" />
                            <div class="px-2 py-1 bg-gray-50 text-xs text-gray-600">
                              {{ attachment.filename }} ({{ formatFileSize(attachment.size) }})
                            </div>
                          </div>
                          
                          <!-- Video Preview -->
                          <div v-else-if="attachment.type === 'video'" class="rounded-lg overflow-hidden border">
                            <video controls class="max-w-md w-full">
                              <source :src="`http://localhost:8080${attachment.url}`" />
                              Your browser does not support video playback.
                            </video>
                            <div class="px-2 py-1 bg-gray-50 text-xs text-gray-600">
                              {{ attachment.filename }} ({{ formatFileSize(attachment.size) }})
                            </div>
                          </div>
                          
                          <!-- Audio Preview -->
                          <div v-else-if="attachment.type === 'audio'" class="rounded-lg border p-3 bg-gray-50">
                            <audio controls class="w-full max-w-md">
                              <source :src="`http://localhost:8080${attachment.url}`" />
                              Your browser does not support audio playback.
                            </audio>
                            <div class="text-xs text-gray-600 mt-1">
                              {{ attachment.filename }} ({{ formatFileSize(attachment.size) }})
                            </div>
                          </div>
                          
                          <!-- Document/Other Files -->
                          <div v-else class="flex items-center space-x-2 p-2 bg-gray-50 rounded border">
                            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                            </svg>
                            <a :href="`http://localhost:8080${attachment.url}`" target="_blank" download
                               class="text-blue-600 hover:text-blue-700 text-sm flex-1">
                              {{ attachment.filename }} ({{ formatFileSize(attachment.size) }})
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Message Input -->
            <div class="border-t border-gray-200 p-4">
              <!-- Upload Preview -->
              <div v-if="uploadedAttachments.length > 0" class="mb-3 flex flex-wrap gap-2">
                <div v-for="(file, idx) in uploadedAttachments" :key="idx" 
                     class="relative bg-blue-50 border border-blue-200 rounded px-3 py-1 text-sm">
                  <span class="text-blue-700">{{ file.filename }}</span>
                  <button @click="uploadedAttachments.splice(idx, 1)" 
                          class="ml-2 text-blue-600 hover:text-blue-800">×</button>
                </div>
              </div>
              
              <form @submit.prevent="sendMessage" class="flex space-x-4">
                <div class="flex-1">
                  <textarea v-model="newMessage" 
                           placeholder="Type your message..."
                           class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                           rows="2"
                           @keydown.enter.prevent="sendMessage"
                           :disabled="sending"></textarea>
                </div>
                <div class="flex flex-col space-y-2">
                  <button type="button" @click="$refs.fileInput.click()"
                          class="p-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                    </svg>
                  </button>
                  <button type="submit" 
                          :disabled="(!newMessage.trim() && uploadedAttachments.length === 0) || sending"
                          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed">
                    <svg v-if="sending" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </button>
                </div>
              </form>
              <input ref="fileInput" type="file" class="hidden" @change="handleFileUpload" multiple>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Members Modal -->
    <div v-if="showMembers" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg max-w-md w-full mx-4 max-h-96 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-medium text-gray-900">Group Members</h3>
          <button @click="showMembers = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6 overflow-y-auto">
          <div v-if="loadingMembers" class="text-center py-4">
            <div class="animate-spin h-6 w-6 border-2 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
          </div>
          <div v-else class="space-y-3">
            <div v-for="member in members" :key="member.id" class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <span class="text-sm font-medium text-blue-600">
                  {{ member.full_name?.charAt(0)?.toUpperCase() }}
                </span>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900">{{ member.full_name }}</p>
                <p class="text-xs text-gray-500">{{ member.role }} {{ member.grade ? `- Grade ${member.grade}` : '' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Image Viewer -->
    <ImageViewer 
      :isOpen="imageViewerOpen"
      :imageUrl="selectedImageUrl"
      :senderName="selectedImageSender"
      :timestamp="selectedImageTime"
      :attachment="selectedImageAttachment"
      @close="imageViewerOpen = false"
      @forward="handleForward"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ImageViewer from '../components/ImageViewer.vue'
import api from '../utils/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const groupId = ref(route.params.groupId)
const channelId = ref(route.params.channelId)

const group = ref(null)
const channel = ref(null)
const channels = ref([])
const messages = ref([])
const members = ref([])

const newMessage = ref('')
const selectedFiles = ref([])
const uploadedAttachments = ref([])
const imageViewerOpen = ref(false)
const selectedImageUrl = ref('')
const selectedImageSender = ref('')
const selectedImageTime = ref('')
const selectedImageAttachment = ref(null)

const loadingChannels = ref(true)
const loadingMessages = ref(true)
const loadingMembers = ref(false)
const sending = ref(false)
const showMembers = ref(false)

const messagesContainer = ref(null)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  await loadGroupData()
  await loadChannels()
  
  if (channelId.value) {
    await loadMessages()
  } else if (channels.value.length > 0) {
    // Select first channel if none specified
    selectChannel(channels.value[0].id)
  }
})

async function loadGroupData() {
  try {
    const response = await api.get(`/directory/groups/${groupId.value}`)
    group.value = response.data
  } catch (err) {
    console.error('Failed to load group:', err)
    router.push('/home')
  }
}

async function loadChannels() {
  try {
    const response = await api.get(`/directory/groups/${groupId.value}/channels`)
    channels.value = response.data || []
    
    // Add mock unread counts
    channels.value.forEach(channel => {
      channel.unread_count = Math.floor(Math.random() * 3)
    })
  } catch (err) {
    console.error('Failed to load channels:', err)
  } finally {
    loadingChannels.value = false
  }
}

async function loadMessages() {
  if (!channelId.value) return
  
  loadingMessages.value = true
  try {
    const response = await api.get(`/messages/channel/${channelId.value}`)
    messages.value = response.data || []
    
    // Debug: Log messages with attachments
    const withAttachments = messages.value.filter(m => m.attachments && m.attachments.length > 0)
    if (withAttachments.length > 0) {
      console.log('Messages with attachments:', withAttachments)
    }
    
    // Find current channel
    channel.value = channels.value.find(ch => ch.id === parseInt(channelId.value))
    
    // Scroll to bottom
    await nextTick()
    scrollToBottom()
  } catch (err) {
    console.error('Failed to load messages:', err)
  } finally {
    loadingMessages.value = false
  }
}

async function loadMembers() {
  if (loadingMembers.value) return
  
  loadingMembers.value = true
  try {
    const response = await api.get(`/directory/groups/${groupId.value}/members`)
    members.value = response.data || []
  } catch (err) {
    console.error('Failed to load members:', err)
  } finally {
    loadingMembers.value = false
  }
}

function selectChannel(newChannelId) {
  channelId.value = newChannelId
  router.push(`/hubs/${groupId.value}/channels/${newChannelId}`)
  loadMessages()
}

async function sendMessage() {
  if ((!newMessage.value.trim() && uploadedAttachments.value.length === 0) || sending.value) return
  
  sending.value = true
  try {
    const payload = {
      content: newMessage.value.trim() || '📎 Attachment',
      channel_id: parseInt(channelId.value),
      attachments: uploadedAttachments.value
    }
    
    await api.post('/messages', payload)
    newMessage.value = ''
    selectedFiles.value = []
    uploadedAttachments.value = []
    
    // Reload messages
    await loadMessages()
  } catch (err) {
    console.error('Failed to send message:', err)
    alert('Failed to send message. Please try again.')
  } finally {
    sending.value = false
  }
}

async function handleFileUpload(event) {
  const files = Array.from(event.target.files)
  if (files.length === 0) return
  
  selectedFiles.value = files
  
  try {
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    
    const response = await api.post('/uploads/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    uploadedAttachments.value = response.data.files
  } catch (err) {
    console.error('Failed to upload files:', err)
    alert('Failed to upload files. Please try again.')
  }
}

function uploadResource() {
  router.push(`/upload-resource?group=${groupId.value}&channel=${channelId.value}`)
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatFileSize(bytes) {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

function openImageViewer(url, sender, time, attachment) {
  selectedImageUrl.value = url
  selectedImageSender.value = sender
  selectedImageTime.value = time
  selectedImageAttachment.value = attachment
  imageViewerOpen.value = true
}

async function handleForward(attachment) {
  // Show channel selection modal or forward to current channel
  const confirmed = confirm('Forward this image to another channel?')
  if (confirmed) {
    alert('✅ Image forwarded! (Feature coming soon)')
  }
}

// Watch for members modal
function watchShowMembers() {
  if (showMembers.value && members.value.length === 0) {
    loadMembers()
  }
}
</script>