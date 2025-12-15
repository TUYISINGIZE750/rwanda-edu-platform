<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="bg-white rounded-2xl shadow-xl p-6 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <GlobeAltIcon class="w-10 h-10 text-blue-600" />
            <div>
              <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">School Connect</h1>
              <p class="text-gray-600 mt-1">Direct message students & teachers across all schools in Rwanda</p>
            </div>
          </div>
          <button @click="$router.push('/home')" class="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 flex items-center gap-2">
            <ArrowLeftIcon class="w-5 h-5" />
            Back
          </button>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-6">
        <!-- All Users by School -->
        <div class="col-span-2 bg-white rounded-2xl shadow-xl p-6">
          <div class="mb-6">
            <div class="flex items-center gap-2 mb-3">
              <UsersIcon class="w-6 h-6 text-blue-600" />
              <h2 class="text-xl font-bold">All Schools & Users (Same School + Inter-School)</h2>
            </div>
            <div class="relative">
              <MagnifyingGlassIcon class="w-6 h-6 text-gray-400 absolute left-3 top-3.5" />
              <input v-model="searchQuery" @input="filterUsers" type="text" placeholder="Search by name, school, district, trade, or role..." class="w-full px-4 py-3 pl-11 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none shadow-sm">
            </div>
            <p v-if="searchQuery" class="text-sm text-gray-600 mt-2">Found {{ totalUsers }} user(s) in {{ filteredSchools.length }} school(s)</p>
          </div>
          
          <div class="space-y-6 max-h-[600px] overflow-y-auto pr-2">
            <!-- Group by District -->
            <div v-for="(districtSchools, district) in groupedByDistrict" :key="district" class="border-2 border-blue-200 rounded-xl p-4 bg-gradient-to-br from-blue-50 to-indigo-50">
              <h3 class="font-bold text-lg text-blue-700 mb-4 flex items-center gap-2">
                <MapPinIcon class="w-6 h-6 text-blue-600" />
                {{ district }}
              </h3>
              
              <!-- Schools in District -->
              <div class="space-y-4">
                <div v-for="school in districtSchools" :key="school.school_id" class="bg-white border-2 border-purple-200 rounded-lg p-4 shadow-md hover:shadow-lg transition-shadow">
                  <div class="flex items-start justify-between mb-3 pb-3 border-b border-gray-200">
                    <div class="flex-1">
                      <h4 class="font-bold text-base text-purple-700 flex items-center gap-2">
                        <BuildingOfficeIcon class="w-6 h-6 text-purple-600" />
                        {{ school.school_name }}
                      </h4>
                      <p class="text-xs text-gray-600 mt-1 flex items-center gap-2">
                        <MapPinIcon class="w-4 h-4" />
                        <span class="bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">{{ school.province }}</span>
                        <span class="bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">{{ school.district }}</span>
                      </p>
                    </div>
                    <span class="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
                      <UserIcon class="w-4 h-4" />
                      {{ school.users.length }}
                    </span>
                  </div>
                  
                  <!-- Users in School -->
                  <div class="space-y-2">
                    <div v-for="user in school.users" :key="user.id" class="flex items-center justify-between p-3 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 rounded-lg border border-transparent hover:border-purple-200 transition-all">
                      <div class="flex-1">
                        <p class="font-semibold text-gray-900 flex items-center gap-2">
                          <AcademicCapIcon v-if="user.role === 'STUDENT'" class="w-5 h-5 text-blue-600" />
                          <UserIcon v-else-if="user.role === 'TEACHER'" class="w-5 h-5 text-purple-600" />
                          <CheckBadgeIcon v-else class="w-5 h-5 text-green-600" />
                          {{ user.full_name }}
                        </p>
                        <div class="flex items-center gap-2 mt-1">
                          <span class="text-xs bg-gray-100 text-gray-700 px-2 py-0.5 rounded-full font-medium">{{ user.role }}</span>
                          <span v-if="user.selected_trade" class="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full flex items-center gap-1">
                            <AcademicCapIcon class="w-3 h-3" />
                            {{ user.selected_trade }} - {{ user.selected_level }}
                          </span>
                        </div>
                      </div>
                      <button v-if="user.connection_id" @click="openChatById(user.connection_id, user, school)" class="px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white text-sm rounded-lg hover:from-green-600 hover:to-emerald-600 font-medium shadow-md flex items-center gap-1">
                        <ChatBubbleLeftRightIcon class="w-4 h-4" />
                        Chat
                      </button>
                      <button v-else-if="user.request_status === 'PENDING_SENT'" disabled class="px-4 py-2 bg-orange-300 text-white text-sm rounded-lg cursor-not-allowed font-medium flex items-center gap-1">
                        <ClockIcon class="w-4 h-4" />
                        Pending
                      </button>
                      <button v-else-if="user.request_status === 'PENDING_RECEIVED'" @click="viewRequest(user)" class="px-4 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-white text-sm rounded-lg hover:from-yellow-600 hover:to-orange-600 font-medium shadow-md flex items-center gap-1">
                        <PaperAirplaneIcon class="w-4 h-4" />
                        Respond
                      </button>
                      <button v-else @click="sendRequest(user, school)" class="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white text-sm rounded-lg hover:from-blue-600 hover:to-purple-600 font-medium shadow-md flex items-center gap-1">
                        <PaperAirplaneIcon class="w-4 h-4" />
                        Request
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="Object.keys(groupedByDistrict).length === 0" class="text-center py-12">
              <MagnifyingGlassIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p class="text-gray-500 text-lg font-semibold">No users found</p>
              <p class="text-gray-400 text-sm mt-1">Try a different search term</p>
            </div>
          </div>
        </div>

        <!-- Pending Requests & My Chats -->
        <div class="col-span-1 bg-white rounded-2xl shadow-xl p-6">
          <div class="mb-4">
            <button @click="showPending = true" class="w-full px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 flex items-center justify-between">
              <span class="flex items-center gap-2">
                <EnvelopeIcon class="w-5 h-5" />
                Pending Requests
              </span>
              <span v-if="pendingRequests.length > 0" class="bg-white text-orange-500 px-2 py-1 rounded-full text-sm font-bold flex items-center gap-1">
                <BellAlertIcon class="w-4 h-4" />
                {{ pendingRequests.length }}
              </span>
            </button>
          </div>
          <div class="flex items-center gap-2 mb-4">
            <ChatBubbleLeftRightIcon class="w-6 h-6 text-blue-600" />
            <h2 class="text-xl font-bold">My Chats ({{ connections.length }})</h2>
          </div>
          
          <div class="space-y-3 max-h-[600px] overflow-y-auto">
            <div v-for="conn in connections" :key="conn.connection_id" @click="openChat(conn)" class="border rounded-lg p-3 hover:bg-blue-50 cursor-pointer relative">
              <div v-if="conn.unread_count > 0" class="absolute top-2 right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-xs font-bold">{{ conn.unread_count }}</div>
              <h3 class="font-semibold">{{ conn.user_name }}</h3>
              <p class="text-xs text-gray-600">{{ conn.user_role }} • {{ conn.school_name }}</p>
              <p v-if="conn.last_message" class="text-sm text-gray-700 mt-2 truncate">{{ conn.last_message }}</p>
            </div>
            <p v-if="connections.length === 0" class="text-center text-gray-500 py-8">No chats yet</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Modal -->
    <div v-if="activeChat" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50" @click="activeChat = null">
      <div class="bg-white rounded-2xl w-full max-w-4xl h-[85vh] flex flex-col shadow-2xl" @click.stop>
        <div class="p-4 border-b bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-t-2xl">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-lg flex items-center gap-2">
                <UserIcon class="w-6 h-6" />
                {{ activeChat.user_name }}
              </h3>
              <p class="text-sm text-blue-100 flex items-center gap-1 mt-1">
                <BuildingOfficeIcon class="w-4 h-4" />
                {{ activeChat.school_name }}
              </p>
              <p v-if="activeChat.district" class="text-xs text-blue-200 flex items-center gap-1">
                <MapPinIcon class="w-3 h-3" />
                {{ activeChat.district }}, {{ activeChat.province }}
              </p>
            </div>
            <button @click="activeChat = null" class="text-white hover:bg-white/20 p-2 rounded-lg">
              <XMarkIcon class="w-6 h-6" />
            </button>
          </div>
        </div>

        <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-3">
          <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full">
            <ChatBubbleLeftRightIcon class="w-20 h-20 text-gray-300 mb-4" />
            <p class="text-gray-500 text-lg font-semibold">No messages yet</p>
            <p class="text-gray-400 text-sm">Start the conversation!</p>
          </div>
          
          <div v-for="msg in messages" :key="msg.id" class="flex items-end gap-2" :class="msg.is_mine ? 'justify-end' : 'justify-start'">
            <!-- Avatar for others -->
            <div v-if="!msg.is_mine" class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-semibold text-sm flex-shrink-0">
              {{ msg.sender_name?.charAt(0).toUpperCase() || 'U' }}
            </div>
            
            <div class="max-w-md">
              <div v-if="!msg.is_mine" class="flex items-center gap-2 mb-1 ml-1">
                <span class="text-sm font-semibold text-gray-800">{{ msg.sender_name }}</span>
              </div>
              
              <div class="rounded-2xl px-4 py-2.5 shadow-sm" :class="msg.is_mine ? 'bg-blue-500 text-white rounded-br-sm' : 'bg-white text-gray-900 rounded-bl-sm border border-gray-200'">
                <!-- Reply Preview -->
                <div v-if="msg.reply_to" class="mb-2 p-2 rounded-lg border-l-4 cursor-pointer hover:opacity-80" :class="msg.is_mine ? 'bg-blue-600 border-blue-300' : 'bg-gray-100 border-purple-400'">
                  <div class="flex items-center gap-2 mb-1">
                    <svg class="w-4 h-4" :class="msg.is_mine ? 'text-blue-200' : 'text-purple-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                    </svg>
                    <span class="text-xs font-semibold" :class="msg.is_mine ? 'text-blue-100' : 'text-purple-600'">{{ msg.reply_to.sender_name }}</span>
                  </div>
                  <p class="text-xs" :class="msg.is_mine ? 'text-blue-100' : 'text-gray-600'">{{ msg.reply_to.content }}</p>
                </div>
                
                <!-- File Content -->
                <div v-if="msg.file_url" class="mb-2">
                  <!-- Image Preview -->
                  <div v-if="msg.file_type?.startsWith('image/')" class="max-w-xs relative group">
                    <img :src="`http://localhost:8080${msg.file_url}`" :alt="msg.file_name" class="rounded-lg max-w-full h-auto cursor-pointer" @click="openFileUrl(msg.file_url)" />
                    <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button @click.stop="downloadFileUrl(msg.file_url, msg.file_name)" class="bg-black bg-opacity-50 text-white p-1 rounded-full hover:bg-opacity-70">
                        <ArrowDownTrayIcon class="w-4 h-4" />
                      </button>
                    </div>
                    <p class="text-xs mt-1" :class="msg.is_mine ? 'text-blue-100' : 'text-gray-500'">{{ msg.file_name }} • {{ formatFileSize(msg.file_size) }}</p>
                  </div>
                  
                  <!-- Video Preview -->
                  <div v-else-if="msg.file_type?.startsWith('video/')" class="max-w-xs">
                    <video :src="`http://localhost:8080${msg.file_url}`" controls class="rounded-lg max-w-full h-auto"></video>
                    <p class="text-xs mt-1" :class="msg.is_mine ? 'text-blue-100' : 'text-gray-500'">{{ msg.file_name }} • {{ formatFileSize(msg.file_size) }}</p>
                  </div>
                  
                  <!-- Audio Preview -->
                  <div v-else-if="msg.file_type?.startsWith('audio/')" class="max-w-xs">
                    <div class="bg-gray-100 rounded-lg p-3">
                      <audio :src="`http://localhost:8080${msg.file_url}`" controls class="w-full"></audio>
                      <p class="text-xs mt-2" :class="msg.is_mine ? 'text-blue-100' : 'text-gray-500'">{{ msg.file_name }} • {{ formatFileSize(msg.file_size) }}</p>
                    </div>
                  </div>
                  
                  <!-- Other Files -->
                  <div v-else class="flex items-center gap-3 p-3 rounded-lg cursor-pointer hover:opacity-80" :class="msg.is_mine ? 'bg-blue-600' : 'bg-gray-100'" @click="downloadFileUrl(msg.file_url, msg.file_name)">
                    <div class="w-10 h-10 rounded-lg flex items-center justify-center" :class="msg.is_mine ? 'bg-blue-500' : 'bg-gray-200'">
                      <component :is="getFileIconComponent(msg.file_type)" class="w-6 h-6" :class="msg.is_mine ? 'text-white' : 'text-gray-600'" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="font-medium truncate" :class="msg.is_mine ? 'text-white' : 'text-gray-900'">{{ msg.file_name }}</p>
                      <p class="text-xs" :class="msg.is_mine ? 'text-blue-100' : 'text-gray-500'">{{ formatFileSize(msg.file_size) }} • Click to download</p>
                    </div>
                    <ArrowDownTrayIcon class="w-5 h-5" :class="msg.is_mine ? 'text-blue-200' : 'text-gray-400'" />
                  </div>
                </div>
                
                <!-- Text Content -->
                <p v-if="msg.content" class="text-sm leading-relaxed whitespace-pre-wrap break-words">{{ msg.content }}</p>
                
                <div class="flex items-center justify-end gap-1 mt-1">
                  <p class="text-xs" :class="msg.is_mine ? 'text-blue-100' : 'text-gray-500'">{{ formatTime(msg.created_at) }}</p>
                  <CheckBadgeIcon v-if="msg.is_mine" class="w-4 h-4" :class="msg.is_mine ? 'text-blue-100' : 'text-gray-400'" />
                </div>
                
                <!-- Message Actions -->
                <div class="flex items-center gap-2 mt-3 flex-wrap">
                  <button @click="toggleReaction(msg.id, '👍')" :class="msg.userReactions?.[currentUserId]?.includes('👍') ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg scale-105 ring-2 ring-blue-300' : 'bg-white hover:bg-blue-50 text-blue-600'" class="px-3 py-1.5 rounded-full transition-all transform hover:scale-110 active:scale-95 flex items-center gap-1.5 text-sm font-bold shadow-md border-2 border-blue-300">
                    <HandThumbUpIcon class="w-5 h-5" />
                    <span>{{ msg.likes || 0 }}</span>
                  </button>
                  
                  <button @click="toggleReaction(msg.id, '❤️')" :class="msg.userReactions?.[currentUserId]?.includes('❤️') ? 'bg-gradient-to-r from-red-500 to-pink-600 text-white shadow-lg scale-105 ring-2 ring-red-300' : 'bg-white hover:bg-red-50 text-red-600'" class="px-3 py-1.5 rounded-full transition-all transform hover:scale-110 active:scale-95 flex items-center gap-1.5 text-sm font-bold shadow-md border-2 border-red-300">
                    <HeartIcon class="w-5 h-5" />
                    <span>{{ msg.loves || 0 }}</span>
                  </button>
                  
                  <button @click="toggleReaction(msg.id, '😂')" :class="msg.userReactions?.[currentUserId]?.includes('😂') ? 'bg-gradient-to-r from-yellow-500 to-orange-600 text-white shadow-lg scale-105 ring-2 ring-yellow-300' : 'bg-white hover:bg-yellow-50 text-yellow-600'" class="px-3 py-1.5 rounded-full transition-all transform hover:scale-110 active:scale-95 flex items-center gap-1.5 text-sm font-bold shadow-md border-2 border-yellow-300">
                    <FaceSmileIcon class="w-5 h-5" />
                    <span>{{ msg.laughs || 0 }}</span>
                  </button>
                  
                  <button @click="toggleReaction(msg.id, '🔥')" :class="msg.userReactions?.[currentUserId]?.includes('🔥') ? 'bg-gradient-to-r from-orange-500 to-red-600 text-white shadow-lg scale-105 ring-2 ring-orange-300' : 'bg-white hover:bg-orange-50 text-orange-600'" class="px-3 py-1.5 rounded-full transition-all transform hover:scale-110 active:scale-95 flex items-center gap-1.5 text-sm font-bold shadow-md border-2 border-orange-300">
                    <FireIcon class="w-5 h-5" />
                    <span>{{ msg.fires || 0 }}</span>
                  </button>
                  
                  <button @click="toggleReaction(msg.id, '🎉')" :class="msg.userReactions?.[currentUserId]?.includes('🎉') ? 'bg-gradient-to-r from-purple-500 to-pink-600 text-white shadow-lg scale-105 ring-2 ring-purple-300' : 'bg-white hover:bg-purple-50 text-purple-600'" class="px-3 py-1.5 rounded-full transition-all transform hover:scale-110 active:scale-95 flex items-center gap-1.5 text-sm font-bold shadow-md border-2 border-purple-300">
                    <SparklesIcon class="w-5 h-5" />
                    <span>{{ msg.parties || 0 }}</span>
                  </button>
                  
                  <button @click="replyToMessage(msg)" class="px-3 py-1.5 hover:bg-purple-100 rounded-full transition-all transform hover:scale-110 active:scale-95 text-sm font-medium text-purple-600 shadow-sm border border-purple-200 flex items-center gap-1">
                    <ArrowUturnLeftIcon class="w-4 h-4" />
                    Reply
                  </button>
                  
                  <button @click="copyMessage(msg)" class="px-3 py-1.5 hover:bg-yellow-100 rounded-full transition-all transform hover:scale-110 active:scale-95 text-sm font-medium text-yellow-600 shadow-sm border border-yellow-200 flex items-center gap-1">
                    <ClipboardDocumentIcon class="w-4 h-4" />
                    Copy
                  </button>
                  
                  <button v-if="msg.is_mine" @click="deleteMessage(msg.id)" class="px-3 py-1.5 hover:bg-red-100 rounded-full transition-all transform hover:scale-110 active:scale-95 text-sm font-medium text-red-600 shadow-sm border border-red-200 flex items-center gap-1">
                    <TrashIcon class="w-4 h-4" />
                    Delete
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Avatar for own messages -->
            <div v-if="msg.is_mine" class="w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white font-semibold text-sm flex-shrink-0">
              {{ msg.sender_name?.charAt(0).toUpperCase() || 'M' }}
            </div>
          </div>
        </div>

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
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
          
          <div v-if="selectedFile" class="mb-2 p-3 bg-blue-50 rounded-lg flex items-center justify-between border border-blue-200">
            <div class="flex items-center gap-2">
              <component :is="getFileIconComponent(selectedFile.type)" class="w-8 h-8 text-blue-600" />
              <div>
                <p class="text-sm font-medium text-gray-900">{{ selectedFile.name }}</p>
                <p class="text-xs text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
              </div>
            </div>
            <button @click="selectedFile = null" class="text-red-500 hover:text-red-700">
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
          
          <div class="flex items-center gap-2">
            <!-- Attachment Button -->
            <div class="relative">
              <button @click="showAttachmentMenu = !showAttachmentMenu" class="p-2.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-all">
                <PaperClipIcon class="w-6 h-6" />
              </button>
              
              <!-- Attachment Menu -->
              <div v-if="showAttachmentMenu" class="absolute bottom-full left-0 mb-2 bg-white rounded-xl shadow-lg border p-2 min-w-48 z-10">
                <button @click="selectFile('image')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-blue-50 rounded-lg text-left">
                  <PhotoIcon class="w-6 h-6 text-blue-600" />
                  <span class="text-sm font-medium text-gray-700">Photo</span>
                </button>
                <button @click="selectFile('video')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-purple-50 rounded-lg text-left">
                  <VideoCameraIcon class="w-6 h-6 text-purple-600" />
                  <span class="text-sm font-medium text-gray-700">Video</span>
                </button>
                <button @click="selectFile('audio')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-green-50 rounded-lg text-left">
                  <MusicalNoteIcon class="w-6 h-6 text-green-600" />
                  <span class="text-sm font-medium text-gray-700">Audio</span>
                </button>
                <button @click="selectFile('document')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-yellow-50 rounded-lg text-left">
                  <DocumentIcon class="w-6 h-6 text-yellow-600" />
                  <span class="text-sm font-medium text-gray-700">Document</span>
                </button>
                <button @click="selectFile('any')" class="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-50 rounded-lg text-left">
                  <ArchiveBoxIcon class="w-6 h-6 text-gray-600" />
                  <span class="text-sm font-medium text-gray-700">Any File</span>
                </button>
              </div>
            </div>
            
            <!-- Message Input -->
            <div class="flex-1 relative">
              <input v-model="newMessage" @keyup.enter="sendMessage" type="text" placeholder="Type a message..." class="w-full px-4 py-2.5 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" :disabled="sending">
            </div>
            
            <!-- Send Button -->
            <button @click="sendMessage" :disabled="(!newMessage.trim() && !selectedFile) || sending" class="p-2.5 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105">
              <PaperAirplaneIcon class="w-6 h-6" />
            </button>
          </div>
          
          <!-- Hidden File Input -->
          <input ref="fileInput" type="file" class="hidden" @change="handleFileSelect" />
        </div>
      </div>
    </div>

    <!-- Send Request Modal -->
    <div v-if="showRequestModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click="showRequestModal = false">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full" @click.stop>
        <h3 class="text-xl font-bold mb-4">Send Connection Request</h3>
        <div class="mb-4 p-4 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg border-2 border-blue-200">
          <p class="font-bold text-lg flex items-center gap-2">
            <UserIcon class="w-6 h-6 text-blue-600" />
            {{ selectedUser?.full_name }}
          </p>
          <p class="text-sm text-gray-700 mt-2">{{ selectedUser?.role }}</p>
          <p class="text-xs text-gray-600 mt-1 flex items-center gap-1">
            <BuildingOfficeIcon class="w-4 h-4" />
            {{ selectedUser?.school_name }}
          </p>
          <p class="text-xs text-gray-600 flex items-center gap-1">
            <MapPinIcon class="w-4 h-4" />
            {{ selectedUser?.district }}, {{ selectedUser?.province }}
          </p>
          <p v-if="selectedUser?.selected_trade" class="text-xs text-green-600 mt-1 flex items-center gap-1">
            <AcademicCapIcon class="w-4 h-4" />
            {{ selectedUser?.selected_trade }} - {{ selectedUser?.selected_level }}
          </p>
        </div>
        <textarea v-model="requestMessage" rows="3" placeholder="Why do you want to connect? (optional)" class="w-full px-4 py-2 border rounded-lg mb-4"></textarea>
        <div class="flex gap-2">
          <button @click="confirmRequest" class="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center justify-center gap-2">
            <PaperAirplaneIcon class="w-5 h-5" />
            Send Request
          </button>
          <button @click="showRequestModal = false" class="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 flex items-center gap-2">
            <XMarkIcon class="w-5 h-5" />
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Pending Requests Modal -->
    <div v-if="showPending" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click="showPending = false">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[600px] flex flex-col" @click.stop>
        <div class="p-4 border-b bg-gradient-to-r from-orange-500 to-yellow-500 text-white rounded-t-2xl">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-lg flex items-center gap-2">
                <EnvelopeIcon class="w-6 h-6" />
                Pending Requests ({{ pendingRequests.length }})
              </h3>
              <p class="text-sm text-white/90">Review connection requests</p>
            </div>
            <button @click="showPending = false" class="text-white hover:bg-white/20 p-2 rounded-lg">
              <XMarkIcon class="w-6 h-6" />
            </button>
          </div>
        </div>

        <div class="flex-1 overflow-y-auto p-4 space-y-3">
          <div v-if="pendingRequests.length === 0" class="text-center py-8 text-gray-500">
            <InboxIcon class="w-16 h-16 text-gray-300 mx-auto mb-2" />
            <p>No pending requests</p>
          </div>
          <div v-for="req in pendingRequests" :key="req.id" class="border rounded-lg p-4 bg-orange-50">
            <div class="flex items-start justify-between mb-3">
              <div>
                <h4 class="font-bold">{{ req.sender_name }}</h4>
                <p class="text-sm text-gray-600">{{ req.sender_role }} • {{ req.sender_school }}</p>
                <p class="text-xs text-gray-500">{{ req.sender_province }}, {{ req.sender_district }}</p>
                <p v-if="req.sender_trade" class="text-xs text-blue-600">{{ req.sender_trade }} - {{ req.sender_level }}</p>
              </div>
            </div>
            <p v-if="req.message" class="text-sm text-gray-700 italic mb-3">“{{ req.message }}”</p>
            <div class="flex gap-2">
              <button @click="acceptRequest(req.id)" class="flex-1 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center justify-center gap-2">
                <CheckCircleIcon class="w-5 h-5" />
                Accept
              </button>
              <button @click="rejectRequest(req.id)" class="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 flex items-center justify-center gap-2">
                <XCircleIcon class="w-5 h-5" />
                Reject
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'
import { 
  MagnifyingGlassIcon, 
  MapPinIcon, 
  AcademicCapIcon, 
  UserIcon, 
  BuildingOfficeIcon, 
  ChatBubbleLeftRightIcon, 
  ClockIcon, 
  PaperAirplaneIcon, 
  XMarkIcon, 
  PaperClipIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  ArrowLeftIcon,
  InboxIcon,
  PhotoIcon,
  VideoCameraIcon,
  MusicalNoteIcon,
  DocumentIcon,
  ArchiveBoxIcon,
  ArrowUturnLeftIcon,
  ClipboardDocumentIcon,
  TrashIcon,
  ArrowDownTrayIcon,
  GlobeAltIcon,
  UsersIcon,
  EnvelopeIcon,
  BellAlertIcon
} from '@heroicons/vue/24/outline'
import { 
  CheckBadgeIcon, 
  HandThumbUpIcon, 
  HeartIcon, 
  FaceSmileIcon, 
  FireIcon, 
  SparklesIcon 
} from '@heroicons/vue/24/solid'

