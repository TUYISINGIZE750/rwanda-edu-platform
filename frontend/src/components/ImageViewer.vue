<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-95 z-[100] flex items-center justify-center" @click="close">
    <div class="relative w-full h-full flex flex-col" @click.stop>
      <!-- Header -->
      <div class="bg-black bg-opacity-50 p-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-semibold">
            {{ senderName?.charAt(0).toUpperCase() || 'U' }}
          </div>
          <div>
            <p class="text-white font-medium">{{ senderName || 'Unknown' }}</p>
            <p class="text-gray-300 text-sm">{{ formatTime(timestamp) }}</p>
          </div>
        </div>
        <button @click="close" class="text-white hover:text-gray-300 p-2">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Image Container -->
      <div class="flex-1 flex items-center justify-center p-4 overflow-hidden">
        <img 
          :src="imageUrl" 
          :style="{ transform: `scale(${zoom}) rotate(${rotation}deg)` }"
          class="max-w-full max-h-full object-contain transition-transform duration-200"
          @click.stop
        />
      </div>

      <!-- Controls -->
      <div class="bg-black bg-opacity-50 p-4">
        <div class="flex items-center justify-center gap-4">
          <button @click="zoomOut" class="p-3 bg-gray-800 hover:bg-gray-700 rounded-full text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7" />
            </svg>
          </button>

          <button @click="zoomIn" class="p-3 bg-gray-800 hover:bg-gray-700 rounded-full text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
            </svg>
          </button>

          <button @click="rotate" class="p-3 bg-gray-800 hover:bg-gray-700 rounded-full text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>

          <button @click="download" class="p-3 bg-blue-600 hover:bg-blue-700 rounded-full text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </button>

          <button @click="share" class="p-3 bg-green-600 hover:bg-green-700 rounded-full text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
            </svg>
          </button>

          <button @click="$emit('forward', attachment)" class="p-3 bg-purple-600 hover:bg-purple-700 rounded-full text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>

          <button @click="reset" class="p-3 bg-gray-800 hover:bg-gray-700 rounded-full text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
        <p class="text-center text-gray-300 text-sm mt-3">Zoom: {{ Math.round(zoom * 100) }}%</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  imageUrl: String,
  senderName: String,
  timestamp: String,
  attachment: Object
})

const emit = defineEmits(['close', 'forward'])

const zoom = ref(1)
const rotation = ref(0)

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    zoom.value = 1
    rotation.value = 0
  }
})

function close() {
  emit('close')
}

function zoomIn() {
  if (zoom.value < 3) zoom.value += 0.25
}

function zoomOut() {
  if (zoom.value > 0.5) zoom.value -= 0.25
}

function rotate() {
  rotation.value = (rotation.value + 90) % 360
}

function reset() {
  zoom.value = 1
  rotation.value = 0
}

async function download() {
  try {
    const response = await fetch(props.imageUrl)
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `image-${Date.now()}.jpg`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
    alert('✅ Image downloaded successfully!')
  } catch (err) {
    console.error('Download failed:', err)
    alert('❌ Failed to download image')
  }
}

async function share() {
  // Check if Web Share API is supported
  if (navigator.share) {
    try {
      // Fetch the image
      const response = await fetch(props.imageUrl)
      const blob = await response.blob()
      
      // Determine file type from blob
      const fileType = blob.type || 'image/jpeg'
      const extension = fileType.split('/')[1] || 'jpg'
      const fileName = `shared-image-${Date.now()}.${extension}`
      
      const file = new File([blob], fileName, { type: fileType })
      
      // Check if files can be shared
      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        // Share with native share sheet (WhatsApp, Facebook, Email, Bluetooth, etc.)
        await navigator.share({
          title: 'Rwanda Edu Platform - Shared Image',
          text: `Shared by ${props.senderName || 'Unknown'}`,
          files: [file]
        })
        // User completed share or cancelled - no alert needed
      } else {
        // Fallback: share URL only
        await navigator.share({
          title: 'Rwanda Edu Platform - Shared Image',
          text: `Check out this image shared by ${props.senderName || 'Unknown'}`,
          url: props.imageUrl
        })
      }
    } catch (err) {
      // User cancelled the share - don't show error
      if (err.name === 'AbortError') {
        console.log('Share cancelled by user')
      } else {
        console.error('Share failed:', err)
        // Fallback to copy link
        copyLink()
      }
    }
  } else {
    // Browser doesn't support Web Share API - copy link instead
    copyLink()
  }
}

function copyLink() {
  navigator.clipboard.writeText(props.imageUrl)
    .then(() => alert('✅ Image link copied to clipboard! You can now paste it in WhatsApp, Email, or any other app.'))
    .catch(() => {
      // Fallback if clipboard API fails
      prompt('Copy this link to share:', props.imageUrl)
    })
}

function formatTime(timestamp) {
  if (!timestamp) return 'Just now'
  const date = new Date(timestamp)
  if (isNaN(date.getTime())) return 'Just now'
  return date.toLocaleString()
}
</script>
