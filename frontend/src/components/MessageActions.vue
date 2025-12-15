<template>
  <div class="message-actions-wrapper">
    <!-- Quick Reactions (appear on hover) -->
    <div v-if="showQuickReactions" 
         class="absolute -top-8 left-0 bg-white rounded-full shadow-lg border-2 border-gray-200 px-2 py-1 flex gap-1 z-10 animate-bounce-in">
      <button v-for="emoji in quickReactions" :key="emoji"
              @click="addReaction(emoji)"
              class="text-xl hover:scale-125 transition-transform p-1">
        {{ emoji }}
      </button>
      <button @click="showReactionPicker = true" 
              class="text-gray-500 hover:text-gray-700 px-2">
        ➕
      </button>
    </div>

    <!-- Actions Menu Button -->
    <button @click="toggleMenu" 
            class="p-1 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 transition-all">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
      </svg>
    </button>

    <!-- Actions Dropdown Menu -->
    <div v-if="showMenu" 
         class="absolute right-0 top-8 bg-white rounded-xl shadow-2xl border-2 border-gray-200 py-2 w-56 z-50 animate-slide-down">
      
      <!-- Reply -->
      <button @click="handleAction('reply')" 
              class="w-full px-4 py-2 hover:bg-blue-50 flex items-center gap-3 text-left transition-colors group">
        <svg class="w-5 h-5 text-blue-600 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
        </svg>
        <span class="font-medium text-gray-700">Reply</span>
      </button>

      <!-- Forward -->
      <button @click="handleAction('forward')" 
              class="w-full px-4 py-2 hover:bg-purple-50 flex items-center gap-3 text-left transition-colors group">
        <svg class="w-5 h-5 text-purple-600 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
        </svg>
        <span class="font-medium text-gray-700">Forward</span>
      </button>

      <!-- Copy -->
      <button @click="handleAction('copy')" 
              class="w-full px-4 py-2 hover:bg-green-50 flex items-center gap-3 text-left transition-colors group">
        <svg class="w-5 h-5 text-green-600 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
        <span class="font-medium text-gray-700">Copy Text</span>
      </button>

      <!-- Download -->
      <button v-if="hasAttachments" @click="handleAction('download')" 
              class="w-full px-4 py-2 hover:bg-indigo-50 flex items-center gap-3 text-left transition-colors group">
        <svg class="w-5 h-5 text-indigo-600 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        <span class="font-medium text-gray-700">Download</span>
      </button>

      <div class="border-t border-gray-200 my-2"></div>

      <!-- Pin Message -->
      <button @click="handleAction('pin')" 
              class="w-full px-4 py-2 hover:bg-yellow-50 flex items-center gap-3 text-left transition-colors group">
        <svg class="w-5 h-5 text-yellow-600 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
        </svg>
        <span class="font-medium text-gray-700">Pin Message</span>
      </button>

      <!-- Star/Favorite -->
      <button @click="handleAction('star')" 
              class="w-full px-4 py-2 hover:bg-amber-50 flex items-center gap-3 text-left transition-colors group">
        <svg class="w-5 h-5 text-amber-600 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
        </svg>
        <span class="font-medium text-gray-700">Add to Favorites</span>
      </button>

      <div class="border-t border-gray-200 my-2"></div>

      <!-- Report -->
      <button @click="handleAction('report')" 
              class="w-full px-4 py-2 hover:bg-orange-50 flex items-center gap-3 text-left transition-colors group">
        <svg class="w-5 h-5 text-orange-600 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span class="font-medium text-gray-700">Report</span>
      </button>

      <!-- Delete (only for own messages) -->
      <button v-if="isOwnMessage" @click="handleAction('delete')" 
              class="w-full px-4 py-2 hover:bg-red-50 flex items-center gap-3 text-left transition-colors group">
        <svg class="w-5 h-5 text-red-600 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
        <span class="font-medium text-red-600">Delete</span>
      </button>
    </div>

    <!-- Reaction Picker Modal -->
    <div v-if="showReactionPicker" 
         class="fixed inset-0 bg-black bg-opacity-50 z-[60] flex items-center justify-center"
         @click="showReactionPicker = false">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full mx-4" @click.stop>
        <h3 class="text-lg font-bold mb-4">React to Message</h3>
        <div class="grid grid-cols-6 gap-3">
          <button v-for="emoji in allReactions" :key="emoji"
                  @click="addReaction(emoji)"
                  class="text-4xl hover:scale-125 transition-transform p-2 hover:bg-gray-100 rounded-lg">
            {{ emoji }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  message: Object,
  isOwnMessage: Boolean,
  hasAttachments: Boolean
})

const emit = defineEmits(['action', 'reaction'])

const showMenu = ref(false)
const showQuickReactions = ref(false)
const showReactionPicker = ref(false)

const quickReactions = ['👍', '❤️', '😂', '😮', '😢', '🙏']
const allReactions = [
  '👍','👎','❤️','🔥','😂','😮','😢','😡','🙏','👏',
  '🎉','💯','✅','❌','🤔','😍','🥰','😎','🤩','😱',
  '🤯','💪','👌','✌️','🤝','💡','⭐','🌟','✨','🎯'
]

function toggleMenu() {
  showMenu.value = !showMenu.value
  showQuickReactions.value = false
}

function handleAction(action) {
  emit('action', { action, message: props.message })
  showMenu.value = false
}

function addReaction(emoji) {
  emit('reaction', { emoji, messageId: props.message.id })
  showQuickReactions.value = false
  showReactionPicker.value = false
}

// Show quick reactions on hover
function showQuick() {
  showQuickReactions.value = true
}

function hideQuick() {
  setTimeout(() => {
    if (!showReactionPicker.value) {
      showQuickReactions.value = false
    }
  }, 200)
}

defineExpose({ showQuick, hideQuick })
</script>

<style scoped>
@keyframes bounce-in {
  0% { transform: scale(0.8) translateY(10px); opacity: 0; }
  50% { transform: scale(1.05); }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}

@keyframes slide-down {
  from { transform: translateY(-10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.animate-bounce-in {
  animation: bounce-in 0.3s ease-out;
}

.animate-slide-down {
  animation: slide-down 0.2s ease-out;
}
</style>
