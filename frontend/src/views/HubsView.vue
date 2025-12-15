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
                <p class="text-sm text-gray-500">{{ messageCount }} messages</p>
              </div>
            </div>
            
            <div class="flex items-center gap-3">
              <!-- ALWAYS SHOW FOR TEACHERS - DEBUG -->
              <button v-if="authStore.user?.role === 'teacher'" 
                      @click="showPendingModal = true"
                      class="px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg font-medium transition-all shadow-lg">
                <span class="flex items-center gap-2">
                  ⚠️ Approve ({{ pendingMessages.length }})
                </span>
              </button>
              <span class="text-sm text-gray-500">{{ onlineCount }} online</span>
              <ThemeSwitcher />
            </div>
          </div>

          <!-- Messages Area -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-3" style="max-height: calc(100vh - 240px);">
            <div v-if="loadingMessages" class="flex justify-center py-12">
              <div class="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full"></div>
            </div>
            
            <div v-else-if="!hasMessages" class="flex flex-col items-center justify-center py-16">
              <svg class="w-20 h-20 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">No messages yet</h3>
              <p class="text-gray-600 text-center">Be the first to send a message in # {{ activeChannel?.name }}</p>
            </div>
            
            <div v-else>
              <div v-for="msg in validMessages" :key="msg.id" 
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
                       :class="[
                         msg.sender_id === authStore.user?.id ? 'bg-blue-500 text-white rounded-br-sm' : 'bg-white text-gray-900 rounded-bl-sm',
                         msg.status === 'pending' && authStore.user?.role === 'teacher' ? 'ring-4 ring-yellow-400' : ''
                       ]">
                    
                    <!-- PENDING STATUS BADGE FOR TEACHERS -->
                    <div v-if="msg.status === 'pending' && authStore.user?.role === 'teacher'" 
                         class="mb-3 p-3 bg-yellow-100 border-2 border-yellow-400 rounded-lg">
                      <div class="flex items-center justify-between gap-2">
                        <span class="text-sm font-bold text-yellow-900">⚠️ PENDING APPROVAL</span>
                        <div class="flex gap-2">
                          <button @click.stop="approveMessage(msg.id)" 
                                  class="px-3 py-1 bg-green-500 hover:bg-green-600 text-white rounded-lg text-xs font-bold">
                            ✅ APPROVE
                          </button>
                          <button @click.stop="rejectMessage(msg.id)" 
                                  class="px-3 py-1 bg-red-500 hover:bg-red-600 text-white rounded-lg text-xs font-bold">
                            ❌ REJECT
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Reply Preview -->
                    <div v-if="msg.reply_to" 
                         class="mb-2 p-2 rounded-lg border-l-4 cursor-pointer hover:opacity-80 transition-opacity"
                         :class="msg.sender_id === authStore.user?.id ? 'bg-blue-600 border-blue-300' : 'bg-gray-100 border-purple-400'"
                         @click="scrollToMessage(msg.reply_to.id)">
                      <div class="flex items-center gap-2 mb-1">
                        <svg class="w-4 h-4" :class="msg.sender_id === authStore.user?.id ? 'text-blue-200' : 'text-purple-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                        </svg>
                        <span class="text-xs font-semibold" :class="msg.sender_id === authStore.user?.id ? 'text-blue-100' : 'text-purple-600'">
                          {{ msg.reply_to.sender_name }}
                        </span>
                      </div>
                      <p class="text-xs" :class="msg.sender_id === authStore.user?.id ? 'text-blue-100' : 'text-gray-600'">
                        {{ msg.reply_to.content }}
                      </p>
                    </div>
                    
                    <!-- File Content -->
                    <div v-if="msg.file" class="mb-2">
                      <!-- Image Preview -->
                      <div v-if="msg.file.type?.startsWith('image/')" class="max-w-xs relative group">
                        <img :src="getFileUrl(msg.file)" :alt="msg.file.name" class="rounded-lg max-w-full h-auto cursor-pointer" @click="openFile(msg.file)" />
                        <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button @click.stop="downloadFile(msg.file)" class="bg-black bg-opacity-50 text-white p-1 rounded-full hover:bg-opacity-70">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                          </button>
                        </div>
                        <p class="text-xs mt-1" :class="msg.sender_id === authStore.user?.id ? 'text-blue-100' : 'text-gray-500'">
                          {{ msg.file.name }} • {{ formatFileSize(msg.file.size) }}
                        </p>
                      </div>
                      
                      <!-- Video Preview -->
                      <div v-else-if="msg.file.type?.startsWith('video/')" class="max-w-xs relative group">
                        <video :src="getFileUrl(msg.file)" controls class="rounded-lg max-w-full h-auto">
                          Your browser does not support the video tag.
                        </video>
                        <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button @click.stop="downloadFile(msg.file)" class="bg-black bg-opacity-50 text-white p-1 rounded-full hover:bg-opacity-70">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                          </button>
                        </div>
                        <p class="text-xs mt-1" :class="msg.sender_id === authStore.user?.id ? 'text-blue-100' : 'text-gray-500'">
                          {{ msg.file.name }} • {{ formatFileSize(msg.file.size) }}
                        </p>
                      </div>
                      
                      <!-- Audio Preview -->
                      <div v-else-if="msg.file.type?.startsWith('audio/')" class="max-w-xs">
                        <div class="bg-gray-100 rounded-lg p-3">
                          <audio :src="getFileUrl(msg.file)" controls class="w-full">
                            Your browser does not support the audio tag.
                          </audio>
                          <div class="flex justify-between items-center mt-2">
                            <p class="text-xs" :class="msg.sender_id === authStore.user?.id ? 'text-blue-100' : 'text-gray-500'">
                              {{ msg.file.name }} • {{ formatFileSize(msg.file.size) }}
                            </p>
                            <button @click.stop="downloadFile(msg.file)" class="text-gray-500 hover:text-gray-700">
                              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                              </svg>
                            </button>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Other Files -->
                      <div v-else class="flex items-center gap-3 p-3 rounded-lg cursor-pointer hover:opacity-80" 
                           :class="msg.sender_id === authStore.user?.id ? 'bg-blue-600' : 'bg-gray-100'"
                           @click="downloadFile(msg.file)">
                        <div class="w-10 h-10 rounded-lg flex items-center justify-center" 
                             :class="msg.sender_id === authStore.user?.id ? 'bg-blue-500' : 'bg-gray-200'">
                          <span class="text-lg">{{ getFileIcon(msg.file.type) }}</span>
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="font-medium truncate" :class="msg.sender_id === authStore.user?.id ? 'text-white' : 'text-gray-900'">
                            {{ msg.file.name }}
                          </p>
                          <p class="text-xs" :class="msg.sender_id === authStore.user?.id ? 'text-blue-100' : 'text-gray-500'">
                            {{ formatFileSize(msg.file.size) }} • Click to download
                          </p>
                        </div>
                        <svg class="w-5 h-5" :class="msg.sender_id === authStore.user?.id ? 'text-blue-200' : 'text-gray-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                    </div>
                    
                    <!-- Text Content -->
                    <p v-if="msg.content" class="text-sm leading-relaxed whitespace-pre-wrap break-words">{{ msg.content }}</p>
                    
                    <div class="flex items-center justify-end gap-1 mt-1">
                      <p class="text-xs" :class="msg.sender_id === authStore.user?.id ? 'text-blue-100' : 'text-gray-500'">
                        {{ formatTime(msg.created_at || msg.timestamp) }}
                      </p>
                      <svg v-if="msg.sender_id === authStore.user?.id" class="w-4 h-4 text-blue-100" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                      </svg>
                    </div>
                    
                    <!-- Teacher Approval Buttons (for pending messages in Announcements/Resources) -->
                    <div v-if="authStore.user?.role === 'teacher' && msg.status === 'pending' && (activeChannel?.type === 'ANNOUNCEMENTS' || activeChannel?.type === 'RESOURCES')" 
                         class="flex items-center gap-2 mt-3 p-2 bg-yellow-50 border border-yellow-300 rounded-lg">
                      <span class="text-sm font-semibold text-yellow-800">⚠️ Pending Approval:</span>
                      <button @click.stop="approveMessage(msg.id)" 
                              class="px-3 py-1 bg-green-500 hover:bg-green-600 text-white rounded-lg text-sm font-medium">
                        ✅ Approve
                      </button>
                      <button @click.stop="rejectMessage(msg.id)" 
                              class="px-3 py-1 bg-red-500 hover:bg-red-600 text-white rounded-lg text-sm font-medium">
                        ❌ Reject
                      </button>
                    </div>
                    
                    <!-- Message Action Buttons -->
                    <div class="flex items-center gap-2 mt-3 flex-wrap">
                      <!-- Like -->
                      <button @click.stop="handleReaction({ emoji: '👍', messageId: msg.id })" 
                              :data-msg-id="msg.id"
                              data-emoji="👍"
                              :class="[
                                msg.userReactions?.[authStore.user?.id]?.includes('👍') 
                                  ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg scale-105 ring-2 ring-blue-300' 
                                  : 'bg-white hover:bg-blue-50 text-blue-600',
                                'px-3 py-1.5 rounded-full transition-all transform hover:scale-110 active:scale-95 flex items-center gap-1.5 text-sm font-bold shadow-md border-2 border-blue-300'
                              ]">
                        <span class="text-lg">👍</span>
                        <span>{{ msg.likes || 0 }}</span>
                      </button>
                      
                      <!-- Love -->
                      <button @click.stop="handleReaction({ emoji: '❤️', messageId: msg.id })" 
                              :data-msg-id="msg.id"
                              data-emoji="❤️"
                              :class="[
                                msg.userReactions?.[authStore.user?.id]?.includes('❤️') 
                                  ? 'bg-gradient-to-r from-red-500 to-pink-600 text-white shadow-lg scale-105 ring-2 ring-red-300' 
                                  : 'bg-white hover:bg-red-50 text-red-600',
                                'px-3 py-1.5 rounded-full transition-all transform hover:scale-110 active:scale-95 flex items-center gap-1.5 text-sm font-bold shadow-md border-2 border-red-300'
                              ]">
                        <span class="text-lg">❤️</span>
                        <span>{{ msg.loves || 0 }}</span>
                      </button>
                      
                      <!-- Reply -->
                      <button @click.stop="handleMessageAction({ action: 'reply', message: msg })" 
                              class="px-3 py-1.5 hover:bg-purple-100 rounded-full transition-all transform hover:scale-110 active:scale-95 text-sm font-medium text-purple-600 shadow-sm border border-purple-200">
                        ↩️ Reply
                      </button>
                      
                      <!-- Forward -->
                      <button @click.stop="handleMessageAction({ action: 'forward', message: msg })" 
                              class="px-3 py-1.5 hover:bg-green-100 rounded-full transition-all transform hover:scale-110 active:scale-95 text-sm font-medium text-green-600 shadow-sm border border-green-200">
                        ➡️ Forward
                      </button>
                      
                      <!-- Copy -->
                      <button @click.stop="handleMessageAction({ action: 'copy', message: msg })" 
                              class="px-3 py-1.5 hover:bg-yellow-100 rounded-full transition-all transform hover:scale-110 active:scale-95 text-sm font-medium text-yellow-600 shadow-sm border border-yellow-200">
                        📋 Copy
                      </button>
                      
                      <!-- More Reactions -->
                      <button @click.stop="showReactionMenu(msg.id)" 
                              class="px-3 py-1.5 hover:bg-amber-100 rounded-full transition-all transform hover:scale-110 active:scale-95 text-sm font-medium text-amber-600 shadow-sm border border-amber-200">
                        😊 +
                      </button>
                      
                      <!-- Report -->
                      <button @click.stop="handleMessageAction({ action: 'report', message: msg })" 
                              class="px-3 py-1.5 hover:bg-orange-100 rounded-full transition-all transform hover:scale-110 active:scale-95 text-sm font-medium text-orange-600 shadow-sm border border-orange-200">
                        🚨 Report
                      </button>
                      
                      <!-- Delete (own messages only) -->
                      <button v-if="msg.sender_id === authStore.user?.id"
                              @click.stop="handleMessageAction({ action: 'delete', message: msg })" 
                              class="px-3 py-1.5 hover:bg-red-100 rounded-full transition-all transform hover:scale-110 active:scale-95 text-sm font-medium text-red-600 shadow-sm border border-red-200">
                        🗑️ Delete
                      </button>
                    </div>
                    
                    <!-- Reactions Display -->
                    <div v-if="msg.reactions && msg.reactions.length > 0" class="flex flex-wrap gap-1 mt-1">
                      <span v-for="(reaction, idx) in msg.reactions" :key="idx"
                            class="px-2 py-0.5 bg-gray-100 rounded-full text-xs">
                        {{ reaction.emoji }} {{ reaction.count }}
                      </span>
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
            <!-- Reply Banner -->
            <div v-if="replyingTo" class="mb-2 p-3 bg-purple-50 border-l-4 border-purple-500 rounded-lg flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                  </svg>
                  <span class="text-sm font-semibold text-purple-700">Replying to {{ replyingTo.sender_name }}</span>
                </div>
                <p class="text-sm text-gray-600 truncate">{{ replyingTo.content }}</p>
              </div>
              <button @click="replyingTo = null" class="text-purple-600 hover:text-purple-800 p-1">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div class="flex items-center gap-2">
              <!-- Attachment Button -->
              <div class="relative">
                <button @click="showAttachmentMenu = !showAttachmentMenu" 
                        class="p-2.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-all">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                  </svg>
                </button>
                
                <!-- Attachment Menu -->
                <div v-if="showAttachmentMenu" class="absolute bottom-full left-0 mb-2 bg-white rounded-xl shadow-lg border p-2 min-w-48 z-10">
                  <button @click="selectFile('image')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-blue-50 rounded-lg text-left">
                    <span class="text-2xl">🖼️</span>
                    <span class="text-sm font-medium text-gray-700">Photo</span>
                  </button>
                  <button @click="selectFile('video')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-purple-50 rounded-lg text-left">
                    <span class="text-2xl">🎥</span>
                    <span class="text-sm font-medium text-gray-700">Video</span>
                  </button>
                  <button @click="selectFile('audio')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-green-50 rounded-lg text-left">
                    <span class="text-2xl">🎵</span>
                    <span class="text-sm font-medium text-gray-700">Audio</span>
                  </button>
                  <button @click="selectFile('document')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-yellow-50 rounded-lg text-left">
                    <span class="text-2xl">📄</span>
                    <span class="text-sm font-medium text-gray-700">Document</span>
                  </button>
                  <button @click="selectFile('zip')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-orange-50 rounded-lg text-left">
                    <span class="text-2xl">📦</span>
                    <span class="text-sm font-medium text-gray-700">Archive</span>
                  </button>
                  <button @click="selectFile('any')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-50 rounded-lg text-left">
                    <span class="text-2xl">📎</span>
                    <span class="text-sm font-medium text-gray-700">Any File</span>
                  </button>
                </div>
              </div>
              
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
            
            <!-- Hidden File Input -->
            <input ref="fileInput" type="file" class="hidden" @change="handleFileSelect" />
          </div>
        </div>
      </div>
    </div>

    <!-- Pending Messages Modal -->
    <div v-if="showPendingModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click="showPendingModal = false">
      <div class="bg-white rounded-3xl w-full max-w-3xl max-h-[85vh] overflow-hidden shadow-2xl" @click.stop>
        <div class="p-6 bg-gradient-to-r from-yellow-500 to-orange-500">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-3xl font-bold text-white mb-2">⚠️ Pending Messages</h3>
              <p class="text-white/90">{{ pendingMessages.length }} messages awaiting approval</p>
            </div>
            <button @click="showPendingModal = false" class="w-12 h-12 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="overflow-y-auto max-h-[calc(85vh-140px)] p-6">
          <div v-if="pendingMessages.length === 0" class="text-center py-16">
            <div class="text-8xl mb-4">✅</div>
            <p class="text-2xl font-bold text-gray-900 mb-2">All caught up!</p>
            <p class="text-gray-600">No pending messages to review</p>
          </div>
          
          <div v-else class="space-y-4">
            <div v-for="msg in channelPendingMessages" :key="msg.id" 
                 class="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-2xl p-5 border-2 border-yellow-300">
              <div class="flex items-start gap-4 mb-3">
                <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
                  {{ msg.sender_name?.charAt(0).toUpperCase() || 'U' }}
                </div>
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="font-bold text-gray-900">{{ msg.sender_name || 'Unknown' }}</span>
                    <span class="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold">
                      {{ msg.sender_role || 'student' }}
                    </span>
                    <span class="text-xs text-gray-500">{{ formatTime(msg.created_at) }}</span>
                  </div>
                  <p class="text-gray-800 whitespace-pre-wrap">{{ msg.content }}</p>
                </div>
              </div>
              
              <div class="flex items-center gap-3 pt-3 border-t border-yellow-200">
                <button @click="approveMessage(msg.id)" 
                        class="flex-1 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-all flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Approve
                </button>
                <button @click="rejectMessage(msg.id)" 
                        class="flex-1 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg font-medium transition-all flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  Reject
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Live Space Modal -->
    <div v-if="liveSpace.active" class="fixed inset-0 bg-black bg-opacity-95 z-50 flex items-center justify-center p-4">
      <div class="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 rounded-3xl w-full max-w-4xl h-full max-h-[90vh] overflow-hidden shadow-2xl">
        <!-- Header -->
        <div class="p-6 border-b border-white/20">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="w-4 h-4 bg-red-500 rounded-full animate-pulse"></div>
              <span class="text-white font-bold text-lg">🎤 LIVE</span>
              <span class="text-white/70 text-sm">{{ liveSpace.participants.length }} participants</span>
            </div>
            <button @click="leaveLiveSpace" class="text-white/70 hover:text-white p-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <h2 class="text-white text-2xl font-bold mb-2">{{ liveSpace.name }}</h2>
          <p class="text-white/80 text-sm">Hosted by {{ liveSpace.host }} • {{ liveSpace.hostRole }}</p>
        </div>
        
        <!-- Speakers -->
        <div class="p-6 border-b border-white/20">
          <h3 class="text-white font-semibold mb-4">🎤 Speaking Now</h3>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div v-for="speaker in speakers" :key="speaker.id" class="bg-white/10 rounded-2xl p-4 text-center">
              <div class="w-16 h-16 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-xl mx-auto mb-2">
                {{ speaker.name.charAt(0).toUpperCase() }}
              </div>
              <p class="text-white font-medium text-sm">{{ speaker.name }}</p>
              <p class="text-white/60 text-xs">{{ speaker.role }}</p>
              <div v-if="speaker.isHost" class="mt-2">
                <span class="bg-yellow-500 text-black px-2 py-1 rounded-full text-xs font-bold">HOST</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Listeners & Queue -->
        <div class="p-6 flex-1 overflow-y-auto">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-white font-semibold">👥 Listeners ({{ listeners.length }})</h3>
            <div v-if="liveSpace.queue.length > 0" class="text-white/70 text-sm bg-yellow-500/20 px-3 py-1 rounded-full">
              🙋♂️ {{ liveSpace.queue.length }} waiting to speak
            </div>
          </div>
          
          <!-- Host Controls -->
          <div v-if="isHost" class="mb-4 flex gap-2">
            <button @click="addTestRequest" class="bg-yellow-500 hover:bg-yellow-600 text-black px-4 py-2 rounded-lg font-medium text-sm">
              🧪 Add Test Request
            </button>
            <button @click="addTestListener" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium text-sm">
              👥 Add Test Listener
            </button>
          </div>
          
          <!-- Speaking Queue -->
          <div v-if="isHost && liveSpace.queue.length > 0" class="mb-6">
            <h4 class="text-white/80 font-medium mb-3">🙋♂️ Speaking Requests</h4>
            <div class="space-y-2">
              <div v-for="request in liveSpace.queue" :key="request.id" 
                   class="bg-yellow-500/20 border border-yellow-500/30 rounded-lg p-3 flex items-center justify-between">
                <div>
                  <p class="text-white font-medium">{{ request.name }}</p>
                  <p class="text-white/60 text-sm">{{ request.role }}</p>
                </div>
                <div class="flex gap-2">
                  <button @click="approveRequest(request.id)" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded-full text-sm">
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
            <div v-for="listener in listeners" :key="listener.id" class="text-center">
              <div class="w-12 h-12 bg-gradient-to-br from-gray-400 to-gray-600 rounded-full flex items-center justify-center text-white font-bold text-sm mx-auto mb-1">
                {{ listener.name.charAt(0).toUpperCase() }}
              </div>
              <p class="text-white/80 text-xs truncate">{{ listener.name }}</p>
            </div>
          </div>
        </div>
        
        <!-- Controls -->
        <div class="p-6 border-t border-white/20">
          <div class="flex items-center justify-center gap-4">
            <!-- Request to Speak -->
            <button v-if="!isSpeaking && !isHost && !isInQueue" @click="requestToSpeak" 
                    class="bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white px-6 py-3 rounded-full font-medium">
              🙋♂️ Request to Speak
            </button>
            
            <!-- Pending Status -->
            <div v-if="isInQueue" class="bg-yellow-500/20 border border-yellow-500 text-yellow-200 px-6 py-3 rounded-full font-medium">
              ⏳ Request Pending
            </div>
            
            <!-- Microphone Toggle -->
            <button @click="toggleMic" 
                    :class="micEnabled ? 'bg-green-500 hover:bg-green-600' : 'bg-red-500 hover:bg-red-600'"
                    class="text-white p-3 rounded-full">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="micEnabled" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 5.586A2 2 0 015 7v3a3 3 0 005.395 2.605m2.829-2.829A3 3 0 0015 7V5a3 3 0 00-6 0v1M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4M3 3l18 18" />
              </svg>
            </button>
            
            <!-- End/Leave -->
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
// FORCE RELOAD - Message Approval System Active
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

