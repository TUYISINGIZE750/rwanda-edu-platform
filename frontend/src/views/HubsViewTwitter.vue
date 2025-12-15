<template>
  <div class="h-screen flex bg-white">
    <!-- Sidebar -->
    <div class="w-64 border-r border-gray-200 flex flex-col sticky top-0 h-screen">
      <!-- Logo -->
      <div class="p-4 border-b border-gray-200">
        <div class="flex items-center gap-2 font-bold text-2xl text-blue-500">
          <span>💬</span>
          <span>TSSANYWHERE</span>
        </div>
      </div>

      <!-- Channels -->
      <div class="flex-1 overflow-y-auto p-4 space-y-2">
        <div class="text-xs font-bold text-gray-500 px-4 py-2">CHANNELS</div>
        <button v-for="channel in channels" :key="channel.id"
                @click="selectChannel(channel)"
                :class="activeChannelId === channel.id ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' : 'text-gray-700 hover:bg-gray-50'"
                class="w-full flex items-center gap-3 px-4 py-3 rounded-full transition-all text-left">
          <span class="text-lg">#</span>
          <span class="font-medium">{{ channel.name }}</span>
        </button>
      </div>

      <!-- User Profile -->
      <div class="p-4 border-t border-gray-200">
        <button @click="$router.push('/teacher-dashboard')" class="w-full px-4 py-3 bg-blue-500 text-white rounded-full font-bold hover:bg-blue-600 transition-all">
          Back to Dashboard
        </button>
      </div>
    </div>

    <!-- Main Feed -->
    <div class="flex-1 max-w-2xl border-r border-gray-200 flex flex-col">
      <!-- Header -->
      <div class="sticky top-0 backdrop-blur bg-white/80 border-b border-gray-200 px-4 py-3 z-10">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ activeChannel?.name }}</h2>
            <p class="text-sm text-gray-500">{{ onlineCount }} online</p>
          </div>
          <button @click="showSettings = !showSettings" class="p-2 hover:bg-blue-50 rounded-full transition-all">
            <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Messages Feed -->
      <div ref="messagesContainer" class="flex-1 overflow-y-auto">
        <div v-if="loadingMessages" class="flex justify-center items-center h-full">
          <div class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
        </div>

        <div v-else-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-gray-500">
          <svg class="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <p class="text-lg font-medium">No messages yet</p>
          <p class="text-sm">Start the conversation!</p>
        </div>

        <div v-else class="divide-y divide-gray-200">
          <div v-for="msg in messages" :key="msg.id" class="p-4 hover:bg-gray-50 transition-all cursor-pointer border-b border-gray-100 group">
            <div class="flex gap-3">
              <!-- Avatar -->
              <div class="w-12 h-12 rounded-full flex-shrink-0 flex items-center justify-center text-white font-bold shadow-md"
                   :class="msg.sender_id === authStore.user?.id ? 'bg-blue-500' : 'bg-gray-400'">
                {{ msg.sender_name?.charAt(0) || 'U' }}
              </div>

              <!-- Content -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-gray-900">{{ msg.sender_name }}</span>
                  <span class="text-gray-500">@{{ msg.sender_name?.toLowerCase().replace(/\s/g, '') }}</span>
                  <span class="text-gray-500">·</span>
                  <span class="text-gray-500 text-sm">{{ formatTime(msg.created_at) }}</span>
                </div>

                <!-- Reply Preview -->
                <div v-if="msg.reply_to" class="mt-2 p-3 bg-gray-50 rounded-lg border border-gray-200 text-sm">
                  <p class="font-semibold text-gray-900">{{ msg.reply_to.sender_name }}</p>
                  <p class="text-gray-600">{{ msg.reply_to.content }}</p>
                </div>

                <!-- Message Text -->
                <p class="text-gray-900 text-base mt-2 break-words">{{ msg.content }}</p>

                <!-- Media -->
                <div v-if="msg.file_url" class="mt-3 rounded-2xl overflow-hidden border border-gray-200 max-w-sm">
                  <img v-if="msg.file_type?.startsWith('image/')" 
                       :src="getFullFileUrl(msg.file_url)" 
                       :alt="msg.file_name"
                       class="w-full h-auto cursor-pointer hover:opacity-90 transition-opacity"
                       @click="openImageModal(getFullFileUrl(msg.file_url), msg.file_name, msg.file_size)" />
                  <video v-else-if="msg.file_type?.startsWith('video/')" 
                         :src="getFullFileUrl(msg.file_url)" 
                         controls 
                         class="w-full h-auto" />
                </div>

                <!-- Reactions -->
                <div v-if="getMessageReactions(msg.id) && Object.keys(getMessageReactions(msg.id)).length > 0" class="flex gap-2 mt-3 flex-wrap">
                  <button v-for="(count, emoji) in getMessageReactions(msg.id)" :key="emoji"
                          @click="toggleReaction(msg.id, emoji)"
                          class="px-3 py-1 rounded-full text-sm bg-gray-100 hover:bg-gray-200 transition-all flex items-center gap-1"
                          :class="hasUserReaction(msg.id, emoji) ? 'bg-blue-100 text-blue-600' : ''">
                    {{ emoji }} <span class="text-xs">{{ count }}</span>
                  </button>
                </div>

                <!-- Actions -->
                <div class="flex gap-8 mt-3 text-gray-500 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button @click="replyTo(msg)" class="flex items-center gap-2 hover:text-blue-500 transition-all">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6-6m-6 6l-6-6" />
                    </svg>
                    <span class="text-xs">Reply</span>
                  </button>
                  <button @click="toggleReactionPicker(msg.id)" class="flex items-center gap-2 hover:text-blue-500 transition-all">
                    <span class="text-lg">😊</span>
                  </button>
                  <button @click="shareMessage(msg)" class="flex items-center gap-2 hover:text-blue-500 transition-all">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </button>
                </div>

                <!-- Quick Reaction Picker -->
                <div v-if="activeReactionPicker === msg.id" class="flex gap-2 mt-3 p-2 bg-gray-100 rounded-lg">
                  <button v-for="emoji in quickReactions" :key="emoji"
                          @click="addQuickReaction(msg.id, emoji)"
                          class="text-2xl hover:scale-125 transition-transform">
                    {{ emoji }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Compose Area -->
      <div class="border-t border-gray-200 p-4 bg-white">
        <!-- Reply Banner -->
        <div v-if="replyingTo" class="mb-3 p-3 bg-blue-50 rounded-lg flex items-center justify-between">
          <div>
            <p class="text-xs font-semibold text-blue-600">Replying to {{ replyingTo.sender_name }}</p>
            <p class="text-sm text-gray-600">{{ replyingTo.content }}</p>
          </div>
          <button @click="replyingTo = null" class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
            </svg>
          </button>
        </div>

        <!-- Input -->
        <div class="flex gap-4">
          <div class="w-12 h-12 rounded-full flex-shrink-0 flex items-center justify-center bg-blue-500 text-white font-bold shadow-md">
            {{ authStore.user?.full_name?.charAt(0) || 'U' }}
          </div>
          <div class="flex-1">
            <textarea v-model="newMessage"
                      @keydown.enter.ctrl="sendMessage"
                      placeholder="What's happening?!"
                      class="w-full text-xl text-gray-900 placeholder-gray-500 resize-none focus:outline-none bg-transparent"
                      rows="3"></textarea>
            <div class="flex items-center justify-between mt-4">
              <div class="flex gap-2">
                <button @click="selectFileType('image')" class="p-2 text-blue-500 hover:bg-blue-50 rounded-full transition-all">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
                  </svg>
                </button>
                <button @click="showEmojiPicker = !showEmojiPicker" class="p-2 text-blue-500 hover:bg-blue-50 rounded-full transition-all">
                  <span class="text-xl">😊</span>
                </button>
              </div>
              <button @click="sendMessage"
                      :disabled="!newMessage.trim() || sending"
                      class="px-6 py-2 bg-blue-500 text-white rounded-full font-bold hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all">
                {{ sending ? '...' : 'Post' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Sidebar (Trends/Info) -->
    <div class="w-80 p-4 hidden lg:block">
      <div class="bg-gray-100 rounded-3xl p-4 mb-4">
        <input type="text" placeholder="Search TSSANYWHERE" class="w-full px-4 py-3 bg-white rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>

      <!-- What's happening -->
      <div class="bg-gray-100 rounded-3xl p-4 space-y-4">
        <h2 class="text-xl font-bold text-gray-900">What's happening?!</h2>
        
        <div class="bg-white rounded-2xl p-4 hover:bg-gray-50 cursor-pointer transition-all">
          <p class="text-xs text-gray-500">Trending Worldwide</p>
          <p class="font-bold text-gray-900">#TSSANYWHERE</p>
          <p class="text-xs text-gray-500">{{ messages.length }} posts</p>
        </div>

        <div class="bg-white rounded-2xl p-4 hover:bg-gray-50 cursor-pointer transition-all">
          <p class="text-xs text-gray-500">Education Trending</p>
          <p class="font-bold text-gray-900">Online Learning</p>
          <p class="text-xs text-gray-500">{{ totalStudents }} students</p>
        </div>

        <div class="bg-white rounded-2xl p-4 hover:bg-gray-50 cursor-pointer transition-all">
          <p class="text-xs text-gray-500">Rwanda Trending</p>
          <p class="font-bold text-gray-900">Education Tech</p>
          <p class="text-xs text-gray-500">{{ groups.length }} classes</p>
        </div>
      </div>
    </div>

    <!-- Hidden file input -->
    <input ref="fileInput" type="file" class="hidden" @change="handleFileSelect" accept="image/*,video/*" />

    <!-- Image Modal -->
    <div v-if="imageModal.show" class="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4" @click="closeImageModal">
      <div class="relative max-w-2xl w-full" @click.stop>
        <button @click="closeImageModal" class="absolute -top-10 right-0 text-white hover:bg-white/20 p-2 rounded-full">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
          </svg>
        </button>
        <img :src="imageModal.url" class="w-full h-auto rounded-2xl" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../utils/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const groupId = ref(parseInt(route.params.groupId))
const group = ref(null)
const channels = ref([])
const activeChannelId = ref(null)
const activeChannel = ref(null)
const messages = ref([])
const reactions = ref({})
const newMessage = ref('')
const sending = ref(false)
const replyingTo = ref(null)
const loadingMessages = ref(false)
const messagesContainer = ref(null)
const showEmojiPicker = ref(false)
const activeReactionPicker = ref(null)
const quickReactions = ['👍', '❤️', '😂', '😮', '😢', '🙏', '🎉', '🔥']
const selectedFile = ref(null)
const fileInput = ref(null)
const showSettings = ref(false)
const imageModal = ref({ show: false, url: '' })

let messagePolling = null
let reactionPolling = null

const onlineCount = computed(() => Math.floor(Math.random() * 5) + 3)
const totalStudents = computed(() => group.value?.member_count || 0)
const groups = computed(() => channels.value.length)

async function loadGroup() {
  const res = await api.get(`/directory/groups/${groupId.value}`)
  group.value = res.data
}

async function loadChannels() {
  const res = await api.get(`/directory/groups/${groupId.value}/channels`)
  channels.value = res.data
  if (channels.value.length > 0 && !activeChannelId.value) {
    const accessibleChannel = channels.value.find(c => c.can_access)
    if (accessibleChannel) selectChannel(accessibleChannel)
  }
}

async function selectChannel(channel) {
  activeChannelId.value = channel.id
  activeChannel.value = channel
  loadingMessages.value = true
  
  if (messagePolling) clearInterval(messagePolling)
  if (reactionPolling) clearInterval(reactionPolling)
  
  messages.value = []
  
  await loadMessages()
  await loadReactions()
  
  messagePolling = setInterval(loadMessages, 1000)
  reactionPolling = setInterval(loadReactions, 2000)
  
  loadingMessages.value = false
}

async function loadMessages() {
  if (!activeChannelId.value) return
  try {
    const res = await api.get(`/simple-chat/channels/${activeChannelId.value}/messages`)
    const newMsgs = res.data.messages || res.data || []
    const wasAtBottom = isScrolledToBottom()
    messages.value = newMsgs
    if (wasAtBottom) {
      await nextTick()
      scrollToBottom()
    }
  } catch (err) {
    console.error('Load messages failed:', err)
  }
}

async function loadReactions() {
  if (!activeChannelId.value) return
  try {
    const res = await api.get(`/reactions/channel/${activeChannelId.value}`)
    reactions.value = res.data
  } catch (err) {
    console.error('Load reactions failed:', err)
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || sending.value) return
  
  sending.value = true
  const content = newMessage.value.trim()
  newMessage.value = ''
  
  try {
    const formData = new FormData()
    formData.append('content', content)
    if (replyingTo.value) formData.append('reply_to_id', replyingTo.value.id)
    if (selectedFile.value) formData.append('file', selectedFile.value)
    
    await api.post(`/simple-chat/channels/${activeChannelId.value}/messages`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    replyingTo.value = null
    selectedFile.value = null
    await loadMessages()
    scrollToBottom()
  } catch (err) {
    console.error('Send failed:', err)
    newMessage.value = content
  } finally {
    sending.value = false
  }
}

function selectFileType(type) {
  if (fileInput.value) {
    fileInput.value.accept = type === 'image' ? 'image/*' : 'video/*'
    fileInput.value.click()
  }
}

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (file && file.size <= 50 * 1024 * 1024) {
    selectedFile.value = file
  }
  event.target.value = ''
}

function getFullFileUrl(fileUrl) {
  if (!fileUrl) return ''
  if (fileUrl.startsWith('http')) return fileUrl
  return `http://localhost:8080${fileUrl}`
}

function openImageModal(url, fileName = '', fileSize = 0) {
  imageModal.value = { show: true, url, fileName, fileSize }
}

function closeImageModal() {
  imageModal.value.show = false
}

async function toggleReaction(messageId, emoji) {
  try {
    await api.post('/reactions/', { message_id: messageId, emoji })
    await loadReactions()
  } catch (err) {
    console.error('Reaction failed:', err)
  }
}

function getMessageReactions(messageId) {
  const msgReactions = reactions.value[messageId] || {}
  const result = {}
  if (msgReactions.likes > 0) result['👍'] = msgReactions.likes
  if (msgReactions.loves > 0) result['❤️'] = msgReactions.loves
  if (msgReactions.all_reactions) {
    Object.entries(msgReactions.all_reactions).forEach(([emoji, count]) => {
      if (count > 0) result[emoji] = count
    })
  }
  return result
}

function hasUserReaction(messageId, emoji) {
  return reactions.value[messageId]?.user_reactions?.includes(emoji) || false
}

function toggleReactionPicker(messageId) {
  activeReactionPicker.value = activeReactionPicker.value === messageId ? null : messageId
}

async function addQuickReaction(messageId, emoji) {
  await toggleReaction(messageId, emoji)
  activeReactionPicker.value = null
}

function replyTo(msg) {
  replyingTo.value = msg
}

function shareMessage(msg) {
  const text = `"${msg.content}" - ${msg.sender_name}`
  if (navigator.share) {
    navigator.share({ text })
  } else {
    navigator.clipboard.writeText(text)
  }
}

function isScrolledToBottom() {
  if (!messagesContainer.value) return true
  const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
  return scrollHeight - scrollTop - clientHeight < 100
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return 'now'
  if (diffMins < 60) return `${diffMins}m`
  if (diffHours < 24) return `${diffHours}h`
  if (diffDays < 7) return `${diffDays}d`
  return date.toLocaleDateString()
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  await loadGroup()
  await loadChannels()
})

onUnmounted(() => {
  if (messagePolling) clearInterval(messagePolling)
  if (reactionPolling) clearInterval(reactionPolling)
})
</script>

<style scoped>
textarea {
  font-family: inherit;
}

textarea::placeholder {
  color: #9ca3af;
}
</style>
