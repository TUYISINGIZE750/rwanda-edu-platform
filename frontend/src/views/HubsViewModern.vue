<template>
  <div class="h-screen flex transition-colors duration-300" :class="themeClasses.background">
    <!-- Sidebar -->
    <div class="w-80 backdrop-blur-xl border-r shadow-2xl flex flex-col transition-colors duration-300" :class="[themeClasses.sidebar, themeClasses.border]">
      <!-- Header -->
      <div class="p-4 border-b bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 shadow-lg">
        <div class="flex items-center justify-between text-white">
          <div>
            <h2 class="font-bold text-lg">{{ group?.name }}</h2>
            <p class="text-xs text-blue-100">{{ group?.member_count }} members</p>
          </div>
          <button @click="$router.push('/home')" class="hover:bg-white/20 p-2 rounded-full">
            <ChevronLeftIcon class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Channels -->
      <div class="flex-1 overflow-y-auto p-2 bg-gradient-to-b from-white/50 to-transparent">
        <div class="text-xs font-semibold text-gray-500 px-3 py-2">CHANNELS</div>
        <div v-for="channel in channels" :key="channel.id"
             @click="channel.can_access ? selectChannel(channel) : showAccessDenied()"
             class="flex items-center gap-3 px-3 py-2 rounded-xl transition-all transform"
             :class="[
               activeChannelId === channel.id ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg' : 'hover:bg-white/60 hover:shadow-md',
               channel.can_access ? 'cursor-pointer hover:scale-105' : 'opacity-50 cursor-not-allowed'
             ]">
          <span class="text-xl">{{ channel.can_access ? '#' : '🔒' }}</span>
          <span class="font-medium">{{ channel.name }}</span>
        </div>
      </div>
    </div>

    <!-- Chat Area -->
    <div class="flex-1 flex flex-col">
      <!-- Chat Header -->
      <div class="h-16 backdrop-blur-xl border-b shadow-lg px-6 flex items-center justify-between transition-colors duration-300" :class="[themeClasses.header, themeClasses.border]">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
            #
          </div>
          <div>
            <h3 class="font-semibold">{{ activeChannel?.name }}</h3>
            <p class="text-xs text-gray-500">{{ onlineCount }} online</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <!-- Live Session Button -->
          <button @click="showLiveMenu = !showLiveMenu" 
                  class="px-4 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-xl hover:from-red-600 hover:to-pink-600 transition-all flex items-center gap-2 relative shadow-lg hover:shadow-xl transform hover:scale-105">
            <span class="text-lg">🎥</span>
            <span class="font-medium">Go Live</span>
            <span v-if="activeLiveSession" class="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-pulse"></span>
          </button>
          
          <button v-if="authStore.user?.role === 'TEACHER' && activeChannel?.type === 'ANNOUNCEMENTS'" 
                  @click="showPendingMessages = true"
                  class="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-all flex items-center gap-2">
            <span class="w-5 h-5 bg-white text-orange-500 rounded-full flex items-center justify-center text-xs font-bold">{{ pendingCount }}</span>
            Pending
          </button>
          
          <button v-if="authStore.user?.role === 'TEACHER'" 
                  @click="showPendingLive = true"
                  class="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-all flex items-center gap-2"
                  :class="pendingLiveCount > 0 ? 'animate-pulse' : 'opacity-75'">
            <span class="w-5 h-5 bg-white text-purple-500 rounded-full flex items-center justify-center text-xs font-bold">{{ pendingLiveCount }}</span>
            Live Requests
          </button>
          
          <button v-if="authStore.user?.role === 'TEACHER' && activeLiveSession" 
                  @click="cleanupSessions"
                  class="px-4 py-2 bg-red-500 text-white rounded-xl hover:bg-red-600 transition-all flex items-center gap-2 shadow-lg">
            🗑️ End All
          </button>
          
          <button @click="showThemeMenu = !showThemeMenu" 
                  class="p-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 flex items-center gap-2">
            <PaintBrushIcon class="w-5 h-5" />
            <span class="font-medium">Theme</span>
          </button>
        </div>
      </div>

      <!-- Live Session Banner -->
      <div v-if="activeLiveSession && !currentLiveSession" 
           class="bg-gradient-to-r from-red-500 via-pink-500 to-purple-500 text-white p-4 flex items-center justify-between shadow-2xl border-b-4 border-white/20">
        <div class="flex items-center gap-4">
          <div class="relative">
            <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
              <div class="w-3 h-3 bg-white rounded-full animate-ping absolute"></div>
              <div class="w-3 h-3 bg-white rounded-full"></div>
            </div>
          </div>
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="text-2xl">{{ activeLiveSession.type === 'VIDEO' ? '🎥' : '🎤' }}</span>
              <p class="font-bold text-lg">{{ activeLiveSession.title }}</p>
            </div>
            <p class="text-sm text-white/90 flex items-center gap-2">
              <span class="px-2 py-0.5 bg-white/20 rounded-full text-xs font-semibold">LIVE</span>
              {{ activeLiveSession.type }} session • Hosted by {{ activeLiveSession.host_name }}
            </p>
          </div>
        </div>
        <button @click="joinLiveSession(activeLiveSession)" 
                class="px-8 py-3 bg-white text-red-600 font-bold rounded-xl hover:bg-gray-100 transition-all shadow-xl hover:shadow-2xl transform hover:scale-105 flex items-center gap-2">
          <PlayIcon class="w-5 h-5" />
          Join Now
        </button>
      </div>

      <!-- Messages -->
      <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-6 backdrop-blur-sm transition-colors duration-300" :class="themeClasses.messages">
        <div v-if="loadingMessages" class="flex justify-center py-12">
          <div class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
        </div>

        <div v-else-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-gray-400">
          <ChatBubbleLeftRightIcon class="w-16 h-16 mb-4" />
          <p class="text-lg font-medium">No messages yet</p>
          <p class="text-sm">Start the conversation!</p>
        </div>

        <div v-else v-for="msg in messages" :key="msg.id" class="flex gap-3 group"
             :class="msg.sender_id === authStore.user?.id ? 'flex-row-reverse' : ''">
          <!-- Avatar -->
          <div class="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center text-white font-bold shadow-lg ring-2 ring-white"
               :class="msg.sender_id === authStore.user?.id ? 'bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500' : 'bg-gradient-to-br from-orange-500 via-red-500 to-pink-500'">
            {{ msg.sender_name?.charAt(0) || 'U' }}
          </div>

          <!-- Message Content -->
          <div class="max-w-lg">
            <div v-if="msg.sender_id !== authStore.user?.id" class="text-xs font-semibold mb-1"
                 :class="msg.sender_id === authStore.user?.id ? 'text-blue-600 text-right' : 'text-purple-600'">
              {{ msg.sender_name }}
            </div>
            <div v-else class="text-xs font-semibold text-blue-600 text-right mb-1">
              You
            </div>

            <div class="rounded-2xl px-4 py-3 shadow-lg transition-all group-hover:shadow-xl backdrop-blur-sm"
                 :class="msg.sender_id === authStore.user?.id ? 'bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white' : 'bg-white/90 text-gray-900 border border-purple-100'">
              
              <!-- Reply Preview -->
              <div v-if="msg.reply_to" class="mb-2 p-2 rounded-lg border-l-4 transition-all"
                   :class="msg.sender_id === authStore.user?.id ? 'border-blue-300 bg-white/20' : 'border-purple-400 bg-purple-50'">
                <p class="text-xs font-semibold" :class="msg.sender_id === authStore.user?.id ? 'text-white/90' : 'text-purple-700'">{{ msg.reply_to.sender_name }}</p>
                <p class="text-xs" :class="msg.sender_id === authStore.user?.id ? 'text-white/80' : 'text-gray-600'">{{ msg.reply_to.content }}</p>
              </div>

              <!-- File Content -->
              <div v-if="msg.file_url" class="mb-2">
                <!-- Image -->
                <div v-if="msg.file_type?.startsWith('image/')" class="relative group">
                  <img :src="getFullFileUrl(msg.file_url)" 
                       :alt="msg.file_name"
                       class="max-w-sm rounded-lg cursor-pointer hover:opacity-95 transition-opacity shadow-md"
                       @click="openImageModal(getFullFileUrl(msg.file_url), msg.file_name, msg.file_size)" />
                  <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <a :href="getFullFileUrl(msg.file_url)" download :download="msg.file_name"
                       class="bg-black/50 text-white p-2 rounded-full hover:bg-black/70 inline-block">
                      <ArrowDownTrayIcon class="w-4 h-4" />
                    </a>
                  </div>
                  <p class="text-xs mt-1 opacity-70">{{ msg.file_name }}</p>
                </div>
                
                <!-- Video -->
                <div v-else-if="msg.file_type?.startsWith('video/')" class="relative">
                  <video :src="getFullFileUrl(msg.file_url)" 
                         controls 
                         class="max-w-sm rounded-lg shadow-md">
                    Your browser does not support video playback.
                  </video>
                  <p class="text-xs mt-1 opacity-70">{{ msg.file_name }}</p>
                </div>
                
                <!-- Audio -->
                <div v-else-if="msg.file_type?.startsWith('audio/')" class="bg-gray-100 rounded-lg p-3">
                  <div class="flex items-center gap-2 mb-2">
                    <span class="text-2xl">🎵</span>
                    <span class="text-sm font-medium">{{ msg.file_name }}</span>
                  </div>
                  <audio :src="getFullFileUrl(msg.file_url)" 
                         controls 
                         class="w-full">
                    Your browser does not support audio playback.
                  </audio>
                </div>
                
                <!-- Other Files -->
                <a v-else 
                   :href="getFullFileUrl(msg.file_url)" 
                   download
                   :download="msg.file_name"
                   class="flex items-center gap-3 p-3 rounded-lg hover:bg-black/5 transition-all border border-gray-200">
                  <span class="text-3xl">{{ getFileIcon(msg.file_type) }}</span>
                  <div class="flex-1">
                    <p class="text-sm font-medium">{{ msg.file_name }}</p>
                    <p class="text-xs opacity-70">{{ formatFileSize(msg.file_size) }} • Click to download</p>
                  </div>
                  <ArrowDownTrayIcon class="w-5 h-5 opacity-50" />
                </a>
              </div>

              <!-- Message Text -->
              <p v-if="msg.content" class="text-sm leading-relaxed" :style="getMessageStyle(msg)">{{ msg.content }}</p>

              <!-- Timestamp & Status -->
              <div class="flex items-center gap-2 mt-2">
                <p class="text-xs opacity-80">{{ formatTime(msg.created_at) }}</p>
                <span v-if="msg.sender_id === authStore.user?.id" class="text-xs opacity-80">✓✓</span>
              </div>
            </div>

            <!-- Reactions -->
            <div class="flex gap-2 mt-2 flex-wrap" :class="msg.sender_id === authStore.user?.id ? 'justify-end' : ''">
              <!-- Existing Reactions -->
              <button v-for="(count, emoji) in getMessageReactions(msg.id)" :key="emoji"
                      @click="toggleReaction(msg.id, emoji)"
                      class="px-3 py-1 rounded-full text-sm font-medium transition-all shadow-md hover:shadow-lg transform hover:scale-110"
                      :class="hasUserReaction(msg.id, emoji) ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white scale-110' : 'bg-white/90 hover:bg-purple-50 border border-purple-200'">
                {{ emoji }} <span v-if="count > 0">{{ count }}</span>
              </button>
              
              <!-- Add Reaction Button -->
              <div class="relative">
                <button @click="toggleReactionPicker(msg.id)"
                        class="px-3 py-1 rounded-full text-sm font-medium bg-white/90 hover:bg-purple-50 border border-purple-200 transition-all shadow-md hover:shadow-lg transform hover:scale-110">
                  ➕
                </button>
                
                <!-- Quick Reaction Picker -->
                <div v-if="activeReactionPicker === msg.id" class="absolute bottom-full left-0 mb-2 bg-white rounded-xl shadow-xl border p-2 flex gap-2 z-10">
                  <button v-for="emoji in quickReactions" :key="emoji"
                          @click="addQuickReaction(msg.id, emoji)"
                          class="text-2xl hover:scale-125 transition-transform p-1">
                    {{ emoji }}
                  </button>
                </div>
              </div>
              
              <button @click="replyTo(msg)" class="px-3 py-1 rounded-full text-sm font-medium bg-white/90 hover:bg-purple-50 border border-purple-200 transition-all shadow-md hover:shadow-lg transform hover:scale-110">
                ↩️ Reply
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="backdrop-blur-xl border-t shadow-lg p-4 transition-colors duration-300" :class="[themeClasses.input, themeClasses.border]">
        <!-- Reply Banner -->
        <div v-if="replyingTo" class="mb-3 p-3 bg-purple-50 rounded-lg flex items-center justify-between">
          <div>
            <p class="text-xs font-semibold text-purple-700">Replying to {{ replyingTo.sender_name }}</p>
            <p class="text-sm text-gray-600">{{ replyingTo.content }}</p>
          </div>
          <button @click="replyingTo = null" class="text-purple-600 hover:text-purple-800">
            <XMarkIcon class="w-5 h-5" />
          </button>
        </div>

        <!-- File Preview -->
        <div v-if="selectedFile" class="mb-3 p-3 bg-blue-50 rounded-lg flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center text-white">
              {{ getFileIcon(selectedFile.type) }}
            </div>
            <div>
              <p class="text-sm font-medium">{{ selectedFile.name }}</p>
              <p class="text-xs text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
            </div>
          </div>
          <button @click="selectedFile = null" class="text-blue-600 hover:text-blue-800">
            <XMarkIcon class="w-5 h-5" />
          </button>
        </div>

        <!-- Text Formatting Toolbar -->
        <div class="flex items-center gap-2 mb-3 p-3 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border-2 border-purple-200">
          <span class="text-xs font-semibold text-purple-700 mr-2">Format:</span>
          <button @click="toggleBold" 
                  :class="textFormat.bold ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg scale-110' : 'bg-white text-gray-700 hover:bg-purple-100'"
                  class="px-3 py-2 rounded-lg transition-all transform hover:scale-105 border-2 border-purple-300 font-bold">
            B
          </button>
          <button @click="toggleItalic" 
                  :class="textFormat.italic ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg scale-110' : 'bg-white text-gray-700 hover:bg-purple-100'"
                  class="px-3 py-2 rounded-lg transition-all transform hover:scale-105 border-2 border-purple-300 italic">
            I
          </button>
          
          <div class="h-6 w-px bg-purple-300"></div>
          
          <button @click="setFontSize('small')" 
                  :class="textFormat.fontSize === 'small' ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg' : 'bg-white text-gray-700 hover:bg-purple-100'"
                  class="px-3 py-2 rounded-lg text-xs transition-all transform hover:scale-105 border-2 border-purple-300">
            Small
          </button>
          <button @click="setFontSize('normal')" 
                  :class="textFormat.fontSize === 'normal' ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg' : 'bg-white text-gray-700 hover:bg-purple-100'"
                  class="px-3 py-2 rounded-lg text-sm transition-all transform hover:scale-105 border-2 border-purple-300">
            Normal
          </button>
          <button @click="setFontSize('large')" 
                  :class="textFormat.fontSize === 'large' ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg' : 'bg-white text-gray-700 hover:bg-purple-100'"
                  class="px-3 py-2 rounded-lg text-base transition-all transform hover:scale-105 border-2 border-purple-300">
            Large
          </button>
          
          <div class="h-6 w-px bg-purple-300"></div>
          
          <div class="relative">
            <label class="flex items-center gap-2 px-3 py-2 bg-white hover:bg-purple-100 rounded-lg cursor-pointer transition-all border-2 border-purple-300">
              <div class="w-6 h-6 rounded border-2 border-gray-300" :style="{ backgroundColor: textFormat.color }"></div>
              <span class="text-xs font-medium text-gray-700">Color</span>
              <input v-model="textFormat.color" type="color" class="absolute opacity-0 w-0 h-0" />
            </label>
          </div>
        </div>

        <!-- Input -->
        <div class="flex gap-3">
          <div class="relative">
            <button @click="showEmojiPicker = !showEmojiPicker" class="p-3 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-full transition-all">
              <span class="text-2xl">😊</span>
            </button>
            
            <!-- Emoji Picker -->
            <div v-if="showEmojiPicker" class="absolute bottom-full left-0 mb-2 z-20">
              <div class="bg-white rounded-xl shadow-2xl border">
                <emoji-picker @emoji-click="insertEmoji" class="emoji-picker-custom"></emoji-picker>
              </div>
            </div>
          </div>
          
          <div class="relative">
            <button @click="showFileMenu = !showFileMenu" class="p-3 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-all">
              <PaperClipIcon class="w-6 h-6" />
            </button>
            
            <!-- File Type Menu -->
            <div v-if="showFileMenu" class="absolute bottom-full left-0 mb-2 bg-white rounded-xl shadow-lg border p-2 min-w-48 z-10">
              <button @click="selectFileType('image')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-blue-50 rounded-lg text-left transition-all">
                <span class="text-2xl">🖼️</span>
                <span class="text-sm font-medium text-gray-700">Image</span>
              </button>
              <button @click="selectFileType('video')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-purple-50 rounded-lg text-left transition-all">
                <span class="text-2xl">🎥</span>
                <span class="text-sm font-medium text-gray-700">Video</span>
              </button>
              <button @click="selectFileType('audio')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-green-50 rounded-lg text-left transition-all">
                <span class="text-2xl">🎵</span>
                <span class="text-sm font-medium text-gray-700">Audio</span>
              </button>
              <button @click="selectFileType('document')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-yellow-50 rounded-lg text-left transition-all">
                <span class="text-2xl">📄</span>
                <span class="text-sm font-medium text-gray-700">Document</span>
              </button>
              <button @click="selectFileType('zip')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-orange-50 rounded-lg text-left transition-all">
                <span class="text-2xl">📦</span>
                <span class="text-sm font-medium text-gray-700">Archive</span>
              </button>
              <button @click="selectFileType('any')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-50 rounded-lg text-left transition-all">
                <span class="text-2xl">📎</span>
                <span class="text-sm font-medium text-gray-700">Any File</span>
              </button>
            </div>
          </div>
          <input v-model="newMessage"
                 @keyup.enter="sendMessage"
                 @input="handleTyping"
                 type="text"
                 placeholder="Type a message..."
                 :style="getFormattedStyle()"
                 class="flex-1 px-4 py-3 border-2 border-purple-200 rounded-full focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all" />
          <button @click="sendMessage"
                  :disabled="(!newMessage.trim() && !selectedFile) || sending"
                  class="px-6 py-3 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white rounded-full hover:from-indigo-600 hover:via-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl transform hover:scale-110">
            <PaperAirplaneIcon v-if="!sending" class="w-5 h-5" />
            <div v-else class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          </button>
        </div>

        <!-- Hidden File Input -->
        <input ref="fileInput" type="file" class="hidden" @change="handleFileSelect" accept="*/*" />

        <!-- Typing Indicator -->
        <div v-if="typingUsers.length > 0" class="mt-2 flex items-center gap-2">
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
            <div class="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
          </div>
          <span class="text-xs text-purple-600 font-medium">
            {{ typingUsers.length === 1 ? typingUsers[0] : `${typingUsers.length} people` }} typing...
          </span>
        </div>
      </div>
    </div>
  </div>

  <!-- Theme Menu (Teleported) -->
  <Teleport to="body">
    <div v-if="showThemeMenu" class="fixed inset-0 z-[9999]" @click="showThemeMenu = false">
      <div class="fixed top-20 right-4 w-72 bg-white rounded-2xl shadow-2xl border-2 border-purple-200 p-4" @click.stop>
        <h3 class="font-bold text-gray-900 mb-3 flex items-center gap-2">
          <span class="text-xl">🎨</span>
          Choose Your Theme
        </h3>
        <div class="space-y-2">
          <button @click="changeTheme('light')"
                  class="w-full p-3 rounded-xl flex items-center gap-3 transition-all transform hover:scale-105 bg-gradient-to-r from-gray-100 to-gray-200 hover:from-gray-200 hover:to-gray-300"
                  :class="currentTheme === 'light' ? 'ring-2 ring-purple-500 ring-offset-2' : ''">
            <span class="text-2xl">☀️</span>
            <div class="flex-1 text-left">
              <p class="font-semibold text-sm text-gray-900">Light Mode</p>
              <p class="text-xs text-gray-600">Clean & bright</p>
            </div>
            <CheckIcon v-if="currentTheme === 'light'" class="w-5 h-5 text-purple-500" />
          </button>
          
          <button @click="changeTheme('dark')"
                  class="w-full p-3 rounded-xl flex items-center gap-3 transition-all transform hover:scale-105 bg-gradient-to-r from-gray-800 to-gray-900 text-white hover:from-gray-700 hover:to-gray-800"
                  :class="currentTheme === 'dark' ? 'ring-2 ring-purple-500 ring-offset-2' : ''">
            <span class="text-2xl">🌙</span>
            <div class="flex-1 text-left">
              <p class="font-semibold text-sm">Dark Mode</p>
              <p class="text-xs opacity-75">Easy on eyes</p>
            </div>
            <CheckIcon v-if="currentTheme === 'dark'" class="w-5 h-5" />
          </button>
          
          <button @click="changeTheme('vibrant')"
                  class="w-full p-3 rounded-xl flex items-center gap-3 transition-all transform hover:scale-105 bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600"
                  :class="currentTheme === 'vibrant' ? 'ring-2 ring-purple-500 ring-offset-2' : ''">
            <span class="text-2xl">🎨</span>
            <div class="flex-1 text-left">
              <p class="font-semibold text-sm">Vibrant</p>
              <p class="text-xs opacity-75">Colorful & fun</p>
            </div>
            <CheckIcon v-if="currentTheme === 'vibrant'" class="w-5 h-5" />
          </button>
          
          <button @click="changeTheme('ocean')"
                  class="w-full p-3 rounded-xl flex items-center gap-3 transition-all transform hover:scale-105 bg-gradient-to-r from-blue-500 to-cyan-500 text-white hover:from-blue-600 hover:to-cyan-600"
                  :class="currentTheme === 'ocean' ? 'ring-2 ring-purple-500 ring-offset-2' : ''">
            <span class="text-2xl">🌊</span>
            <div class="flex-1 text-left">
              <p class="font-semibold text-sm">Ocean</p>
              <p class="text-xs opacity-75">Cool & calm</p>
            </div>
            <CheckIcon v-if="currentTheme === 'ocean'" class="w-5 h-5" />
          </button>
          
          <button @click="changeTheme('sunset')"
                  class="w-full p-3 rounded-xl flex items-center gap-3 transition-all transform hover:scale-105 bg-gradient-to-r from-orange-500 to-red-500 text-white hover:from-orange-600 hover:to-red-600"
                  :class="currentTheme === 'sunset' ? 'ring-2 ring-purple-500 ring-offset-2' : ''">
            <span class="text-2xl">🌅</span>
            <div class="flex-1 text-left">
              <p class="font-semibold text-sm">Sunset</p>
              <p class="text-xs opacity-75">Warm & cozy</p>
            </div>
            <CheckIcon v-if="currentTheme === 'sunset'" class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  </Teleport>

  <!-- Modern Image Modal -->
  <div v-if="imageModal.show" class="fixed inset-0 bg-black/95 z-50 flex flex-col" @click="closeImageModal">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 bg-black/50 backdrop-blur-sm" @click.stop>
      <div class="text-white">
        <p class="font-medium">{{ imageModal.fileName || 'Image' }}</p>
        <p class="text-sm text-gray-300">{{ formatFileSize(imageModal.fileSize) }}</p>
      </div>
      <button @click="closeImageModal" class="text-white hover:bg-white/10 p-2 rounded-full transition-all">
        <XMarkIcon class="w-6 h-6" />
      </button>
    </div>

    <!-- Image -->
    <div class="flex-1 flex items-center justify-center p-4" @click.stop>
      <img :src="imageModal.url" class="max-h-full max-w-full object-contain rounded-lg" />
    </div>

    <!-- Action Bar -->
    <div class="bg-white p-4" @click.stop>
      <div class="max-w-4xl mx-auto grid grid-cols-3 gap-4">
        <button @click="downloadImage" class="flex flex-col items-center gap-2 p-3 hover:bg-gray-100 rounded-xl transition-all">
          <div class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white">
            <ArrowDownTrayIcon class="w-6 h-6" />
          </div>
          <span class="text-xs font-medium text-gray-700">Download</span>
        </button>

        <button @click="copyImageLink" class="flex flex-col items-center gap-2 p-3 hover:bg-gray-100 rounded-xl transition-all">
          <div class="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center text-white">
            <ClipboardDocumentIcon class="w-6 h-6" />
          </div>
          <span class="text-xs font-medium text-gray-700">Copy Link</span>
        </button>

        <button @click="showForwardMenu = true" class="flex flex-col items-center gap-2 p-3 hover:bg-gray-100 rounded-xl transition-all">
          <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-white">
            <ShareIcon class="w-6 h-6" />
          </div>
          <span class="text-xs font-medium text-gray-700">Forward</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Pending Messages Modal -->
  <div v-if="showPendingMessages" class="fixed inset-0 bg-black/50 z-[60] flex items-center justify-center p-4" @click="showPendingMessages = false">
    <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden" @click.stop>
      <div class="p-4 border-b bg-orange-50">
        <h3 class="text-lg font-bold text-orange-700">Pending Messages ({{ pendingCount }})</h3>
        <p class="text-sm text-gray-600">Review and approve student messages for announcements</p>
      </div>
      <div class="overflow-y-auto max-h-96 p-4 space-y-3">
        <div v-if="pendingMessages.length === 0" class="text-center py-8 text-gray-400">
          <p>No pending messages</p>
        </div>
        <div v-else v-for="msg in pendingMessages" :key="msg.id"
             class="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <div class="flex items-start justify-between mb-2">
            <div>
              <p class="font-semibold text-gray-900">{{ msg.sender_name }}</p>
              <p class="text-xs text-gray-500">{{ msg.channel_name }} • {{ formatTime(msg.created_at) }}</p>
            </div>
          </div>
          <p class="text-sm text-gray-700 mb-3">{{ msg.content }}</p>
          <div class="flex gap-2">
            <button @click="approveMessage(msg.id)"
                    class="flex-1 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-all">
              ✓ Approve
            </button>
            <button @click="rejectMessage(msg.id)"
                    class="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-all">
              ✗ Reject
            </button>
          </div>
        </div>
      </div>
      <div class="p-4 border-t">
        <button @click="showPendingMessages = false" class="w-full py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-all">
          Close
        </button>
      </div>
    </div>
  </div>

  <!-- Live Session Menu -->
  <div v-if="showLiveMenu" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[60] flex items-center justify-center p-4" @click="showLiveMenu = false">
    <div class="bg-white rounded-3xl max-w-md w-full shadow-2xl transform transition-all" @click.stop>
      <div class="p-6 bg-gradient-to-r from-red-500 via-pink-500 to-purple-500 rounded-t-3xl">
        <h3 class="text-2xl font-bold text-white flex items-center gap-2">
          <span class="text-3xl">🎬</span>
          Start Live Session
        </h3>
        <p class="text-sm text-white/90 mt-1">Connect with your class in real-time</p>
      </div>
      
      <!-- Active Session -->
      <div v-if="activeLiveSession" class="p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-b-2 border-green-200">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-3">
            <div class="relative">
              <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center">
                <span class="text-white text-xl">▶️</span>
              </div>
              <div class="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full animate-ping"></div>
            </div>
            <div>
              <p class="font-bold text-green-800">{{ activeLiveSession.title }}</p>
              <p class="text-xs text-green-600 flex items-center gap-1">
                <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                {{ activeLiveSession.type }} • Active Now
              </p>
            </div>
          </div>
        </div>
        <button @click="joinLiveSession(activeLiveSession)" 
                class="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold rounded-xl hover:from-green-600 hover:to-emerald-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105">
          🚀 Join Active Session
        </button>
      </div>
      
      <!-- Start New Session -->
      <div v-else class="p-6 space-y-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Session Title</label>
          <input v-model="liveSessionTitle" 
                 type="text" 
                 placeholder="e.g., Mathematics Class, Science Lab" 
                 class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all" />
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-3">Session Type</label>
        </div>
        
        <button @click="requestLiveSession('AUDIO')" 
                class="w-full flex items-center gap-4 p-5 bg-gradient-to-br from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 rounded-2xl transition-all border-2 border-blue-200 hover:border-blue-400 hover:shadow-lg transform hover:scale-105 group">
          <div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-2xl flex items-center justify-center text-white text-3xl shadow-lg group-hover:shadow-xl">
            🎤
          </div>
          <div class="text-left flex-1">
            <p class="font-bold text-gray-800 text-lg">Audio Only</p>
            <p class="text-sm text-gray-600">Voice conversation • Lower bandwidth</p>
          </div>
          <svg class="w-6 h-6 text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <button @click="requestLiveSession('VIDEO')" 
                class="w-full flex items-center gap-4 p-5 bg-gradient-to-br from-purple-50 to-pink-50 hover:from-purple-100 hover:to-pink-100 rounded-2xl transition-all border-2 border-purple-200 hover:border-purple-400 hover:shadow-lg transform hover:scale-105 group">
          <div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center text-white text-3xl shadow-lg group-hover:shadow-xl">
            🎥
          </div>
          <div class="text-left flex-1">
            <p class="font-bold text-gray-800 text-lg">Video Call</p>
            <p class="text-sm text-gray-600">Video + audio • Full experience</p>
          </div>
          <svg class="w-6 h-6 text-purple-500 opacity-0 group-hover:opacity-100 transition-opacity" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      
      <div class="p-6 border-t bg-gray-50 rounded-b-3xl">
        <button @click="showLiveMenu = false" class="w-full py-3 text-gray-600 hover:bg-white font-medium rounded-xl transition-all border-2 border-transparent hover:border-gray-300">
          Cancel
        </button>
      </div>
    </div>
  </div>

  <!-- Pending Live Sessions (Teacher) -->
  <div v-if="showPendingLive" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[60] flex items-center justify-center p-4" @click="showPendingLive = false">
    <div class="bg-white rounded-3xl max-w-2xl w-full max-h-[80vh] overflow-hidden shadow-2xl" @click.stop>
      <div class="p-6 bg-gradient-to-r from-purple-500 via-pink-500 to-red-500">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-2xl font-bold text-white flex items-center gap-2">
              <span class="text-3xl">📸</span>
              Live Requests
            </h3>
            <p class="text-sm text-white/90 mt-1">{{ pendingLiveCount }} pending approval</p>
          </div>
          <div class="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
            <span class="text-2xl font-bold text-white">{{ pendingLiveCount }}</span>
          </div>
        </div>
      </div>
      <div class="overflow-y-auto max-h-96 p-6 space-y-4 bg-gradient-to-b from-gray-50 to-white">
        <div v-if="pendingLiveSessions.length === 0" class="text-center py-12">
          <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span class="text-4xl">✅</span>
          </div>
          <p class="text-gray-500 font-medium">No pending requests</p>
          <p class="text-sm text-gray-400 mt-1">All caught up!</p>
        </div>
        <div v-else v-for="session in pendingLiveSessions" :key="session.id"
             class="bg-white rounded-2xl p-5 border-2 border-purple-100 hover:border-purple-300 shadow-md hover:shadow-xl transition-all">
          <div class="flex items-start gap-4 mb-4">
            <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center text-white text-2xl flex-shrink-0 shadow-lg">
              {{ session.type === 'VIDEO' ? '🎥' : '🎤' }}
            </div>
            <div class="flex-1">
              <p class="font-bold text-gray-900 text-lg">{{ session.title }}</p>
              <div class="flex items-center gap-2 mt-1 text-sm text-gray-600">
                <span class="px-2 py-0.5 bg-purple-100 text-purple-700 rounded-full text-xs font-semibold">{{ session.type }}</span>
                <span>•</span>
                <span>{{ session.host_name }}</span>
                <span>•</span>
                <span>{{ session.channel_name }}</span>
              </div>
            </div>
          </div>
          <div class="flex gap-3">
            <button @click="approveLiveSession(session.id)"
                    class="flex-1 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold rounded-xl hover:from-green-600 hover:to-emerald-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 flex items-center justify-center gap-2">
              <CheckIcon class="w-5 h-5" />
              Approve
            </button>
            <button @click="rejectLiveSession(session.id)"
                    class="flex-1 px-6 py-3 bg-gradient-to-r from-red-500 to-pink-500 text-white font-bold rounded-xl hover:from-red-600 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 flex items-center justify-center gap-2">
              <XMarkIcon class="w-5 h-5" />
              Reject
            </button>
          </div>
        </div>
      </div>
      <div class="p-6 border-t bg-gray-50 rounded-b-3xl">
        <button @click="showPendingLive = false" class="w-full py-3 text-gray-600 hover:bg-white font-medium rounded-xl transition-all border-2 border-transparent hover:border-gray-300">
          Close
        </button>
      </div>
    </div>
  </div>

  <!-- Live Session Component -->
  <LiveSession v-if="currentLiveSession" 
               :session="currentLiveSession" 
               :room-id="currentLiveSession.room_id"
               @close="leaveLiveSession"
               @ended="endLiveSession" />

  <!-- Forward Menu -->
  <div v-if="showForwardMenu" class="fixed inset-0 bg-black/50 z-[60] flex items-center justify-center p-4" @click="showForwardMenu = false">
    <div class="bg-white rounded-2xl max-w-md w-full max-h-[80vh] overflow-hidden" @click.stop>
      <div class="p-4 border-b">
        <h3 class="text-lg font-bold">Forward to Channel</h3>
      </div>
      <div class="overflow-y-auto max-h-96">
        <button v-for="channel in channels" :key="channel.id"
                @click="forwardToChannel(channel)"
                class="w-full flex items-center gap-3 p-4 hover:bg-gray-50 transition-all">
          <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
            #
          </div>
          <span class="font-medium">{{ channel.name }}</span>
        </button>
      </div>
      <div class="p-4 border-t">
        <button @click="showForwardMenu = false" class="w-full py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-all">
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ThemeSwitcher from '../components/ThemeSwitcher.vue'
import LiveSession from '../components/LiveSession.vue'
import api from '../utils/api'
import 'emoji-picker-element'
import {
  ChevronLeftIcon,
  VideoCameraIcon,
  MicrophoneIcon,
  PaperAirplaneIcon,
  PaperClipIcon,
  FaceSmileIcon,
  XMarkIcon,
  ArrowDownTrayIcon,
  ShareIcon,
  ArrowUturnLeftIcon,
  PlusIcon,
  CheckIcon,
  ChatBubbleLeftRightIcon,
  PaintBrushIcon,
  PhotoIcon,
  MusicalNoteIcon,
  DocumentIcon,
  ArchiveBoxIcon,
  ClipboardDocumentIcon
} from '@heroicons/vue/24/outline'
import { PlayIcon } from '@heroicons/vue/24/solid'

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
const typingUsers = ref([])
const typingTimeout = ref(null)
const showFormatMenu = ref(false)
const showThemeMenu = ref(false)
const textFormat = ref({
  bold: false,
  italic: false,
  color: '#000000',
  fontSize: 'normal'
})

