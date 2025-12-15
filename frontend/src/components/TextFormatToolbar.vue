<template>
  <div class="bg-white border-t border-gray-200 p-2 flex items-center gap-2 flex-wrap">
    <!-- Bold -->
    <button @click="$emit('format', 'bold')" 
            :class="{ 'bg-blue-100 text-blue-600': formats.bold }"
            class="p-2 hover:bg-gray-100 rounded transition-colors" title="Bold (Ctrl+B)">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M11 3H6v14h5.5c2.5 0 4.5-2 4.5-4.5 0-1.5-.7-2.8-1.8-3.5C15.3 8.3 16 7 16 5.5 16 3 14 3 11 3zm-1 6V5h1.5C12.9 5 14 6.1 14 7.5S12.9 10 11.5 10H10zm0 2h2c1.7 0 3 1.3 3 3s-1.3 3-3 3h-2v-6z"/>
      </svg>
    </button>

    <!-- Italic -->
    <button @click="$emit('format', 'italic')"
            :class="{ 'bg-blue-100 text-blue-600': formats.italic }"
            class="p-2 hover:bg-gray-100 rounded transition-colors" title="Italic (Ctrl+I)">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 3h6v2h-2l-4 10h2v2H6v-2h2l4-10H10V3z"/>
      </svg>
    </button>

    <!-- Underline -->
    <button @click="$emit('format', 'underline')"
            :class="{ 'bg-blue-100 text-blue-600': formats.underline }"
            class="p-2 hover:bg-gray-100 rounded transition-colors" title="Underline (Ctrl+U)">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 15c-2.8 0-5-2.2-5-5V3h2v7c0 1.7 1.3 3 3 3s3-1.3 3-3V3h2v7c0 2.8-2.2 5-5 5zM4 17h12v2H4v-2z"/>
      </svg>
    </button>

    <!-- Strikethrough -->
    <button @click="$emit('format', 'strike')"
            :class="{ 'bg-blue-100 text-blue-600': formats.strike }"
            class="p-2 hover:bg-gray-100 rounded transition-colors" title="Strikethrough">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M3 9h14v2H3V9zm4-6h6c2.2 0 4 1.8 4 4 0 1.1-.4 2.1-1.2 2.8l-1.5-1.5c.4-.4.7-1 .7-1.6 0-1.1-.9-2-2-2H7c-1.1 0-2 .9-2 2v.3l-2-2V5c0-2.2 1.8-4 4-4zm6 14H7c-2.2 0-4-1.8-4-4v-.3l2 2V15c0 1.1.9 2 2 2h6c1.1 0 2-.9 2-2v-.3l2 2V15c0 2.2-1.8 4-4 4z"/>
      </svg>
    </button>

    <div class="w-px h-6 bg-gray-300"></div>

    <!-- Text Color -->
    <div class="relative">
      <button @click="showColorPicker = !showColorPicker"
              class="p-2 hover:bg-gray-100 rounded transition-colors flex items-center gap-1" title="Text Color">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 2L3 18h3l1.5-4h5l1.5 4h3L10 2zm0 4l2 5H8l2-5z"/>
        </svg>
        <div class="w-4 h-1 rounded" :style="{ backgroundColor: textColor }"></div>
      </button>
      <div v-if="showColorPicker" class="absolute bottom-full left-0 mb-2 bg-white rounded-lg shadow-xl border p-3 z-50">
        <div class="grid grid-cols-6 gap-2">
          <button v-for="color in colors" :key="color"
                  @click="selectColor(color)"
                  :style="{ backgroundColor: color }"
                  class="w-8 h-8 rounded-full hover:scale-110 transition-transform border-2 border-gray-200">
          </button>
        </div>
      </div>
    </div>

    <!-- Font Size -->
    <select @change="$emit('fontSize', $event.target.value)"
            class="px-2 py-1 border border-gray-300 rounded text-sm hover:border-blue-500 transition-colors">
      <option value="12">Small</option>
      <option value="14" selected>Normal</option>
      <option value="16">Large</option>
      <option value="20">X-Large</option>
      <option value="24">Huge</option>
    </select>

    <div class="w-px h-6 bg-gray-300"></div>

    <!-- Code Block -->
    <button @click="$emit('format', 'code')"
            :class="{ 'bg-blue-100 text-blue-600': formats.code }"
            class="p-2 hover:bg-gray-100 rounded transition-colors" title="Code">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M7 7l-4 4 4 4v-3h6v3l4-4-4-4v3H7V7z"/>
      </svg>
    </button>

    <!-- Quote -->
    <button @click="$emit('format', 'quote')"
            class="p-2 hover:bg-gray-100 rounded transition-colors" title="Quote">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M6 7H4c-1.1 0-2 .9-2 2v6c0 1.1.9 2 2 2h2c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2zm8 0h-2c-1.1 0-2 .9-2 2v6c0 1.1.9 2 2 2h2c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2z"/>
      </svg>
    </button>

    <!-- Clear Formatting -->
    <button @click="$emit('clearFormat')"
            class="p-2 hover:bg-red-100 text-red-600 rounded transition-colors ml-auto" title="Clear Formatting">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M8.5 3h3l1 3h4l-1.5 11h-9L4.5 6h4l1-3zm1 2l-.5 1.5h2L10.5 5h-1zM7 8l1 8h4l1-8H7z"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  formats: {
    type: Object,
    default: () => ({ bold: false, italic: false, underline: false, strike: false, code: false })
  }
})

defineEmits(['format', 'color', 'fontSize', 'clearFormat'])

const showColorPicker = ref(false)
const textColor = ref('#000000')

const colors = [
  '#000000', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF',
  '#00FFFF', '#FFA500', '#800080', '#008000', '#FFC0CB', '#A52A2A',
  '#808080', '#FFD700', '#4B0082', '#FF1493', '#00CED1', '#32CD32'
]

function selectColor(color) {
  textColor.value = color
  showColorPicker.value = false
  emit('color', color)
}
</script>