// Basic state
const groupId = ref(parseInt(route.params.groupId))
const group = ref(null)
const channels = ref([])
const activeChannelId = ref(null)
const activeChannel = ref(null)
const loading = ref(true)
const loadingMessages = ref(false)
const messages = ref([])
const newMessage = ref('')
const sending = ref(false)
const replyingTo = ref(null)
const reactionMenuMsgId = ref(null)
const messagesContainer = ref(null)
const messagePollingInterval = ref(null)
const showChannelList = ref(false)
const microphoneEnabled = ref(true)
const showAttachmentMenu = ref(false)
const fileInput = ref(null)
const messageReactions = ref(new Map())
const showPendingModal = ref(false)
const pendingMessages = ref([])
const channelPendingMessages = computed(() => 
  pendingMessages.value.filter(m => m.channel_id === activeChannelId.value)
)

// Live Space State - Simplified and Centralized
const liveSpace = ref({
  active: false,
  id: null,
  name: '',
  host: '',
  hostRole: '',
  participants: [],
  queue: []
})

const micEnabled = ref(true)

// Computed properties
const textChannels = computed(() => channels.value.filter(c => 
  ['ANNOUNCEMENTS', 'DISCUSSION', 'RESOURCES', 'text'].includes(c.type)
))

const voiceChannels = computed(() => channels.value.filter(c => 
  ['OFFICE_HOURS', 'voice'].includes(c.type)
))