const router = useRouter()

const searchQuery = ref('')
const schools = ref([])
const filteredSchools = ref([])
const groupedByDistrict = ref({})
const totalUsers = ref(0)
const connections = ref([])
const pendingRequests = ref([])
const activeChat = ref(null)
const messages = ref([])
const newMessage = ref('')
const selectedFile = ref(null)
const showRequestModal = ref(false)
const showPending = ref(false)
const requestMessage = ref('')
const selectedUser = ref(null)
const replyingTo = ref(null)
const showAttachmentMenu = ref(false)
const messagesContainer = ref(null)
const fileInput = ref(null)
const sending = ref(false)
const currentUserId = computed(() => {
  // Try multiple sources for user ID
  const userId = localStorage.getItem('user_id') || 
                 localStorage.getItem('userId') ||
                 JSON.parse(localStorage.getItem('user') || '{}').id ||
                 JSON.parse(localStorage.getItem('auth') || '{}').user?.id
  
  console.log('🔍 Looking for user ID:', {
    user_id: localStorage.getItem('user_id'),
    userId: localStorage.getItem('userId'),
    user: localStorage.getItem('user'),
    auth: localStorage.getItem('auth'),
    resolved: userId
  })
  
  return userId
})

async function loadUsers() {
  try {
    const response = await api.get('/inter-school/all-users')
    schools.value = response.data.schools
    
    // Mark users with pending requests
    const pending = await api.get('/inter-school/pending-requests')
    const pendingMap = {}
    pending.data.requests.forEach(req => {
      pendingMap[req.sender_id] = 'PENDING_RECEIVED'
    })
    
    schools.value.forEach(school => {
      school.users.forEach(user => {
        if (pendingMap[user.id]) {
          user.request_status = pendingMap[user.id]
        }
      })
    })
    
    filterUsers()
  } catch (err) {
    console.error('Load users failed:', err)
  }
}

