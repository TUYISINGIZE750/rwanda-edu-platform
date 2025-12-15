<template>
  <div class="fixed inset-0 bg-gray-100 flex flex-col overflow-hidden">
    <!-- Mobile Header -->
    <header class="bg-white shadow-sm border-b flex-shrink-0 lg:hidden">
      <div class="flex items-center justify-between h-16 px-4">
        <div class="flex items-center space-x-3">
          <button @click="$router.push('/home')" class="text-gray-600 hover:text-gray-900">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div>
            <h1 class="text-lg font-semibold text-gray-900">{{ group?.name || 'Loading...' }}</h1>
            <p class="text-sm text-gray-600">{{ onlineCount }} online</p>
          </div>
        </div>
        <button @click="showChannelList = !showChannelList" class="lg:hidden">
          <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </header>

    <div class="flex-1 flex overflow-hidden">
      <!-- Sidebar - Channel List -->
      <div class="w-80 bg-gray-900 text-white flex-shrink-0 hidden lg:flex flex-col"
           :class="{ 'fixed inset-y-0 left-0 z-50 lg:relative': showChannelList }">
        <!-- Server Header -->
        <div class="p-4 border-b border-gray-700">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-lg font-semibold">{{ group?.name || 'Loading...' }}</h2>
              <p class="text-sm text-gray-400">{{ group?.member_count || 0 }} members</p>
            </div>
            <button @click="showChannelList = false" class="lg:hidden text-gray-400 hover:text-white">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Channels -->
        <div class="flex-1 overflow-y-auto">
          <div class="p-2">
            <!-- Text Channels -->
            <div class="mb-4">
              <div class="flex items-center justify-between px-2 py-1 text-xs font-semibold text-gray-400 uppercase tracking-wide">
                <span>Text Channels</span>
                <button v-if="canCreateChannels" @click="createChannel" class="hover:text-white">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </button>
              </div>
              
              <div v-if="loading" class="px-2 py-1 text-sm text-gray-400">
                Loading channels...
              </div>
              
              <div v-else-if="textChannels.length === 0" class="px-2 py-1 text-sm text-gray-400">
                No channels yet
              </div>
              
              <div v-else class="space-y-1">
                <button v-for="channel in textChannels" :key="channel.id"
                        @click="selectChannel(channel)"
                        class="w-full flex items-center justify-between px-2 py-1 rounded hover:bg-gray-700 transition-colors"
                        :class="{ 'bg-gray-700': activeChannelId === channel.id }">
                  <div class="flex items-center space-x-2">
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                    </svg>
                    <span class="text-sm">{{ channel.name }}</span>
                  </div>
                </button>
              </div>
            </div>

            <!-- Voice Channels -->
            <div class="mb-4">
              <div class="flex items-center justify-between px-2 py-1 text-xs font-semibold text-gray-400 uppercase tracking-wide">
                <span>Voice Channels</span>
                <button v-if="canCreateChannels" @click="createVoiceChannel" class="hover:text-white" title="Create Voice Channel">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </button>
              </div>
              
              <div v-if="voiceChannels.length === 0" class="px-2 py-1 text-sm text-gray-400">
                No voice channels
                <div v-if="canCreateChannels" class="text-xs mt-1 text-gray-500">
                  Teachers can create voice channels for office hours
                </div>
              </div>
              
              <div v-else class="space-y-1">
                <button v-for="channel in voiceChannels" :key="channel.id"
                        @click="joinVoiceChannel(channel)"
                        class="w-full flex items-center justify-between px-2 py-1 rounded hover:bg-gray-700 transition-colors"
                        :class="authStore.user?.role !== 'teacher' ? 'opacity-60' : ''">
                  <div class="flex items-center space-x-2">
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                    </svg>
                    <span class="text-sm">{{ channel.name }}</span>
                    <span v-if="authStore.user?.role !== 'teacher'" class="text-xs text-yellow-400">(Teacher Only)</span>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- User Panel -->
        <div class="p-3 bg-gray-800 border-t border-gray-700">
          <div class="flex items-center space-x-3">
            <div class="relative">
              <img :src="userAvatar" :alt="authStore.user?.full_name" class="w-8 h-8 rounded-full" />
              <div class="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 border-2 border-gray-800 rounded-full"></div>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium truncate">{{ authStore.user?.full_name }}</p>
              <p class="text-xs text-gray-400">{{ authStore.user?.role }}</p>
            </div>
            <div class="flex space-x-1">
              <button @click="toggleMicrophone" 
                      :class="microphoneEnabled ? 'bg-green-600 text-white' : 'bg-red-600 text-white'"
                      class="p-1 hover:opacity-80 rounded transition-all" 
                      :title="microphoneEnabled ? 'Mute Microphone' : 'Unmute Microphone'">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path v-if="microphoneEnabled" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 5.586A2 2 0 015 7v3a3 3 0 005.395 2.605m2.829-2.829A3 3 0 0015 7V5a3 3 0 00-6 0v1M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4M3 3l18 18" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Chat Area -->
      <div class="flex-1 flex flex-col bg-gradient-to-b from-gray-50 to-gray-100 min-h-0">
        <div v-if="!activeChannelId" class="flex-1 flex items-center justify-center">
          <div class="text-center">
            <svg class="w-20 h-20 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Welcome to {{ group?.name }}</h3>
            <p class="text-gray-600">Select a channel to start chatting</p>
          </div>
        </div>

        <div v-else class="flex-1 flex flex-col">
          <!-- Channel Header -->
          <div class="bg-white border-b px-6 py-4 flex items-center justify-between shadow-sm">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                </svg>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 text-lg"># {{ activeChannel?.name }}</h3>
                <p class="text-sm text-gray-500">{{ messages.length }} messages</p>
              </div>
            </div>
            
            <div class="flex items-center gap-3">
              <span class="text-sm text-gray-500">{{ onlineCount }} online</span>
              <ThemeSwitcher />
            </div>
          </div>

          <!-- Messages Area -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-3" style="max-height: calc(100vh - 240px);">
            <div v-if="loadingMessages" class="flex justify-center py-12">
              <div class="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full"></div>
            </div>
            
            <div v-else-if="messages.length === 0" class="flex flex-col items-center justify-center py-16">
              <svg class="w-20 h-20 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">No messages yet</h3>
              <p class="text-gray-600 text-center">Be the first to send a message in # {{ activeChannel?.name }}</p>
            </div>
            
            <div v-else>
              <div v-for="msg in messages" :key="msg.id" 
                   class="flex items-end gap-2" 
                   :class="msg.sender_id === authStore.user?.id ? 'justify-end' : 'justify-start'">
                <!-- Avatar for others -->
                <div v-if="msg.sender_id !== authStore.user?.id" 
                     class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-semibold text-sm flex-shrink-0">
                  {{ msg.sender_name?.charAt(0).toUpperCase() || 'U' }}
                </div>
                
                <div class="max-w-md">
                  <div v-if="msg.sender_id !== authStore.user?.id" class="flex items-center gap-2 mb-1 ml-1">
                    <span class="text-sm font-semibold text-gray-800">{{ msg.sender_name || 'Unknown' }}</span>
                    <span class="text-xs px-2 py-0.5 rounded-full" 
                          :class="msg.sender_role === 'teacher' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'">
                      {{ msg.sender_role || 'student' }}
                    </span>
                  </div>
                  <div class="rounded-2xl px-4 py-2.5 shadow-sm max-w-md" 
                       :class="msg.sender_id === authStore.user?.id ? 'bg-blue-500 text-white rounded-br-sm' : 'bg-white text-gray-900 rounded-bl-sm'">
                    
                    <!-- Text Content -->
                    <p v-if="msg.content" class="text-sm leading-relaxed whitespace-pre-wrap break-words">{{ msg.content }}</p>
                    
                    <div class="flex items-center justify-end gap-1 mt-1">
                      <p class="text-xs" :class="msg.sender_id === authStore.user?.id ? 'text-blue-100' : 'text-gray-500'">
                        {{ formatTime(msg.created_at || msg.timestamp) }}
                      </p>
                    </div>
                  </div>
                </div>
                
                <!-- Avatar for own messages -->
                <div v-if="msg.sender_id === authStore.user?.id" 
                     class="w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white font-semibold text-sm flex-shrink-0">
                  {{ authStore.user?.full_name?.charAt(0).toUpperCase() || 'M' }}
                </div>
              </div>
            </div>
          </div>
          
          <!-- Chat Input -->
          <div class="bg-white border-t p-3 flex-shrink-0">
            <div class="flex items-center gap-2">
              <!-- Message Input -->
              <div class="flex-1 relative">
                <input 
                  v-model="newMessage"
                  @keyup.enter="sendMessageDirect"
                  type="text"
                  placeholder="Type a message..."
                  class="w-full px-4 py-2.5 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  :disabled="sending"
                />
              </div>
              
              <!-- Send Button -->
              <button 
                @click="sendMessageDirect"
                :disabled="!newMessage.trim() || sending"
                class="p-2.5 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Live Audio Space Interface -->
    <div v-if="showLiveSpace" class="fixed inset-0 bg-black bg-opacity-95 z-[140] flex items-center justify-center p-4">
      <div class="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 rounded-3xl w-full max-w-4xl h-full max-h-[90vh] overflow-hidden shadow-2xl">
        <!-- Space Header -->
        <div class="p-6 border-b border-white/20">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="w-4 h-4 bg-red-500 rounded-full animate-pulse"></div>
              <span class="text-white font-bold text-lg">🎤 LIVE</span>
              <span class="text-white/70 text-sm">{{ totalParticipants }} participants</span>
            </div>
            <button @click="leaveLiveSpace" class="text-white/70 hover:text-white p-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <h2 class="text-white text-2xl font-bold mb-2">{{ currentLiveSpace?.name }}</h2>
          <p class="text-white/80 text-sm">Hosted by {{ currentLiveSpace?.host }} • {{ currentLiveSpace?.hostRole }}</p>
          <p class="text-white/60 text-sm mt-1">{{ currentLiveSpace?.topic }}</p>
        </div>
        
        <!-- Speakers Section -->
        <div class="p-6 border-b border-white/20">
          <h3 class="text-white font-semibold mb-4 flex items-center gap-2">
            🎤 Speaking Now
          </h3>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div v-for="participant in liveSpaceParticipants.filter(p => p.isSpeaking)" :key="participant.id" 
                 class="bg-white/10 rounded-2xl p-4 text-center">
              <div class="w-16 h-16 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-xl mx-auto mb-2">
                {{ participant.name?.charAt(0).toUpperCase() }}
              </div>
              <p class="text-white font-medium text-sm">{{ participant.name }}</p>
              <p class="text-white/60 text-xs">{{ participant.role }}</p>
              <div v-if="participant.isHost" class="mt-2">
                <span class="bg-yellow-500 text-black px-2 py-1 rounded-full text-xs font-bold">HOST</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Listeners Section -->
        <div class="p-6 flex-1 overflow-y-auto">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-white font-semibold flex items-center gap-2">
              👥 Listeners ({{ listenersCount }})
            </h3>
            <div v-if="speakingQueue.length > 0" class="text-white/70 text-sm bg-yellow-500/20 px-3 py-1 rounded-full">
              🙋♂️ {{ speakingQueue.length }} waiting to speak
            </div>
          </div>
          
          <!-- Test Buttons for Teacher -->
          <div v-if="isHost" class="mb-4 flex gap-2">
            <button @click="addTestSpeakingRequest" class="bg-yellow-500 hover:bg-yellow-600 text-black px-4 py-2 rounded-lg font-medium text-sm">
              🧪 Add Test Request
            </button>
            <button @click="addTestListener" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium text-sm">
              👥 Add Test Listener
            </button>
          </div>
          
          <!-- Speaking Queue (Host View) -->
          <div v-if="isHost && speakingQueue.length > 0" class="mb-6">
            <h4 class="text-white/80 font-medium mb-3">🙋♂️ Speaking Requests</h4>
            <div class="space-y-2">
              <div v-for="request in speakingQueue" :key="request.id" 
                   class="bg-yellow-500/20 border border-yellow-500/30 rounded-lg p-3 flex items-center justify-between">
                <div>
                  <p class="text-white font-medium">{{ request.name }}</p>
                  <p class="text-white/60 text-sm">{{ request.role }}</p>
                </div>
                <div class="flex gap-2">
                  <button @click="approveToSpeak(request.id)" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded-full text-sm">
                    Approve
                  </button>
                  <button @click="declineRequest(request.id)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-full text-sm">
                    Decline
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Listeners Grid -->
          <div class="grid grid-cols-4 md:grid-cols-6 gap-3">
            <div v-for="participant in liveSpaceParticipants.filter(p => !p.isSpeaking)" :key="participant.id" 
                 class="text-center">
              <div class="w-12 h-12 bg-gradient-to-br from-gray-400 to-gray-600 rounded-full flex items-center justify-center text-white font-bold text-sm mx-auto mb-1">
                {{ participant.name?.charAt(0).toUpperCase() }}
              </div>
              <p class="text-white/80 text-xs truncate">{{ participant.name }}</p>
            </div>
          </div>
        </div>
        
        <!-- Controls -->
        <div class="p-6 border-t border-white/20">
          <div class="flex items-center justify-center gap-4">
            <button v-if="!isSpeaking && !isHost && !speakingQueue.find(p => p.id === authStore.user?.id)" @click="requestToSpeak" 
                    class="bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white px-6 py-3 rounded-full font-medium flex items-center gap-2">
              🙋♂️ Request to Speak
            </button>
            
            <div v-if="speakingQueue.find(p => p.id === authStore.user?.id)" class="bg-yellow-500/20 border border-yellow-500 text-yellow-200 px-6 py-3 rounded-full font-medium">
              ⏳ Request Pending - Waiting for teacher approval
            </div>
            
            <button @click="toggleMicrophone" 
                    :class="microphoneEnabled ? 'bg-green-500 hover:bg-green-600' : 'bg-red-500 hover:bg-red-600'"
                    class="text-white p-3 rounded-full">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="microphoneEnabled" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 5.586A2 2 0 015 7v3a3 3 0 005.395 2.605m2.829-2.829A3 3 0 0015 7V5a3 3 0 00-6 0v1M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4M3 3l18 18" />
              </svg>
            </button>
            
            <button v-if="isHost" @click="endLiveSpace" 
                    class="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-full font-medium">
              End Space
            </button>
            
            <button v-else @click="leaveLiveSpace" 
                    class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-full font-medium">
              Leave Space
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import ThemeSwitcher from '../components/ThemeSwitcher.vue'
import api from '../utils/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