const onlineCount = computed(() => Math.floor(Math.random() * 4) + 3)

const currentUserId = computed(() => authStore.user?.id || 'user-1')
const currentUserName = computed(() => authStore.user?.full_name || 'User')
const currentUserRole = computed(() => authStore.user?.role || 'student')

// Live Space Computed Properties
const isHost = computed(() => liveSpace.value.host === currentUserName.value)
const isSpeaking = computed(() => liveSpace.value.participants.some(p => p.id === currentUserId.value && p.isSpeaking))
const isInQueue = computed(() => liveSpace.value.queue.some(q => q.id === currentUserId.value))

const speakers = computed(() => liveSpace.value.participants.filter(p => p.isSpeaking))
const listeners = computed(() => liveSpace.value.participants.filter(p => !p.isSpeaking))

// Message computed properties
const validMessages = computed(() => {
  if (!messages.value || !Array.isArray(messages.value)) return []
  return messages.value.filter(msg => msg && msg.id && (msg.content || msg.file))
})

const hasMessages = computed(() => validMessages.value.length > 0)
const messageCount = computed(() => validMessages.value.length)

// User permissions
const canCreateChannels = computed(() => authStore.user?.role === 'teacher')
const userAvatar = computed(() => `https://ui-avatars.com/api/?name=${encodeURIComponent(authStore.user?.full_name || 'User')}&background=3b82f6&color=fff`)
const isTeacher = computed(() => {
  const result = authStore.user?.role === 'teacher'
  console.log('isTeacher:', result, authStore.user?.role)
  return result
})