function filterUsers() {
  const query = searchQuery.value.toLowerCase().trim()
  
  if (!query) {
    filteredSchools.value = [...schools.value]
  } else {
    filteredSchools.value = []
    
    schools.value.forEach(school => {
      const matchingUsers = school.users.filter(user => {
        const fullName = (user.full_name || '').toLowerCase()
        const role = (user.role || '').toLowerCase()
        const trade = (user.selected_trade || '').toLowerCase()
        const level = (user.selected_level || '').toLowerCase()
        const schoolName = (school.school_name || '').toLowerCase()
        const district = (school.district || '').toLowerCase()
        const province = (school.province || '').toLowerCase()
        
        return fullName.includes(query) ||
               role.includes(query) ||
               trade.includes(query) ||
               level.includes(query) ||
               schoolName.includes(query) ||
               district.includes(query) ||
               province.includes(query)
      })
      
      if (matchingUsers.length > 0) {
        filteredSchools.value.push({ ...school, users: matchingUsers })
      }
    })
  }
  
  // Group by district
  const grouped = {}
  totalUsers.value = 0
  
  filteredSchools.value.forEach(school => {
    if (!grouped[school.district]) {
      grouped[school.district] = []
    }
    grouped[school.district].push(school)
    totalUsers.value += school.users.length
  })
  
  groupedByDistrict.value = grouped
}

