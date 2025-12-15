<template>
  <div class="bg-white border-t border-gray-200 p-4">
    <!-- Typing indicators -->
    <div v-if="typingUsers.length > 0" class="mb-2 text-sm text-gray-500">
      {{ typingText }}
    </div>

    <!-- Reply preview -->
    <div v-if="replyingTo" class="mb-3 p-3 bg-gray-50 rounded-lg border-l-4 border-blue-500">
      <div class="flex justify-between items-start">
        <div>
          <p class="text-sm font-medium text-gray-900">Replying to {{ replyingTo.sender?.name }}</p>
          <p class="text-sm text-gray-600 truncate">{{ replyingTo.content }}</p>
        </div>
        <button @click="cancelReply" class="text-gray-400 hover:text-gray-600">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Main input area -->
    <div class="flex items-end space-x-3">
      <!-- Attachment button -->
      <button @click="toggleAttachmentMenu" 
              class="flex-shrink-0 p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
        </svg>
      </button>

      <!-- Text input -->
      <div class="flex-1 relative">
        <textarea
          ref="messageInput"
          v-model="message"
          @keydown="handleKeyDown"
          @input="handleInput"
          @paste="handlePaste"
          placeholder="Type a message..."
          rows="1"
          class="w-full px-4 py-2 border border-gray-300 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent max-h-32 overflow-y-auto"
          :disabled="sending"
        ></textarea>
        
        <!-- Emoji button -->
        <button @click="toggleEmojiPicker" 
                class="absolute right-2 top-1/2 transform -translate-y-1/2 p-1 text-gray-500 hover:text-gray-700 rounded">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
      </div>

      <!-- Send button -->
      <button @click="sendMessage" 
              :disabled="!canSend || sending"
              class="flex-shrink-0 p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
        <svg v-if="sending" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
        </svg>
      </button>
    </div>

    <!-- Attachment menu -->
    <div v-if="showAttachmentMenu" 
         class="absolute bottom-16 left-4 bg-white rounded-lg shadow-lg border p-2 z-10">
      <input ref="fileInput" type="file" multiple class="hidden" @change="handleFileSelect" />
      <input ref="imageInput" type="file" accept="image/*" multiple class="hidden" @change="handleImageSelect" />
      
      <button @click="selectImages" 
              class="flex items-center space-x-2 w-full p-2 hover:bg-gray-100 rounded text-left">
        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span>Photos</span>
      </button>
      
      <button @click="selectFiles" 
              class="flex items-center space-x-2 w-full p-2 hover:bg-gray-100 rounded text-left">
        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span>Documents</span>
      </button>
    </div>

    <!-- Emoji picker -->
    <div v-if="showEmojiPicker" 
         class="absolute bottom-16 right-4 bg-white rounded-lg shadow-lg border p-4 z-10">
      <div class="grid grid-cols-8 gap-2 max-h-48 overflow-y-auto">
        <button v-for="emoji in commonEmojis" :key="emoji"
                @click="insertEmoji(emoji)"
                class="p-2 hover:bg-gray-100 rounded text-lg">
          {{ emoji }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'

const props = defineProps({
  typingUsers: {
    type: Array,
    default: () => []
  },
  replyingTo: {
    type: Object,
    default: null
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['send', 'typing-start', 'typing-stop', 'cancel-reply'])

const message = ref('')
const sending = ref(false)
const showAttachmentMenu = ref(false)
const showEmojiPicker = ref(false)
const messageInput = ref(null)
const fileInput = ref(null)
const imageInput = ref(null)
const typingTimeout = ref(null)

const commonEmojis = ['😀', '😂', '😍', '🤔', '😢', '😡', '👍', '👎', '❤️', '🔥', '💯', '🎉', '😎', '🤝', '👏', '🙏']

const canSend = computed(() => {
  return message.value.trim().length > 0 && !props.disabled
})

const typingText = computed(() => {
  const users = props.typingUsers
  if (users.length === 1) {
    return `${users[0].name} is typing...`
  } else if (users.length === 2) {
    return `${users[0].name} and ${users[1].name} are typing...`
  } else if (users.length > 2) {
    return `${users[0].name} and ${users.length - 1} others are typing...`
  }
  return ''
})

function handleKeyDown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

function handleInput() {
  autoResize()
  
  // Handle typing indicators
  if (message.value.trim()) {
    emit('typing-start')
    
    // Clear existing timeout
    if (typingTimeout.value) {
      clearTimeout(typingTimeout.value)
    }
    
    // Set new timeout to stop typing
    typingTimeout.value = setTimeout(() => {
      emit('typing-stop')
    }, 1000)
  } else {
    emit('typing-stop')
    if (typingTimeout.value) {
      clearTimeout(typingTimeout.value)
    }
  }
}

function autoResize() {
  nextTick(() => {
    const textarea = messageInput.value
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = Math.min(textarea.scrollHeight, 128) + 'px'
    }
  })
}

async function sendMessage() {
  if (!canSend.value || sending.value) return
  
  const content = message.value.trim()
  if (!content) return
  
  console.log('Sending message:', content)
  sending.value = true
  
  try {
    emit('send', {
      content,
      type: 'text',
      replyTo: props.replyingTo?.id
    })
    
    message.value = ''
    emit('typing-stop')
    autoResize()
    
    if (props.replyingTo) {
      emit('cancel-reply')
    }
    
    console.log('Message sent successfully')
  } catch (error) {
    console.error('Failed to send message:', error)
    alert('Failed to send message: ' + error.message)
  } finally {
    sending.value = false
  }
}

function toggleAttachmentMenu() {
  showAttachmentMenu.value = !showAttachmentMenu.value
  showEmojiPicker.value = false
}

function toggleEmojiPicker() {
  showEmojiPicker.value = !showEmojiPicker.value
  showAttachmentMenu.value = false
}

function selectImages() {
  imageInput.value?.click()
  showAttachmentMenu.value = false
}

function selectFiles() {
  fileInput.value?.click()
  showAttachmentMenu.value = false
}

function handleImageSelect(event) {
  const files = Array.from(event.target.files)
  if (files.length > 0) {
    emit('send', {
      content: message.value.trim(),
      type: 'image',
      files
    })
    message.value = ''
  }
}

function handleFileSelect(event) {
  const files = Array.from(event.target.files)
  if (files.length > 0) {
    emit('send', {
      content: message.value.trim(),
      type: 'file',
      files
    })
    message.value = ''
  }
}

function insertEmoji(emoji) {
  const textarea = messageInput.value
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  
  message.value = message.value.substring(0, start) + emoji + message.value.substring(end)
  
  nextTick(() => {
    textarea.focus()
    textarea.setSelectionRange(start + emoji.length, start + emoji.length)
  })
  
  showEmojiPicker.value = false
}

function handlePaste(event) {
  const items = event.clipboardData?.items
  if (!items) return
  
  const files = []
  for (let item of items) {
    if (item.type.indexOf('image') !== -1) {
      const file = item.getAsFile()
      if (file) files.push(file)
    }
  }
  
  if (files.length > 0) {
    event.preventDefault()
    emit('send', {
      content: message.value.trim(),
      type: 'image',
      files
    })
    message.value = ''
  }
}

function cancelReply() {
  emit('cancel-reply')
}

// Close menus when clicking outside
function handleClickOutside(event) {
  if (!event.target.closest('.attachment-menu')) {
    showAttachmentMenu.value = false
  }
  if (!event.target.closest('.emoji-picker')) {
    showEmojiPicker.value = false
  }
}

// Watch for changes in replyingTo to focus input
watch(() => props.replyingTo, (newValue) => {
  if (newValue) {
    nextTick(() => {
      messageInput.value?.focus()
    })
  }
})
</script>