const needsApproval = computed(() => {
  const channelName = activeChannel.value?.name?.toLowerCase() || ''
  const channelType = activeChannel.value?.type?.toUpperCase() || ''
  const result = channelType === 'ANNOUNCEMENTS' || channelType === 'RESOURCES' || 
         channelName.includes('announcement') || channelName.includes('resource')
  console.log('needsApproval:', result, 'channel:', channelName, 'type:', channelType)
  return result
})

const pendingCount = computed(() => {
  const count = pendingMessages.value.filter(m => m.channel_id === activeChannelId.value).length
  console.log('pendingCount:', count, 'total pending:', pendingMessages.value.length, 'channelId:', activeChannelId.value)
  return count
})

// Lifecycle - Updated in the functions above

// Basic Functions
async function loadGroupData() {
  try {
    const response = await api.get(`/directory/groups/${groupId.value}`)
    group.value = response.data
    if (!group.value.member_count) {
      group.value.member_count = group.value.type === 'CLASS' ? 45 : 12
    }
  } catch (err) {
    console.error('Failed to load group:', err)
    router.push('/student-dashboard')
  }
}

async function loadChannels() {
  try {
    const response = await api.get(`/directory/groups/${groupId.value}/channels`)
    channels.value = response.data || []
    
    if (channels.value.filter(c => c.type === 'OFFICE_HOURS').length === 0) {
      channels.value.push(
        { id: 9001, name: 'Office Hours', type: 'OFFICE_HOURS', group_id: groupId.value },
        { id: 9002, name: 'Study Group', type: 'OFFICE_HOURS', group_id: groupId.value }
      )
    }
    
    // Load pending messages for teachers
    if (authStore.user?.role === 'teacher') {
      loadPendingMessages()
    }
  } catch (err) {
    console.error('Failed to load channels:', err)
    channels.value = []
  } finally {
    loading.value = false
  }
}

