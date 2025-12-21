<template>
  <div v-if="isWakingUp" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-8 max-w-md mx-4 text-center">
      <div class="mb-4">
        <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto"></div>
      </div>
      <h3 class="text-xl font-bold text-gray-900 mb-2">Waking up server...</h3>
      <p class="text-gray-600 mb-4">This may take up to 60 seconds on first visit</p>
      <div class="text-sm text-gray-500">
        Attempt {{ currentAttempt }} of 20
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { wakeUpServer } from '../utils/serverWakeUp';

const isWakingUp = ref(true);
const currentAttempt = ref(1);

let attemptInterval;

onMounted(async () => {
  attemptInterval = setInterval(() => {
    if (currentAttempt.value < 20) {
      currentAttempt.value++;
    }
  }, 3000);

  const result = await wakeUpServer();
  
  clearInterval(attemptInterval);
  isWakingUp.value = false;
  
  if (!result.success) {
    console.error('Server wake-up failed:', result.error);
  }
});
</script>