function changeTheme(theme) {
  currentTheme.value = theme
  localStorage.setItem('chat-theme', theme)
  document.documentElement.setAttribute('data-theme', theme)
  showThemeMenu.value = false
}
const selectedFile = ref(null)
const fileInput = ref(null)
const showFileMenu = ref(false)
const showForwardMenu = ref(false)
const showPendingMessages = ref(false)
const pendingMessages = ref([])
const pendingCount = ref(0)
const showEmojiPicker = ref(false)
const activeReactionPicker = ref(null)
const quickReactions = ['👍', '❤️', '😂', '😮', '😢', '🙏', '🎉', '🔥']
const showLiveMenu = ref(false)
const showPendingLive = ref(false)
const liveSessionTitle = ref('')
const activeLiveSession = ref(null)
const currentLiveSession = ref(null)
const pendingLiveSessions = ref([])
const pendingLiveCount = ref(0)
const imageModal = ref({
  show: false,
  url: '',
  fileName: '',
  fileSize: 0
})

const currentTheme = ref('light')
const themeClasses = computed(() => {
  const themes = {
    light: {
      background: 'bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50',
      sidebar: 'bg-white/80',
      header: 'bg-white/80',
      messages: 'bg-gradient-to-br from-indigo-50/30 via-purple-50/30 to-pink-50/30',
      input: 'bg-white/80',
      border: 'border-white/20',
      text: 'text-gray-900',
      textSecondary: 'text-gray-600'
    },
    dark: {
      background: 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900',
      sidebar: 'bg-gray-800/80',
      header: 'bg-gray-800/80',
      messages: 'bg-gradient-to-br from-gray-900/30 via-gray-800/30 to-gray-900/30',
      input: 'bg-gray-800/80',
      border: 'border-gray-700/20',
      text: 'text-white',
      textSecondary: 'text-gray-300'
    },
    vibrant: {
      background: 'bg-gradient-to-br from-purple-600 via-pink-600 to-purple-700',
      sidebar: 'bg-purple-900/40',
      header: 'bg-purple-900/40',
      messages: 'bg-gradient-to-br from-purple-900/20 via-pink-900/20 to-purple-900/20',
      input: 'bg-purple-900/40',
      border: 'border-purple-400/20',
      text: 'text-white',
      textSecondary: 'text-purple-100'
    },
    ocean: {
      background: 'bg-gradient-to-br from-blue-600 via-cyan-600 to-blue-700',
      sidebar: 'bg-blue-900/40',
      header: 'bg-blue-900/40',
      messages: 'bg-gradient-to-br from-blue-900/20 via-cyan-900/20 to-blue-900/20',
      input: 'bg-blue-900/40',
      border: 'border-blue-400/20',
      text: 'text-white',
      textSecondary: 'text-blue-100'
    },
    sunset: {
      background: 'bg-gradient-to-br from-orange-600 via-red-600 to-orange-700',
      sidebar: 'bg-orange-900/40',
      header: 'bg-orange-900/40',
      messages: 'bg-gradient-to-br from-orange-900/20 via-red-900/20 to-orange-900/20',
      input: 'bg-orange-900/40',
      border: 'border-orange-400/20',
      text: 'text-white',
      textSecondary: 'text-orange-100'
    }
  }
  return themes[currentTheme.value] || themes.light
})