function sendRequest(user, school) {
  selectedUser.value = { ...user, school_name: school.school_name, district: school.district, province: school.province }
  showRequestModal.value = true
}

async function confirmRequest() {
  try {
    await api.post(`/inter-school/request/${selectedUser.value.id}`, null, {
      params: { message: requestMessage.value }
    })
    alert('✅ Request sent!')
    showRequestModal.value = false
    requestMessage.value = ''
    await loadUsers()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to send request')
  }
}

async function loadPendingRequests() {
  try {
    const response = await api.get('/inter-school/pending-requests')
    pendingRequests.value = response.data.requests
  } catch (err) {
    console.error('Load pending failed:', err)
  }
}

async function acceptRequest(requestId) {
  try {
    const response = await api.post(`/inter-school/accept/${requestId}`)
    alert('✅ Connection accepted!')
    await loadPendingRequests()
    await loadConnections()
    await loadUsers()
  } catch (err) {
    alert('Failed to accept')
  }
}

async function rejectRequest(requestId) {
  try {
    await api.post(`/inter-school/reject/${requestId}`)
    alert('✅ Request rejected')
    await loadPendingRequests()
  } catch (err) {
    alert('Failed to reject')
  }
}

function viewRequest(user) {
  showPending.value = true
}

function openChatById(connectionId, user, school) {
  activeChat.value = {
    connection_id: connectionId,
    user_name: user.full_name,
    school_name: school.school_name,
    district: school.district,
    province: school.province
  }
  messages.value = []
  loadMessages(connectionId)
  
  // Poll for new messages every 3 seconds
  if (window.chatPollingInterval) {
    clearInterval(window.chatPollingInterval)
  }
  window.chatPollingInterval = setInterval(() => {
    if (activeChat.value?.connection_id === connectionId) {
      loadMessages(connectionId)
    }
  }, 3000)
}