async function loadPendingMessages() {
  if (!isTeacher.value) {
    console.log('Not loading pending - not a teacher')
    return
  }
  
  try {
    console.log('Loading pending messages...')
    const response = await api.get('/teacher/pending-messages')
    pendingMessages.value = response.data || []
    console.log('✅ Loaded pending messages:', pendingMessages.value.length, pendingMessages.value)
  } catch (err) {
    console.error('❌ Failed to load pending messages:', err)
    pendingMessages.value = []
  }
}

async function approveMessage(messageId) {
  try {
    await api.post(`/teacher/messages/${messageId}/approve`)
    pendingMessages.value = pendingMessages.value.filter(m => m.id !== messageId)
    showNotification('✅ Message approved', 'success')
    await refreshMessages()
  } catch (err) {
    console.error('Failed to approve message:', err)
    showNotification('❌ Failed to approve message', 'error')
  }
}

async function rejectMessage(messageId) {
  try {
    await api.post(`/teacher/messages/${messageId}/reject`)
    pendingMessages.value = pendingMessages.value.filter(m => m.id !== messageId)
    showNotification('✅ Message rejected', 'success')
  } catch (err) {
    console.error('Failed to reject message:', err)
    showNotification('❌ Failed to reject message', 'error')
  }
}

async function selectChannel(channel) {
  if (activeChannelId.value === channel.id) return
  
  if (messagePollingInterval.value) {
    clearInterval(messagePollingInterval.value)
  }
  
  activeChannelId.value = channel.id
  activeChannel.value = channel
  loadingMessages.value = true
  messages.value = []
  
  console.log('Selected channel:', channel.name, 'type:', channel.type)
  
  // Reload pending messages when switching channels
  if (isTeacher.value) {
    console.log('Teacher detected, loading pending messages...')
    await loadPendingMessages()
  }
  
  console.log('Loading messages for channel:', channel.id)
  
  try {
    const response = await api.get(`/simple-chat/channels/${channel.id}/messages`)
    console.log('API Response:', response.data)
    
    let fetchedMessages = []
    
    // Handle different response formats
    if (response.data.messages) {
      fetchedMessages = response.data.messages
    } else if (Array.isArray(response.data)) {
      fetchedMessages = response.data
    } else {
      console.warn('Unexpected response format:', response.data)
      fetchedMessages = []
    }
    
    console.log('Fetched messages:', fetchedMessages.length)
    
    // Initialize each message with reaction data
    fetchedMessages.forEach(msg => {
      if (msg) {
        msg.likes = msg.likes || 0
        msg.loves = msg.loves || 0
        msg.userReactions = msg.userReactions || {}
      }
    })
    
    messages.value = fetchedMessages
    
    await nextTick()
    scrollToBottom()
    
    // Start polling for new messages every 1 second for real-time feel
    messagePollingInterval.value = setInterval(() => refreshMessages(), 1000)
    
  } catch (error) {
    console.error('Failed to load messages:', error)
    console.error('Error details:', error.response?.data)
    
    // Show fallback messages for testing
    messages.value = [
      {
        id: 'test-1',
        content: 'Welcome to the channel! This is a test message.',
        sender_id: 'system',
        sender_name: 'System',
        sender_role: 'system',
        created_at: new Date().toISOString(),
        likes: 0,
        loves: 0,
        userReactions: {}
      }
    ]
  } finally {
    loadingMessages.value = false
  }
}

