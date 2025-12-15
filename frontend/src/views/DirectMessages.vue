<template>
  <div class="h-screen flex bg-gray-100">
    <!-- Sidebar - Conversations List -->
    <div class="w-80 bg-white border-r flex flex-col">
      <!-- Header -->
      <div class="p-4 border-b bg-gradient-to-r from-blue-500 to-blue-600">
        <div class="flex items-center justify-between mb-3">
          <h1 class="text-xl font-bold text-white">Messages</h1>
          <button @click="$router.back()" class="text-white hover:bg-white/20 p-2 rounded-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <button @click="showNewChat = true" class="w-full bg-white text-blue-600 py-2 rounded-lg font-medium hover:bg-blue-50">
          + New Chat
        </button>
      </div>

      <!-- Conversations -->
      <div class="flex-1 overflow-y-auto">
        <div v-if="loadingConversations" class="p-8 text-center">
          <div class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
        </div>
        
        <div v-else-if="conversations.length === 0" class="p-8 text-center text-gray-500">
          <p>No conversations yet</p>
          <p class="text-sm mt-2">Start a new chat!</p>
        </div>
        
        <div v-else>
          <button v-for="conv in conversations" :key="conv.user_id"
                  @click="selectConversation(conv)"
                  class="w-full p-4 border-b hover:bg-gray-50 text-left transition-colors"
                  :class="{ 'bg-blue-50': selectedUser?.user_id === conv.user_id }">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 rounded-full bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-white font-bold">
                {{ conv.user_name.charAt(0).toUpperCase() }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between">
                  <p class="font-semibold text-gray-900 truncate">{{ conv.user_name }}</p>
                  <span v-if="conv.unread_count > 0" class="bg-blue-500 text-white text-xs px-2 py-1 rounded-full">
                    {{ conv.unread_count }}
                  </span>
                </div>
                <p class="text-sm text-gray-500 truncate">{{ conv.last_message }}</p>
              </div>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Chat Area -->
    <div class="flex-1 flex flex-col">
      <div v-if="!selectedUser" class="flex-1 flex items-center justify-center text-gray-500">
        <div class="text-center">
          <svg class="w-20 h-20 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <p class="text-lg">Select a conversation to start chatting</p>
        </div>
      </div>

      <div v-else class="flex-1 flex flex-col">
        <!-- Chat Header -->
        <div class="bg-white border-b p-4 flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-white font-bold">
            {{ selectedUser.user_name.charAt(0).toUpperCase() }}
          </div>
          <div>
            <h2 class="font-semibold text-gray-900">{{ selectedUser.user_name }}</h2>
            <p class="text-sm text-gray-500">{{ selectedUser.user_role }}</p>
          </div>
        </div>

        <!-- Messages -->
        <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-3 bg-gradient-to-b from-gray-50 to-gray-100">
          <div v-if="loadingMessages" class="text-center py-12">
            <div class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
          </div>

          <div v-else-if="messages.length === 0" class="text-center py-12 text-gray-500">
            <p>No messages yet</p>
            <p class="text-sm mt-2">Send the first message!</p>
          </div>

          <div v-else>
            <div v-for="msg in messages" :key="msg.id" 
                 class="flex items-end gap-2" :class="msg.is_own ? 'justify-end' : 'justify-start'">
              <div v-if="!msg.is_own" class="w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-white font-semibold text-sm">
                {{ msg.sender_name.charAt(0).toUpperCase() }}
              </div>
              
              <div class="max-w-md">
                <div class="rounded-2xl px-4 py-2.5 shadow-sm" 
                     :class="msg.is_own ? 'bg-blue-500 text-white rounded-br-sm' : 'bg-white text-gray-900 rounded-bl-sm'">
                  <p class="text-sm leading-relaxed">{{ msg.content }}</p>
                  <p class="text-xs mt-1" :class="msg.is_own ? 'text-blue-100' : 'text-gray-500'">
                    {{ formatTime(msg.created_at) }}
                  </p>
                </div>
              </div>
              
              <div v-if="msg.is_own" class="w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white font-semibold text-sm">
                {{ msg.sender_name.charAt(0).toUpperCase() }}
              </div>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="bg-white border-t p-4">
          <div class="flex gap-3">
            <input 
              v-model="newMessage"
              @keyup.enter="sendMessage"
              type="text"
              placeholder="Type a message..."
              class="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              :disabled="sending"
            />
            <button 
              @click="sendMessage"
              :disabled="!newMessage.trim() || sending"
              class="px-6 py-3 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:opacity-50 font-medium">
              Send
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- New Chat Modal -->
    <div v-if="showNewChat" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="showNewChat = false">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 max-h-[80vh] flex flex-col">
        <div class="p-4 border-b flex items-center justify-between">
          <h3 class="text-lg font-semibold">New Chat</h3>
          <button @click="showNewChat = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-4 border-b">
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Search users..."
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div class="flex-1 overflow-y-auto p-4">
          <div v-if="loadingUsers" class="text-center py-8">
            <div class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
          </div>
          
          <div v-else-if="filteredUsers.length === 0" class="text-center py-8 text-gray-500">
            No users found
          </div>
          
          <div v-else class="space-y-2">
            <button v-for="user in filteredUsers" :key="user.id"
                    @click="startChat(user)"
                    class="w-full p-3 border rounded-lg hover:bg-gray-50 text-left flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-white font-bold">
                {{ user.full_name.charAt(0).toUpperCase() }}
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ user.full_name }}</p>
                <p class="text-sm text-gray-500">{{ user.role }}</p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'