async function loadConnections() {
  try {
    const response = await api.get('/inter-school/connections')
    connections.value = response.data.connections
  } catch (err) {
    console.error('Load connections failed:', err)
  }
}

async function openChat(connection) {
  activeChat.value = connection
  messages.value = []
  await loadMessages(connection.connection_id)
  
  // Poll for new messages every 3 seconds
  if (window.chatPollingInterval) {
    clearInterval(window.chatPollingInterval)
  }
  window.chatPollingInterval = setInterval(() => {
    if (activeChat.value?.connection_id === connection.connection_id) {
      loadMessages(connection.connection_id)
    }
  }, 3000)
}

async function loadMessages(connectionId) {
  try {
    const response = await api.get(`/inter-school/messages/${connectionId}`)
    messages.value = response.data.messages
    await nextTick()
    scrollToBottom()
  } catch (err) {
    console.error('Load messages failed:', err)
  }
}

function showReactionAnimation(emoji) {
  const animation = document.createElement('div')
  animation.textContent = emoji
  animation.className = 'fixed text-6xl pointer-events-none z-50 animate-bounce'
  animation.style.left = Math.random() * window.innerWidth + 'px'
  animation.style.top = Math.random() * window.innerHeight + 'px'
  document.body.appendChild(animation)
  
  setTimeout(() => {
    if (document.body.contains(animation)) {
      document.body.removeChild(animation)
    }
  }, 1000)
}

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  
  const maxSize = 50 * 1024 * 1024 // 50MB
  if (file.size > maxSize) {
    alert('❌ File too large! Maximum size is 50MB')
    event.target.value = ''
    return
  }
  
  selectedFile.value = file
  showAttachmentMenu.value = false
  
  // Show preview notification
  const fileIcon = getFileIcon(file.type)
  console.log(`${fileIcon} File selected: ${file.name} (${formatFileSize(file.size)})`)
}