const groupId = ref(parseInt(route.params.groupId))
const group = ref(null)
const channels = ref([])
const activeChannelId = ref(null)
const activeChannel = ref(null)
const loading = ref(true)
const loadingMessages = ref(false)
const showChannelList = ref(false)
const messagesContainer = ref(null)
const messagePollingInterval = ref(null)
const newMessage = ref('')
const sending = ref(false)
const microphoneEnabled = ref(true)
const showLiveSpace = ref(false)
const currentLiveSpace = ref(null)
const liveSpaceParticipants = ref([])
const speakingQueue = ref([])

// Computed properties for counts
const totalParticipants = computed(() => liveSpaceParticipants.value.length + speakingQueue.value.length)
const listenersCount = computed(() => liveSpaceParticipants.value.filter(p => !p.isSpeaking).length)
const isHost = ref(false)
const isSpeaking = ref(false)

// Computed properties
const textChannels = computed(() => channels.value.filter(c => 
  ['ANNOUNCEMENTS', 'DISCUSSION', 'RESOURCES', 'text'].includes(c.type)
))
const voiceChannels = computed(() => channels.value.filter(c => 
  ['OFFICE_HOURS', 'voice'].includes(c.type)
))
const messages = ref([])
const onlineUsers = ref([])
const onlineCount = computed(() => onlineUsers.value.length)
const canCreateChannels = computed(() => authStore.user?.role?.toLowerCase() === 'teacher')
const userAvatar = computed(() => 
  authStore.user?.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(authStore.user?.full_name || 'User')}&background=random`
)

onMounted(async () => {
  console.log('HubsView mounted, groupId:', groupId.value)
  
  if (!authStore.isAuthenticated) {
    console.log('Not authenticated, redirecting to login')
    router.push('/login')
    return
  }
  
  console.log('User authenticated:', authStore.user)
  
  await loadGroupData()
  await loadChannels()
  await loadOnlineUsers()
  
  console.log('Channels loaded, count:', channels.value.length)
  
  // Auto-select first channel if available
  if (channels.value.length > 0) {
    console.log('Auto-selecting first channel:', channels.value[0])
    selectChannel(channels.value[0])
  } else {
    console.warn('No channels available to select')
  }
})

onUnmounted(() => {
  if (messagePollingInterval.value) {
    clearInterval(messagePollingInterval.value)
  }
  chatStore.reset()
})

async function loadGroupData() {
  try {
    console.log('Loading group data for ID:', groupId.value)
    const response = await api.get(`/directory/groups/${groupId.value}`)
    console.log('Group data loaded:', response.data)
    group.value = response.data
    
    // If no member_count, set a default based on group type
    if (!group.value.member_count) {
      group.value.member_count = group.value.type === 'CLASS' ? 45 : 12
    }
  } catch (err) {
    console.error('Failed to load group:', err)
    alert('Failed to load group: ' + (err.response?.data?.detail || err.message))
    router.push('/student-dashboard')
  }
}

async function loadChannels() {
  try {
    console.log('Loading channels for group:', groupId.value)
    const response = await api.get(`/directory/groups/${groupId.value}/channels`)
    console.log('Channels loaded:', response.data)
    channels.value = response.data || []
    
    // Add default voice channels if none exist
    if (channels.value.filter(c => c.type === 'OFFICE_HOURS').length === 0) {
      channels.value.push(
        {
          id: 9001,
          name: 'Office Hours',
          type: 'OFFICE_HOURS',
          connected_users: 0,
          group_id: groupId.value
        },
        {
          id: 9002,
          name: 'Study Group',
          type: 'OFFICE_HOURS',
          connected_users: 0,
          group_id: groupId.value
        }
      )
    }
    
    if (channels.value.length === 0) {
      console.warn('No channels found for this group')
    }
  } catch (err) {
    console.error('Failed to load channels:', err)
    alert('Failed to load channels: ' + (err.response?.data?.detail || err.message))
    channels.value = []
  } finally {
    loading.value = false
  }
}

async function selectChannel(channel) {
  console.log('=== SELECT CHANNEL ====')
  console.log('Channel:', channel)
  
  if (activeChannelId.value === channel.id) {
    console.log('Channel already selected')
    return
  }
  
  try {
    // Clear previous polling
    if (messagePollingInterval.value) {
      clearInterval(messagePollingInterval.value)
    }
    
    activeChannelId.value = channel.id
    activeChannel.value = channel
    loadingMessages.value = true
    showChannelList.value = false
    
    // Clear previous messages
    messages.value = []
    
    // Load messages from API
    const url = `/simple-chat/channels/${channel.id}/messages`
    console.log('Fetching from:', url)
    
    const response = await api.get(url)
    console.log('API Response:', response.data)
    
    messages.value = response.data.messages || []
    console.log('Messages loaded:', messages.value.length)
    
    // Scroll to bottom
    await nextTick()
    scrollToBottom()
    
    // Start polling messages with error handling
    messagePollingInterval.value = setInterval(async () => {
      try {
        await refreshMessages()
      } catch (error) {
        console.error('Polling error:', error)
      }
    }, 3000)
    
    console.log('Channel selected successfully')
  } catch (error) {
    console.error('ERROR selecting channel:', error)
    alert('Failed to load channel: ' + (error.response?.data?.detail || error.message))
  } finally {
    loadingMessages.value = false
  }
}

async function refreshMessages() {
  if (!activeChannelId.value) return
  
  try {
    const response = await api.get(`/simple-chat/channels/${activeChannelId.value}/messages`)
    const newMessages = response.data.messages || []
    const currentCount = messages.value.length
    
    // Safely process messages
    if (Array.isArray(newMessages)) {
      messages.value = newMessages
      
      if (newMessages.length > currentCount) {
        await nextTick()
        scrollToBottom()
      }
    }
  } catch (error) {
    console.error('Failed to refresh messages:', error)
  }
}

async function sendMessageDirect() {
  console.log('=== SEND MESSAGE ===')
  console.log('Message:', newMessage.value)
  console.log('Channel ID:', activeChannelId.value)
  
  if (!newMessage.value.trim()) {
    console.log('Empty message')
    return
  }
  if (sending.value) {
    console.log('Already sending')
    return
  }
  if (!activeChannelId.value) {
    console.log('No active channel')
    alert('Please select a channel first')
    return
  }
  
  sending.value = true
  const content = newMessage.value.trim()
  newMessage.value = ''
  
  try {
    const url = `/simple-chat/channels/${activeChannelId.value}/messages`
    console.log('Posting to:', url)
    
    const payload = { 
      content: content
    }
    
    const response = await api.post(url, payload)
    console.log('Send response:', response.data)
    
    if (response.data.needs_approval) {
      alert('✅ Message sent! Waiting for teacher approval.')
    } else {
      console.log('Message sent successfully')
    }
    
    await refreshMessages()
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('ERROR sending message:', error)
    alert('❌ Failed to send: ' + (error.response?.data?.detail || error.message))
    newMessage.value = content
  } finally {
    sending.value = false
  }
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function createChannel() {
  router.push(`/create-channel?group=${groupId.value}`)
}

function joinVoiceChannel(channel) {
  console.log('Joining voice channel:', channel)
  console.log('User role:', authStore.user?.role)
  
  // Only teachers can start live spaces
  if (authStore.user?.role !== 'teacher') {
    alert('🚫 Only teachers can start live spaces. Please wait for a teacher to start one.')
    return
  }
  
  try {
    startLiveSpace(channel)
  } catch (error) {
    console.error('Error starting live space:', error)
    alert('❌ Failed to start live space: ' + error.message)
  }
}

function startLiveSpace(channel) {
  console.log('Starting live space for channel:', channel)
  
  try {
    currentLiveSpace.value = {
      id: channel.id,
      name: channel.name,
      host: authStore.user?.full_name || 'Unknown Host',
      hostRole: authStore.user?.role || 'teacher',
      startTime: new Date().toISOString(),
      topic: `Live discussion in ${channel.name}`
    }
    
    isHost.value = true
    isSpeaking.value = true
    showLiveSpace.value = true
    
    // Add host as first participant
    liveSpaceParticipants.value = [{
      id: authStore.user?.id || 'host-1',
      name: authStore.user?.full_name || 'Host',
      role: authStore.user?.role || 'teacher',
      isSpeaking: true,
      isHost: true
    }]
    
    // Initialize empty queue
    speakingQueue.value = []
    
    console.log('Live space created successfully')
  } catch (error) {
    console.error('Error in startLiveSpace:', error)
    throw error
  }
}

function formatTime(timestamp) {
  if (!timestamp) return 'Just now'
  const date = new Date(timestamp)
  if (isNaN(date.getTime())) return 'Just now'
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
}

async function loadOnlineUsers() {
  try {
    // Simulate dynamic online users
    const baseUsers = [
      { id: 1, name: 'HAKIZIMANA Elam', role: 'Teacher', status: 'online' },
      { id: 2, name: 'KUBWAMAHINA Joshua', role: 'Student', status: 'online' },
      { id: 5, name: 'UWIMANA Alice', role: 'Student', status: 'online' },
      { id: 8, name: 'NIYONZIMA Paul', role: 'Student', status: 'online' },
      { id: 12, name: 'MUKAMANA Grace', role: 'Student', status: 'online' },
      { id: 15, name: 'NSENGIMANA Eric', role: 'Student', status: 'online' }
    ]
    
    // Randomly show 3-6 users online
    const count = Math.floor(Math.random() * 4) + 3
    onlineUsers.value = baseUsers.slice(0, count)
  } catch (err) {
    console.error('Failed to load online users:', err)
  }
}

function createVoiceChannel() {
  alert('Voice channel creation coming soon!')
}

function toggleMicrophone() {
  microphoneEnabled.value = !microphoneEnabled.value
  const status = microphoneEnabled.value ? 'unmuted' : 'muted'
  console.log(`Microphone ${status}`)
}

function requestToSpeak() {
  try {
    const userId = authStore.user?.id || 'user-' + Date.now()
    
    if (speakingQueue.value.find(p => p.id === userId)) {
      alert('You are already in the speaking queue')
      return
    }
    
    speakingQueue.value.push({
      id: userId,
      name: authStore.user?.full_name || 'User',
      role: authStore.user?.role || 'student',
      requestTime: new Date().toISOString()
    })
    
    alert('🙋♂️ Request sent! Waiting for host approval.')
    console.log('Speaking request added for user:', userId)
  } catch (error) {
    console.error('Error requesting to speak:', error)
    alert('❌ Failed to request speaking permission')
  }
}

function approveToSpeak(participantId) {
  try {
    console.log('Approving speaker:', participantId)
    
    // Find in queue first
    const queuedParticipant = speakingQueue.value.find(p => p.id === participantId)
    if (!queuedParticipant) {
      console.warn('Participant not found in queue:', participantId)
      return
    }
    
    // Find or add to participants
    let participant = liveSpaceParticipants.value.find(p => p.id === participantId)
    if (!participant) {
      // Add to participants if not already there
      participant = {
        id: queuedParticipant.id,
        name: queuedParticipant.name,
        role: queuedParticipant.role,
        isSpeaking: true,
        isHost: false
      }
      liveSpaceParticipants.value.push(participant)
    } else {
      participant.isSpeaking = true
    }
    
    // Remove from queue
    speakingQueue.value = speakingQueue.value.filter(p => p.id !== participantId)
    
    console.log('Speaker approved successfully')
  } catch (error) {
    console.error('Error approving speaker:', error)
  }
}

function declineRequest(participantId) {
  speakingQueue.value = speakingQueue.value.filter(p => p.id !== participantId)
}

function leaveLiveSpace() {
  try {
    if (isHost.value) {
      if (confirm('As host, ending the space will remove all participants. Continue?')) {
        endLiveSpace()
      }
    } else {
      const userId = authStore.user?.id
      showLiveSpace.value = false
      
      // Remove user from participants
      if (userId) {
        liveSpaceParticipants.value = liveSpaceParticipants.value.filter(p => p.id !== userId)
        speakingQueue.value = speakingQueue.value.filter(p => p.id !== userId)
      }
      
      console.log('Left live space successfully')
    }
  } catch (error) {
    console.error('Error leaving live space:', error)
  }
}

function endLiveSpace() {
  try {
    console.log('Ending live space...')
    
    showLiveSpace.value = false
    currentLiveSpace.value = null
    liveSpaceParticipants.value = []
    speakingQueue.value = []
    isHost.value = false
    isSpeaking.value = false
    
    console.log('Live space ended successfully')
  } catch (error) {
    console.error('Error ending live space:', error)
  }
}

function addTestSpeakingRequest() {
  const testId = Date.now()
  speakingQueue.value.push({
    id: testId,
    name: 'KUBWAMAHINA Joshua',
    role: 'student',
    requestTime: new Date()
  })
}

function addTestListener() {
  const testId = Date.now() + Math.random()
  const names = ['UWASE Marie', 'MUGISHA Jean', 'NIYONZIMA Paul', 'MUKAMANA Grace']
  const randomName = names[Math.floor(Math.random() * names.length)]
  
  liveSpaceParticipants.value.push({
    id: testId,
    name: randomName,
    role: 'student',
    isSpeaking: false,
    isHost: false
  })
}

</script>

<style scoped>
/* Add any custom styles here */
</style>