const router = useRouter()

const conversations = ref([])
const selectedUser = ref(null)
const messages = ref([])
const newMessage = ref('')
const loadingConversations = ref(true)
const loadingMessages = ref(false)
const sending = ref(false)
const messagesContainer = ref(null)
const showNewChat = ref(false)
const users = ref([])
const loadingUsers = ref(false)
const searchQuery = ref('')
const refreshInterval = ref(null)

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(u => u.full_name.toLowerCase().includes(query))
})

onMounted(async () => {
  await loadConversations()
  await loadUsers()
  
  // Auto-refresh every 5 seconds
  refreshInterval.value = setInterval(() => {
    if (selectedUser.value) {
      loadMessages(selectedUser.value.user_id, false)
    }
  }, 5000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})

async function loadConversations() {
  try {
    const response = await api.get('/dm/conversations')
    conversations.value = response.data || []
  } catch (error) {
    console.error('Failed to load conversations:', error)
  } finally {
    loadingConversations.value = false
  }
}

async function loadUsers() {
  try {
    loadingUsers.value = true
    // Get users from same school
    const response = await api.get('/directory/groups')
    const groups = response.data || []
    
    // Extract unique users from groups
    const userSet = new Set()
    for (const group of groups) {
      const membersResponse = await api.get(`/directory/groups/${group.id}/members`)
      const members = membersResponse.data || []
      members.forEach(m => {
        if (!userSet.has(m.id)) {
          userSet.add(m.id)
          users.value.push(m)
        }
      })
    }
  } catch (error) {
    console.error('Failed to load users:', error)
  } finally {
    loadingUsers.value = false
  }
}

async function selectConversation(conv) {
  selectedUser.value = conv
  await loadMessages(conv.user_id)
}

async function loadMessages(userId, showLoading = true) {
  if (showLoading) loadingMessages.value = true
  try {
    const response = await api.get(`/dm/messages/${userId}`)
    messages.value = response.data || []
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to load messages:', error)
  } finally {
    if (showLoading) loadingMessages.value = false
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || sending.value || !selectedUser.value) return
  
  sending.value = true
  const content = newMessage.value.trim()
  newMessage.value = ''
  
  try {
    const response = await api.post('/dm/send', {
      receiver_id: selectedUser.value.user_id,
      content
    })
    
    if (response.data.status === 'pending') {
      alert('✅ Message sent! Waiting for teacher approval.')
    }
    
    await loadMessages(selectedUser.value.user_id, false)
  } catch (error) {
    console.error('Failed to send message:', error)
    alert('❌ Failed to send message')
    newMessage.value = content
  } finally {
    sending.value = false
  }
}

function startChat(user) {
  selectedUser.value = {
    user_id: user.id,
    user_name: user.full_name,
    user_role: user.role
  }
  messages.value = []
  showNewChat.value = false
  loadMessages(user.id)
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function formatTime(timestamp) {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
}
</script>
