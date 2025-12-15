<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
    <!-- Navigation -->
    <nav class="bg-white/90 backdrop-blur-xl border-b border-blue-200 sticky top-0 z-50 shadow-lg">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <router-link to="/" class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <span class="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">TSSANYWHERE</span>
          </router-link>
          <router-link to="/" class="text-gray-700 hover:text-blue-600 font-medium transition-colors">← Back to Home</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="py-20">
      <div class="max-w-6xl mx-auto px-6">
        <div class="text-center mb-12">
          <h1 class="text-5xl font-bold text-gray-900 mb-4">Get in Touch</h1>
          <p class="text-xl text-gray-600">We'd love to hear from you</p>
        </div>

        <div class="grid lg:grid-cols-2 gap-8">
          <!-- Contact Information -->
          <div class="space-y-6">
            <!-- Platform Contact -->
            <div class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border-2 border-blue-200">
              <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <svg class="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                TSSANYWHERE Platform
              </h2>
              
              <div class="space-y-4">
                <div class="flex items-start gap-4">
                  <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="font-bold text-gray-900 mb-1">Email</h3>
                    <p class="text-gray-600">leotuyi100@outlook.com</p>
                  </div>
                </div>

                <div class="flex items-start gap-4">
                  <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="font-bold text-gray-900 mb-1">Phone</h3>
                    <p class="text-gray-600">+250796014801</p>
                  </div>
                </div>

                <div class="flex items-start gap-4">
                  <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="font-bold text-gray-900 mb-1">Address</h3>
                    <p class="text-gray-600">Ministry of Education</p>
                    <p class="text-gray-600">Kigali, Rwanda</p>
                  </div>
                </div>

                <div class="flex items-start gap-4">
                  <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="font-bold text-gray-900 mb-1">Support Hours</h3>
                    <p class="text-gray-600">Monday - Friday: 8:00 AM - 5:00 PM</p>
                    <p class="text-gray-600">Saturday: 9:00 AM - 1:00 PM</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Developer Contact -->
            <div class="bg-gradient-to-br from-indigo-600 to-purple-600 rounded-3xl shadow-2xl p-8 text-white">
              <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
                <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Contact Developer
              </h2>
              
              <div class="space-y-4">
                <div>
                  <h3 class="font-bold text-white mb-2">Leonard TUYISINGIZE</h3>
                  <p class="text-white/90 text-sm mb-4">Software Developer & Technical Trainer</p>
                </div>

                <div class="flex items-center gap-3 text-white/90">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span>leotuyi100@outlook.com</span>
                </div>

                <div class="flex items-center gap-3 text-white/90">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  <span>+250796014801</span>
                </div>

                <div class="flex items-center gap-3 text-white/90">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  </svg>
                  <span>Kigali, Rwanda</span>
                </div>

                <div class="pt-4 border-t border-white/20">
                  <router-link to="/about-developer" class="inline-flex items-center gap-2 text-white hover:text-white/80 transition-colors">
                    <span>Learn more about the developer</span>
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Contact Form -->
          <div class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border-2 border-blue-200">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Send us a Message</h2>
            
            <form @submit.prevent="submitForm" class="space-y-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
                <input v-model="form.name" type="text" required class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none transition-colors" placeholder="Your full name">
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Email Address</label>
                <input v-model="form.email" type="email" required class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none transition-colors" placeholder="your.email@example.com">
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Subject</label>
                <input v-model="form.subject" type="text" required class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none transition-colors" placeholder="What is this about?">
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Message</label>
                <textarea v-model="form.message" rows="6" required class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none transition-colors resize-none" placeholder="Tell us more..."></textarea>
              </div>

              <button type="submit" :disabled="submitting" class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed">
                <span v-if="!submitting">Send Message</span>
                <span v-else class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Sending...
                </span>
              </button>

              <p v-if="successMessage" class="text-green-600 text-center bg-green-50 p-3 rounded-xl border border-green-200">
                {{ successMessage }}
              </p>
              <p v-if="errorMessage" class="text-red-600 text-center bg-red-50 p-3 rounded-xl border border-red-200">
                {{ errorMessage }}
              </p>
            </form>
          </div>
        </div>
      </div>
    </section>

    <!-- Quick Links -->
    <section class="py-16 bg-white">
      <div class="max-w-6xl mx-auto px-6">
        <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">Quick Links</h2>
        <div class="grid md:grid-cols-3 gap-6">
          <router-link to="/about-developer" class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border-2 border-blue-200 hover:border-blue-400 hover:shadow-xl transition-all">
            <div class="text-4xl mb-3">👨‍💻</div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">About Developer</h3>
            <p class="text-gray-600 text-sm">Learn about Leonard TUYISINGIZE</p>
          </router-link>

          <router-link to="/login" class="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 border-2 border-green-200 hover:border-green-400 hover:shadow-xl transition-all">
            <div class="text-4xl mb-3">🔐</div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Login</h3>
            <p class="text-gray-600 text-sm">Access your account</p>
          </router-link>

          <router-link to="/register" class="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6 border-2 border-purple-200 hover:border-purple-400 hover:shadow-xl transition-all">
            <div class="text-4xl mb-3">🚀</div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Get Started</h3>
            <p class="text-gray-600 text-sm">Create your free account</p>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-8">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <p class="text-gray-400">© 2024 TSSANYWHERE • Technical Skills & Learning Anytime, Anywhere • Vision 2050</p>
        <p class="text-gray-500 text-sm mt-2">Developed by <span class="text-blue-400 font-semibold">Trainer Leonard TUYISINGIZE</span></p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const submitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

async function submitForm() {
  submitting.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    successMessage.value = '✅ Message sent successfully! We\'ll get back to you soon.'
    form.value = { name: '', email: '', subject: '', message: '' }
  } catch (err) {
    errorMessage.value = '❌ Failed to send message. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>