let messagePolling = null
let reactionPolling = null
let liveSessionPolling = null
let channelPolling = null

const onlineCount = computed(() => Math.floor(Math.random() * 5) + 3)

async function loadGroup() {
  const res = await api.get(`/directory/groups/${groupId.value}`)
  group.value = res.data
}

async function loadChannels() {
  const res = await api.get(`/directory/groups/${groupId.value}/channels`)
  channels.value = res.data
  if (channels.value.length > 0 && !activeChannelId.value) {
    const accessibleChannel = channels.value.find(c => c.can_access)
    if (accessibleChannel) {
      selectChannel(accessibleChannel)
    }
  }
}

async function selectChannel(channel) {
  activeChannelId.value = channel.id
  activeChannel.value = channel
  loadingMessages.value = true
  
  // Stop old polling
  if (messagePolling) clearInterval(messagePolling)
  if (reactionPolling) clearInterval(reactionPolling)
  if (liveSessionPolling) clearInterval(liveSessionPolling)
  
  // Clear messages when switching channels
  messages.value = []
  
  await loadMessages()
  await loadReactions()
  await loadLiveSessions()
  
  // Start new polling - every 1 second for real-time
  messagePolling = setInterval(loadMessages, 1000)
  reactionPolling = setInterval(loadReactions, 2000)
  liveSessionPolling = setInterval(async () => {
    await loadLiveSessions()
    if (authStore.user?.role === 'TEACHER') {
      await loadPendingLiveSessions()
    }
  }, 3000)
  
  loadingMessages.value = false
}