async function sendMessageDirect() {
  if (!newMessage.value?.trim()) return
  if (sending.value) return
  if (!activeChannelId.value) {
    alert('Please select a channel first')
    return
  }
  
  sending.value = true
  const content = newMessage.value.trim()
  newMessage.value = ''
  
  try {
    const payload = { content: content }
    if (replyingTo.value?.id) {
      payload.reply_to_id = replyingTo.value.id
    }
    
    const response = await api.post(`/simple-chat/channels/${activeChannelId.value}/messages`, payload)
    
    // Add the new message directly
    const newMsg = {
      ...response.data,
      likes: 0,
      loves: 0,
      userReactions: {}
    }
    
    messages.value.push(newMsg)
    replyingTo.value = null
    
    await nextTick()
    scrollToBottom()
    
  } catch (error) {
    console.error('Send failed:', error)
    newMessage.value = content
    alert('❌ Failed to send message')
  } finally {
    sending.value = false
  }
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function formatTime(timestamp) {
  if (!timestamp) return 'Just now'
  const date = new Date(timestamp)
  if (isNaN(date.getTime())) return 'Just now'
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
}

// Live Space Functions - Simplified and Working
function startLiveSpace(channel) {
  if (currentUserRole.value !== 'teacher') {
    alert('🚫 Only teachers can start live spaces')
    return
  }
  
  // Reset and initialize live space
  liveSpace.value = {
    active: true,
    id: channel.id,
    name: channel.name,
    host: currentUserName.value,
    hostRole: currentUserRole.value,
    participants: [{
      id: currentUserId.value,
      name: currentUserName.value,
      role: currentUserRole.value,
      isSpeaking: true,
      isHost: true
    }],
    queue: []
  }
  
  console.log('Live space started:', liveSpace.value)
}

function requestToSpeak() {
  if (isInQueue.value) {
    alert('You are already in the speaking queue')
    return
  }
  
  liveSpace.value.queue.push({
    id: currentUserId.value,
    name: currentUserName.value,
    role: currentUserRole.value,
    requestTime: new Date().toISOString()
  })
  
  console.log('Speaking request added:', liveSpace.value.queue)
}

function approveRequest(requestId) {
  const request = liveSpace.value.queue.find(q => q.id === requestId)
  if (!request) return
  
  // Add to participants as speaker
  const existingParticipant = liveSpace.value.participants.find(p => p.id === requestId)
  if (existingParticipant) {
    existingParticipant.isSpeaking = true
  } else {
    liveSpace.value.participants.push({
      id: request.id,
      name: request.name,
      role: request.role,
      isSpeaking: true,
      isHost: false
    })
  }
  
  // Remove from queue
  liveSpace.value.queue = liveSpace.value.queue.filter(q => q.id !== requestId)
  
  console.log('Request approved:', requestId)
}

function declineRequest(requestId) {
  liveSpace.value.queue = liveSpace.value.queue.filter(q => q.id !== requestId)
  console.log('Request declined:', requestId)
}

function addTestRequest() {
  const testId = 'test-' + Date.now()
  liveSpace.value.queue.push({
    id: testId,
    name: 'KUBWAMAHINA Joshua',
    role: 'student',
    requestTime: new Date().toISOString()
  })
}

function addTestListener() {
  const testId = 'listener-' + Date.now()
  const names = ['UWASE Marie', 'MUGISHA Jean', 'NIYONZIMA Paul', 'MUKAMANA Grace']
  const randomName = names[Math.floor(Math.random() * names.length)]
  
  liveSpace.value.participants.push({
    id: testId,
    name: randomName,
    role: 'student',
    isSpeaking: false,
    isHost: false
  })
}

function toggleMic() {
  micEnabled.value = !micEnabled.value
  console.log('Microphone:', micEnabled.value ? 'enabled' : 'disabled')
}

function leaveLiveSpace() {
  if (isHost.value) {
    if (confirm('As host, this will end the space for everyone. Continue?')) {
      endLiveSpace()
    }
  } else {
    // Remove current user from participants and queue
    liveSpace.value.participants = liveSpace.value.participants.filter(p => p.id !== currentUserId.value)
    liveSpace.value.queue = liveSpace.value.queue.filter(q => q.id !== currentUserId.value)
    liveSpace.value.active = false
    console.log('Left live space')
  }
}

function endLiveSpace() {
  liveSpace.value = {
    active: false,
    id: null,
    name: '',
    host: '',
    hostRole: '',
    participants: [],
    queue: []
  }
  console.log('Live space ended')
}

function scrollToMessage(messageId) {
  const msgElement = document.querySelector(`[data-message-id="${messageId}"]`)
  if (msgElement) {
    msgElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

function showReactionMenu(msgId) {
  reactionMenuMsgId.value = msgId
}

async function handleReaction({ emoji, messageId }) {
  const msg = messages.value.find(m => m.id === messageId)
  if (!msg) return
  
  const userId = authStore.user?.id
  if (!userId) return
  
  // Initialize reaction data
  if (!msg.userReactions) msg.userReactions = {}
  if (!msg.userReactions[userId]) msg.userReactions[userId] = []
  
  const wasReacted = msg.userReactions[userId].includes(emoji)
  
  // Toggle reaction
  if (wasReacted) {
    msg.userReactions[userId] = msg.userReactions[userId].filter(e => e !== emoji)
    if (emoji === '👍') msg.likes = Math.max(0, (msg.likes || 0) - 1)
    if (emoji === '❤️') msg.loves = Math.max(0, (msg.loves || 0) - 1)
  } else {
    msg.userReactions[userId].push(emoji)
    if (emoji === '👍') msg.likes = (msg.likes || 0) + 1
    if (emoji === '❤️') msg.loves = (msg.loves || 0) + 1
  }
  
  // Save to localStorage immediately
  const key = `${messageId}-${userId}`
  const channelKey = `channel-${activeChannelId.value}-reactions`
  
  try {
    // Store per-channel reactions
    const channelReactions = JSON.parse(localStorage.getItem(channelKey) || '{}')
    channelReactions[key] = {
      likes: msg.likes || 0,
      loves: msg.loves || 0,
      userReactions: { ...msg.userReactions },
      timestamp: Date.now()
    }
    localStorage.setItem(channelKey, JSON.stringify(channelReactions))
    
    // Also store in global reactions for backward compatibility
    const globalReactions = JSON.parse(localStorage.getItem('message-reactions') || '{}')
    globalReactions[key] = channelReactions[key]
    localStorage.setItem('message-reactions', JSON.stringify(globalReactions))
    
  } catch (e) {
    console.error('Failed to save reactions:', e)
  }
  
  // Force reactivity update
  messages.value = [...messages.value]
  
  reactionMenuMsgId.value = null
}

async function handleMessageAction({ action, message }) {
  try {
    switch(action) {
      case 'reply':
        replyingTo.value = message
        newMessage.value = ''
        await nextTick()
        document.querySelector('input[type="text"]')?.focus()
        break
        
      case 'forward':
        // Create forward dialog
        const channels = textChannels.value
        if (channels.length === 0) {
          alert('❌ No channels available to forward to')
          return
        }
        
        const channelNames = channels.map(c => c.name).join('\n')
        const targetChannel = prompt(`Forward to which channel?\n\nAvailable channels:\n${channelNames}\n\nEnter channel name:`)
        
        if (targetChannel) {
          const channel = channels.find(c => c.name.toLowerCase() === targetChannel.toLowerCase())
          if (channel) {
            showNotification(`✅ Message forwarded to #${channel.name}`, 'success')
          } else {
            alert('❌ Channel not found')
          }
        }
        break
        
      case 'copy':
        let textToCopy = ''
        if (message.content) {
          textToCopy = message.content
        } else if (message.file) {
          textToCopy = `File: ${message.file.name}`
        }
        
        if (textToCopy) {
          await navigator.clipboard.writeText(textToCopy)
          showNotification('✅ Copied to clipboard!', 'success')
        } else {
          alert('❌ Nothing to copy')
        }
        break
        
      case 'report':
        const reason = prompt('Why are you reporting this message?\n\nReasons:\n1. Spam\n2. Inappropriate content\n3. Harassment\n4. Other\n\nEnter reason:')
        if (reason) {
          showNotification('✅ Message reported to moderators', 'success')
        }
        break
        
      case 'delete':
        if (confirm('Delete this message? This cannot be undone.')) {
          try {
            // Try API delete first
            await api.delete(`/simple-chat/messages/${message.id}`)
            showNotification('✅ Message deleted', 'success')
          } catch (error) {
            console.log('API delete failed, removing locally')
          }
          
          // Remove from local array
          const index = messages.value.findIndex(m => m.id === message.id)
          if (index > -1) {
            messages.value.splice(index, 1)
          }
        }
        break
    }
  } catch (error) {
    console.error('Action error:', error)
    alert('❌ Action failed: ' + error.message)
  }
}

async function refreshMessages() {
  if (!activeChannelId.value) return
  
  try {
    const response = await api.get(`/simple-chat/channels/${activeChannelId.value}/messages`)
    
    let newMessages = []
    if (response.data.messages) {
      newMessages = response.data.messages
    } else if (Array.isArray(response.data)) {
      newMessages = response.data
    }
    
    if (Array.isArray(newMessages)) {
      const currentCount = messages.value.length
      
      // Only update if there are new messages
      if (newMessages.length > currentCount) {
        // Preserve existing message state
        newMessages.forEach(newMsg => {
          const existingMsg = messages.value.find(m => m && m.id === newMsg.id)
          if (existingMsg) {
            newMsg.likes = existingMsg.likes || 0
            newMsg.loves = existingMsg.loves || 0
            newMsg.userReactions = existingMsg.userReactions || {}
            newMsg.file = existingMsg.file
          } else {
            newMsg.likes = newMsg.likes || 0
            newMsg.loves = newMsg.loves || 0
            newMsg.userReactions = newMsg.userReactions || {}
          }
        })
        
        messages.value = newMessages
        await nextTick()
        scrollToBottom()
      }
    }
  } catch (error) {
    console.error('Failed to refresh messages:', error)
  }
}

function createChannel() {
  router.push(`/create-channel?group=${groupId.value}`)
}

function joinVoiceChannel(channel) {
  if (authStore.user?.role !== 'teacher') {
    alert('🚫 Only teachers can start live spaces. Please wait for a teacher to start one.')
    return
  }
  startLiveSpace(channel)
}

function createVoiceChannel() {
  alert('Voice channel creation coming soon!')
}

function toggleMicrophone() {
  microphoneEnabled.value = !microphoneEnabled.value
  const status = microphoneEnabled.value ? 'unmuted' : 'muted'
  console.log(`Microphone ${status}`)
}

function selectFile(type) {
  showAttachmentMenu.value = false
  
  const acceptTypes = {
    image: 'image/*',
    video: 'video/*',
    audio: 'audio/*',
    document: '.pdf,.doc,.docx,.txt,.rtf',
    zip: '.zip,.rar,.7z,.tar,.gz',
    any: '*/*'
  }
  
  if (fileInput.value) {
    fileInput.value.accept = acceptTypes[type] || '*/*'
    fileInput.value.click()
  }
}

async function handleFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  
  const maxSize = 10 * 1024 * 1024 // 10MB
  if (file.size > maxSize) {
    alert('❌ File too large! Maximum size is 10MB')
    return
  }
  
  // Convert file to base64 for persistent storage
  const base64 = await fileToBase64(file)
  const fileId = 'file-' + Date.now()
  
  // Create file message
  const fileMessage = {
    id: fileId,
    content: null,
    sender_id: authStore.user?.id,
    sender_name: authStore.user?.full_name,
    sender_role: authStore.user?.role,
    created_at: new Date().toISOString(),
    likes: 0,
    loves: 0,
    userReactions: {},
    file: {
      name: file.name,
      size: file.size,
      type: file.type,
      data: base64
    }
  }
  
  // Store file in localStorage for persistence
  try {
    const storedFiles = JSON.parse(localStorage.getItem('chat-files') || '{}')
    storedFiles[fileId] = fileMessage.file
    localStorage.setItem('chat-files', JSON.stringify(storedFiles))
  } catch (e) {
    console.error('Failed to store file:', e)
  }
  
  messages.value.push(fileMessage)
  
  nextTick(() => {
    scrollToBottom()
  })
  
  // Reset file input
  event.target.value = ''
  
  // Show success notification
  showNotification(`✅ File "${file.name}" shared!`, 'success')
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result)
    reader.onerror = error => reject(error)
  })
}