async function sendMessage() {
  if ((!newMessage.value?.trim() && !selectedFile.value) || sending.value) return
  
  sending.value = true
  
  try {
    const formData = new FormData()
    if (newMessage.value?.trim()) formData.append('content', newMessage.value.trim())
    if (selectedFile.value) formData.append('file', selectedFile.value)
    if (replyingTo.value?.id) formData.append('reply_to_id', replyingTo.value.id)
    
    await api.post(`/inter-school/messages/${activeChat.value.connection_id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    newMessage.value = ''
    selectedFile.value = null
    replyingTo.value = null
    await loadMessages(activeChat.value.connection_id)
    await nextTick()
    scrollToBottom()
  } catch (err) {
    console.error('Failed to send message:', err)
    alert('Failed to send message')
  } finally {
    sending.value = false
  }
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

async function toggleReaction(messageId, emoji) {
  try {
    const response = await api.post(`/inter-school/messages/${messageId}/react`, null, {
      params: { emoji }
    })
    
    // Update local message with new counts
    const msg = messages.value.find(m => m.id === messageId)
    if (msg && response.data.counts) {
      msg.likes = response.data.counts['👍'] || 0
      msg.loves = response.data.counts['❤️'] || 0
      msg.laughs = response.data.counts['😂'] || 0
      msg.fires = response.data.counts['🔥'] || 0
      msg.parties = response.data.counts['🎉'] || 0
      msg.userReactions = response.data.user_reactions || {}
      
      // Force reactivity
      messages.value = [...messages.value]
      
      // Show animation
      showReactionAnimation(emoji)
    }
  } catch (err) {
    console.error('Failed to toggle reaction:', err)
    alert('❌ Failed to react. Please try again.')
  }
}

function replyToMessage(msg) {
  replyingTo.value = msg
}

async function copyMessage(msg) {
  const text = msg.content || `File: ${msg.file_name}`
  try {
    await navigator.clipboard.writeText(text)
    alert('✅ Copied to clipboard!')
  } catch (err) {
    alert('❌ Failed to copy')
  }
}

async function deleteMessage(messageId) {
  if (!confirm('Delete this message? This cannot be undone.')) return
  
  messages.value = messages.value.filter(m => m.id !== messageId)
  alert('✅ Message deleted')
}

function selectFile(type) {
  showAttachmentMenu.value = false
  
  const acceptTypes = {
    image: 'image/*',
    video: 'video/*',
    audio: 'audio/*',
    document: '.pdf,.doc,.docx,.txt,.rtf',
    any: '*/*'
  }
  
  if (fileInput.value) {
    fileInput.value.accept = acceptTypes[type] || '*/*'
    fileInput.value.click()
  }
}

function formatFileSize(bytes) {
  if (!bytes) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function getFileIconComponent(fileType) {
  if (!fileType) return DocumentIcon
  if (fileType.startsWith('image/')) return PhotoIcon
  if (fileType.startsWith('video/')) return VideoCameraIcon
  if (fileType.startsWith('audio/')) return MusicalNoteIcon
  if (fileType.includes('pdf')) return DocumentIcon
  if (fileType.includes('word') || fileType.includes('document')) return DocumentIcon
  if (fileType.includes('excel') || fileType.includes('spreadsheet')) return DocumentIcon
  if (fileType.includes('powerpoint') || fileType.includes('presentation')) return DocumentIcon
  if (fileType.includes('zip') || fileType.includes('rar') || fileType.includes('archive')) return ArchiveBoxIcon
  if (fileType.includes('text')) return DocumentIcon
  return DocumentIcon
}

function openFileUrl(url) {
  window.open(`http://localhost:8080${url}`, '_blank')
}

function downloadFileUrl(url, filename) {
  const link = document.createElement('a')
  link.href = `http://localhost:8080${url}`
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  alert(`📥 Downloaded: ${filename}`)
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
}

onMounted(async () => {
  await loadUsers()
  await loadConnections()
  await loadPendingRequests()
  // Poll for new requests every 5 seconds
  setInterval(loadPendingRequests, 5000)
})

onUnmounted(() => {
  if (window.chatPollingInterval) {
    clearInterval(window.chatPollingInterval)
  }
})
</script>