async function loadMessages() {
  if (!activeChannelId.value) return
  
  try {
    const res = await api.get(`/simple-chat/channels/${activeChannelId.value}/messages`)
    const newMsgs = res.data.messages || res.data || []
    
    // Always update messages to ensure correct channel data
    const wasAtBottom = isScrolledToBottom()
    messages.value = newMsgs
    if (wasAtBottom) {
      await nextTick()
      scrollToBottom()
    }
    
    // Load pending count for teachers in announcement channels
    if (authStore.user?.role === 'TEACHER' && activeChannel.value?.type === 'ANNOUNCEMENTS') {
      await loadPendingCount()
    }
  } catch (err) {
    console.error('Load messages failed:', err)
  }
}

async function loadPendingCount() {
  try {
    const res = await api.get('/simple-chat/pending-messages')
    pendingCount.value = res.data.count || 0
  } catch (err) {
    console.error('Load pending count failed:', err)
  }
}

async function loadPendingMessages() {
  try {
    const res = await api.get('/simple-chat/pending-messages')
    pendingMessages.value = res.data.pending || []
    pendingCount.value = res.data.count || 0
  } catch (err) {
    console.error('Load pending messages failed:', err)
  }
}

async function approveMessage(messageId) {
  try {
    await api.post(`/simple-chat/approve-message/${messageId}`)
    showNotification('Message approved', 'success')
    await loadPendingMessages()
    await loadMessages()
  } catch (err) {
    console.error('Approve failed:', err)
    showNotification('Failed to approve message', 'error')
  }
}