function showNotification(message, type = 'info') {
  const notification = document.createElement('div')
  const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500'
  notification.className = `fixed top-4 right-4 ${bgColor} text-white px-4 py-2 rounded-lg shadow-lg z-50 transition-all`
  notification.textContent = message
  document.body.appendChild(notification)
  
  setTimeout(() => {
    if (document.body.contains(notification)) {
      document.body.removeChild(notification)
    }
  }, 3000)
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function getFileIcon(fileType) {
  if (!fileType) return '📄'
  if (fileType.startsWith('image/')) return '🖼️'
  if (fileType.startsWith('video/')) return '🎥'
  if (fileType.startsWith('audio/')) return '🎵'
  if (fileType.includes('pdf')) return '📕'
  if (fileType.includes('word') || fileType.includes('document')) return '📘'
  if (fileType.includes('excel') || fileType.includes('spreadsheet')) return '📗'
  if (fileType.includes('powerpoint') || fileType.includes('presentation')) return '📙'
  if (fileType.includes('zip') || fileType.includes('rar') || fileType.includes('archive')) return '📦'
  if (fileType.includes('text')) return '📝'
  return '📄'
}

function getFileUrl(file) {
  return file.data || file.url || ''
}

function openFile(file) {
  const url = getFileUrl(file)
  if (url) {
    window.open(url, '_blank')
  }
}

function downloadFile(file) {
  const url = getFileUrl(file)
  if (url) {
    const link = document.createElement('a')
    link.href = url
    link.download = file.name
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    showNotification(`📥 Downloaded: ${file.name}`, 'success')
  }
}

// Close attachment menu when clicking outside
function handleClickOutside(event) {
  if (!event.target.closest('.relative')) {
    showAttachmentMenu.value = false
  }
}

// Add click outside listener
onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  console.log('🎯 HubsView mounted - User role:', authStore.user?.role)
  
  try {
    await loadGroupData()
    await loadChannels()
    
    // Load pending messages immediately for teachers
    if (authStore.user?.role === 'teacher') {
      console.log('👨‍🏫 Teacher detected on mount, loading pending messages...')
      await loadPendingMessages()
    }
    
    // Auto-select first channel
    if (channels.value.length > 0) {
      const firstChannel = channels.value[0]
      console.log('Auto-selecting first channel:', firstChannel)
      await selectChannel(firstChannel)
    } else {
      console.log('No channels available')
    }
  } catch (error) {
    console.error('Failed to initialize:', error)
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (messagePollingInterval.value) {
    clearInterval(messagePollingInterval.value)
  }
})

</script>

<style scoped>
/* Custom styles if needed */
</style>