async function rejectMessage(messageId) {
  try {
    await api.post(`/simple-chat/reject-message/${messageId}`)
    showNotification('Message rejected', 'success')
    await loadPendingMessages()
  } catch (err) {
    console.error('Reject failed:', err)
    showNotification('Failed to reject message', 'error')
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
  if ((!newMessage.value.trim() && !selectedFile.value) || sending.value) return
  
  sending.value = true
  const content = newMessage.value.trim()
  
  // Store formatting for this message
  const messageFormat = { ...textFormat.value }
  
  newMessage.value = ''
  
  try {
    const formData = new FormData()
    if (content) {
      formData.append('content', content)
      // Store formatting as JSON in a custom field
      formData.append('format', JSON.stringify(messageFormat))
    }
    if (replyingTo.value) formData.append('reply_to_id', replyingTo.value.id)
    if (selectedFile.value) formData.append('file', selectedFile.value)
    
    const response = await api.post(`/simple-chat/channels/${activeChannelId.value}/messages`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    // Check if message needs approval
    if (response.data.needs_approval) {
      showNotification('Message sent for teacher approval', 'info')
    }
    
    replyingTo.value = null
    selectedFile.value = null
    
    // Immediately reload messages
    await loadMessages()
    scrollToBottom()
  } catch (err) {
    console.error('Send failed:', err)
    newMessage.value = content
    showNotification('Failed to send message', 'error')
  } finally {
    sending.value = false
  }
}

function selectFileType(type) {
  showFileMenu.value = false
  
  const acceptTypes = {
    image: 'image/*',
    video: 'video/*',
    audio: 'audio/*',
    document: '.pdf,.doc,.docx,.txt,.rtf,.ppt,.pptx,.xls,.xlsx',
    zip: '.zip,.rar,.7z,.tar,.gz',
    any: '*/*'
  }
  
  if (fileInput.value) {
    fileInput.value.accept = acceptTypes[type] || '*/*'
    fileInput.value.click()
  }
}

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  
  const maxSize = 50 * 1024 * 1024 // 50MB
  if (file.size > maxSize) {
    alert('File too large! Maximum size is 50MB')
    return
  }
  
  selectedFile.value = file
  event.target.value = '' // Reset input
}

function getFileIcon(fileType) {
  if (!fileType) return '📄'
  if (fileType.startsWith('image/')) return '🖼️'
  if (fileType.startsWith('video/')) return '🎥'
  if (fileType.startsWith('audio/')) return '🎵'
  if (fileType.includes('pdf')) return '📕'
  if (fileType.includes('word') || fileType.includes('document')) return '📘'
  if (fileType.includes('excel') || fileType.includes('spreadsheet')) return '📗'
  if (fileType.includes('zip') || fileType.includes('rar')) return '📦'
  return '📄'
}

function formatFileSize(bytes) {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

function insertEmoji(event) {
  const emoji = event.detail.unicode
  newMessage.value += emoji
  showEmojiPicker.value = false
}

function toggleReactionPicker(messageId) {
  activeReactionPicker.value = activeReactionPicker.value === messageId ? null : messageId
}

async function addQuickReaction(messageId, emoji) {
  await toggleReaction(messageId, emoji)
  activeReactionPicker.value = null
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
  
  // Map old format to new
  if (msgReactions.likes > 0) result['👍'] = msgReactions.likes
  if (msgReactions.loves > 0) result['❤️'] = msgReactions.loves
  
  // Add any other emojis from reactions
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

function replyTo(msg) {
  replyingTo.value = msg
}

function handleTyping() {
  // Simulate typing indicator (in production, use WebSocket)
  if (newMessage.value.length > 0) {
    // Show typing for other users
    if (Math.random() > 0.7 && typingUsers.value.length === 0) {
      typingUsers.value = ['Student typing...']
    }
  }
  
  if (typingTimeout.value) clearTimeout(typingTimeout.value)
  typingTimeout.value = setTimeout(() => {
    typingUsers.value = []
  }, 2000)
}

function toggleBold() {
  textFormat.value.bold = !textFormat.value.bold
}

function toggleItalic() {
  textFormat.value.italic = !textFormat.value.italic
}

function setFontSize(size) {
  textFormat.value.fontSize = size
}

function applyFormatting(text) {
  let formatted = text
  if (textFormat.value.bold) formatted = `**${formatted}**`
  if (textFormat.value.italic) formatted = `*${formatted}*`
  return formatted
}

function getFormattedStyle() {
  return {
    fontWeight: textFormat.value.bold ? 'bold' : 'normal',
    fontStyle: textFormat.value.italic ? 'italic' : 'normal',
    color: textFormat.value.color,
    fontSize: textFormat.value.fontSize === 'large' ? '1.125rem' : textFormat.value.fontSize === 'small' ? '0.875rem' : '1rem'
  }
}

function getMessageStyle(msg) {
  // Check if message has stored format data
  if (msg.format_data) {
    try {
      const format = typeof msg.format_data === 'string' ? JSON.parse(msg.format_data) : msg.format_data
      if (format && format.textFormat) {
        return {
          fontWeight: format.textFormat.bold ? 'bold' : 'normal',
          fontStyle: format.textFormat.italic ? 'italic' : 'normal',
          color: format.textFormat.color || 'inherit',
          fontSize: format.textFormat.fontSize === 'large' ? '1.125rem' : format.textFormat.fontSize === 'small' ? '0.875rem' : '1rem'
        }
      }
    } catch (e) {
      console.error('Error parsing message format:', e)
    }
  }
  
  // Default style
  return {
    fontWeight: 'normal',
    fontStyle: 'normal',
    fontSize: '1rem'
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

function getFullFileUrl(fileUrl) {
  if (!fileUrl) return ''
  if (fileUrl.startsWith('http')) return fileUrl
  return `http://localhost:8080${fileUrl}`
}

function openImageModal(url, fileName = '', fileSize = 0) {
  imageModal.value = {
    show: true,
    url,
    fileName,
    fileSize
  }
}

function closeImageModal() {
  imageModal.value.show = false
}

async function downloadImage() {
  try {
    const response = await fetch(imageModal.value.url)
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = imageModal.value.fileName || 'image.jpg'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    showNotification('Image downloaded!', 'success')
  } catch (err) {
    console.error('Download failed:', err)
    showNotification('Download failed', 'error')
  }
}

async function shareImage() {
  try {
    if (navigator.share) {
      await navigator.share({
        title: 'Share Image',
        text: 'Check out this image!',
        url: imageModal.value.url
      })
      showNotification('Shared successfully!', 'success')
    } else {
      await copyImageLink()
    }
  } catch (err) {
    if (err.name !== 'AbortError') {
      console.error('Share failed:', err)
      await copyImageLink()
    }
  }
}

async function forwardToChannel(channel) {
  try {
    // Fetch the image as blob
    const response = await fetch(imageModal.value.url)
    const blob = await response.blob()
    const file = new File([blob], imageModal.value.fileName || 'image.jpg', { type: blob.type })
    
    const formData = new FormData()
    formData.append('content', `Forwarded image: ${imageModal.value.fileName || 'image'}`)
    formData.append('file', file)
    
    await api.post(`/simple-chat/channels/${channel.id}/messages`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    showNotification(`Forwarded to #${channel.name}`, 'success')
    showForwardMenu.value = false
    closeImageModal()
  } catch (err) {
    console.error('Forward failed:', err)
    showNotification('Forward failed', 'error')
  }
}

async function copyImageLink() {
  try {
    await navigator.clipboard.writeText(imageModal.value.url)
    showNotification('Link copied to clipboard!', 'success')
  } catch (err) {
    // Fallback for older browsers
    const textArea = document.createElement('textarea')
    textArea.value = imageModal.value.url
    textArea.style.position = 'fixed'
    textArea.style.left = '-999999px'
    document.body.appendChild(textArea)
    textArea.select()
    try {
      document.execCommand('copy')
      showNotification('Link copied to clipboard!', 'success')
    } catch (err2) {
      showNotification('Failed to copy link', 'error')
    }
    document.body.removeChild(textArea)
  }
}

async function requestLiveSession(type) {
  if (!liveSessionTitle.value.trim()) {
    showNotification('Please enter a session title', 'error')
    return
  }
  
  try {
    const res = await api.post('/live-sessions/request', {
      channel_id: activeChannelId.value,
      type: type,
      title: liveSessionTitle.value
    })
    
    if (res.data.needs_approval) {
      showNotification('Live session request sent to teacher', 'info')
    } else {
      showNotification('Live session approved! Starting...', 'success')
      await startLiveSession(res.data.session_id)
    }
    
    showLiveMenu.value = false
    liveSessionTitle.value = ''
    await loadLiveSessions()
  } catch (err) {
    console.error('Request live session failed:', err)
    showNotification(err.response?.data?.detail || 'Failed to request live session', 'error')
  }
}

async function loadLiveSessions() {
  if (!activeChannelId.value) return
  
  try {
    const res = await api.get(`/live-sessions/channel/${activeChannelId.value}`)
    const sessions = res.data.sessions || []
    
    // Find active session
    activeLiveSession.value = sessions.find(s => s.status === 'ACTIVE')
    
    // Load pending count for teachers
    if (authStore.user?.role === 'TEACHER') {
      await loadPendingLiveSessions()
    }
  } catch (err) {
    console.error('Load live sessions failed:', err)
  }
}

async function loadPendingLiveSessions() {
  try {
    const res = await api.get('/live-sessions/pending')
    pendingLiveSessions.value = res.data.pending || []
    pendingLiveCount.value = res.data.count || 0
    console.log('Pending live sessions:', pendingLiveCount.value, pendingLiveSessions.value)
  } catch (err) {
    console.error('Load pending live sessions failed:', err)
  }
}

async function approveLiveSession(sessionId) {
  try {
    await api.post(`/live-sessions/${sessionId}/approve`)
    showNotification('Live session approved! Starting...', 'success')
    await loadPendingLiveSessions()
    await loadLiveSessions()
    
    // Auto-start the approved session
    await startLiveSession(sessionId)
    showPendingLive.value = false
  } catch (err) {
    console.error('Approve failed:', err)
    showNotification('Failed to approve session', 'error')
  }
}

async function rejectLiveSession(sessionId) {
  try {
    await api.post(`/live-sessions/${sessionId}/reject`)
    showNotification('Live session rejected', 'success')
    await loadPendingLiveSessions()
  } catch (err) {
    console.error('Reject failed:', err)
    showNotification('Failed to reject session', 'error')
  }
}

async function startLiveSession(sessionId) {
  try {
    const res = await api.post(`/live-sessions/${sessionId}/start`)
    await loadLiveSessions()
    
    // Auto-join the session after starting
    if (activeLiveSession.value) {
      await joinLiveSession(activeLiveSession.value)
    }
  } catch (err) {
    console.error('Start session failed:', err)
    showNotification('Failed to start session', 'error')
  }
}

async function joinLiveSession(session) {
  currentLiveSession.value = session
  showLiveMenu.value = false
}

async function leaveLiveSession() {
  if (currentLiveSession.value) {
    await endLiveSession()
  }
  currentLiveSession.value = null
}

async function endLiveSession() {
  if (currentLiveSession.value) {
    try {
      await api.post(`/live-sessions/${currentLiveSession.value.id}/end`)
      showNotification('Live session ended', 'success')
      currentLiveSession.value = null
      await loadLiveSessions()
    } catch (err) {
      console.error('End session failed:', err)
      showNotification('Failed to end session', 'error')
    }
  }
}

async function cleanupSessions() {
  if (!confirm('End all active live sessions?')) return
  
  try {
    const res = await api.delete('/live-sessions/cleanup')
    showNotification(`Cleaned up ${res.data.cleaned} sessions`, 'success')
    currentLiveSession.value = null
    await loadLiveSessions()
  } catch (err) {
    console.error('Cleanup failed:', err)
    showNotification('Failed to cleanup sessions', 'error')
  }
}

function showNotification(message, type = 'info') {
  const notification = document.createElement('div')
  const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500'
  notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all`
  notification.textContent = message
  document.body.appendChild(notification)
  
  setTimeout(() => {
    if (document.body.contains(notification)) {
      document.body.removeChild(notification)
    }
  }, 3000)
}

function showAccessDenied() {
  showNotification('🔒 Access denied. Only the module creator can access this chat.', 'error')
}

function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
}

// Watch for route changes to reload channels
watch(() => route.params.groupId, async (newId, oldId) => {
  if (newId && newId !== oldId) {
    groupId.value = parseInt(newId)
    await loadGroup()
    await loadChannels()
  }
})

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  // Load theme
  const savedTheme = localStorage.getItem('chat-theme') || 'light'
  currentTheme.value = savedTheme
  
  // Watch for theme changes
  const observer = new MutationObserver(() => {
    const theme = document.documentElement.getAttribute('data-theme') || 'light'
    currentTheme.value = theme
  })
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] })
  
  await loadGroup()
  await loadChannels()
  
  // Poll channels every 3 seconds to detect new modules
  channelPolling = setInterval(loadChannels, 3000)
  
  // Load pending items for teachers
  if (authStore.user?.role === 'TEACHER') {
    await loadPendingMessages()
    await loadPendingLiveSessions()
  }
})

onUnmounted(() => {
  if (messagePolling) clearInterval(messagePolling)
  if (reactionPolling) clearInterval(reactionPolling)
  if (liveSessionPolling) clearInterval(liveSessionPolling)
  if (channelPolling) clearInterval(channelPolling)
})
</script>

<style>
.emoji-picker-custom {
  --border-radius: 12px;
  --border-color: #e5e7eb;
  --category-emoji-size: 1.5rem;
  --emoji-size: 1.75rem;
  --indicator-color: #3b82f6;
  --input-border-color: #e5e7eb;
  --input-border-radius: 8px;
  --input-padding: 8px;
  --num-columns: 8;
  --outline-color: #3b82f6;
  --background: #ffffff;
  width: 350px;
  height: 400px;
  font-family: inherit;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .emoji-picker-custom {
    --background: #1f2937;
    --border-color: #374151;
    --input-border-color: #4b5563;
  }
}
</style>
