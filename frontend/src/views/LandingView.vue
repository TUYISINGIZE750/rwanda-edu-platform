<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-300">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50 shadow-sm transition-colors duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl flex items-center justify-center shadow-lg">
              <AcademicCapIcon class="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">TSSANYWHERE</h1>
              <p class="text-xs text-gray-600 dark:text-gray-400 font-medium">{{ t('hero.description').substring(0, 20) }}...</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <select v-model="language" @change="changeLanguage" class="px-3 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600">
              <option value="en">English</option>
              <option value="rw">Kinyarwanda</option>
              <option value="fr">Français</option>
            </select>
            <button @click="toggleTheme" class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors" title="Toggle theme">
              <SunIcon v-if="isDark" class="w-6 h-6 text-gray-700 dark:text-gray-300" />
              <MoonIcon v-else class="w-6 h-6 text-gray-700" />
            </button>
            <router-link to="/guide" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors">📖 Guide</router-link>
            <router-link to="/downloads" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors">📥 Downloads</router-link>
            <router-link to="/login" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors">{{ t('nav.login') }}</router-link>
            <router-link to="/register" class="px-6 py-2.5 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-all shadow-md hover:shadow-lg">{{ t('nav.getStarted') }}</router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative bg-gradient-to-br from-blue-50 via-white to-blue-50 dark:from-gray-800 dark:via-gray-900 dark:to-gray-800 py-20 transition-colors duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <div class="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 rounded-full mb-6">
              <SparklesIcon class="w-5 h-5 text-blue-600" />
              <span class="text-sm font-semibold text-blue-700">{{ t('hero.badge') }}</span>
            </div>
            <h1 class="text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
              {{ t('hero.title') }}
            </h1>
            <p class="text-xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
              {{ t('hero.description') }}
            </p>
            <div class="flex items-center gap-4">
              <router-link to="/register" class="inline-flex items-center gap-2 px-8 py-4 bg-blue-600 text-white rounded-xl font-bold text-lg hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl">
                <RocketLaunchIcon class="w-6 h-6" />
                {{ t('hero.startLearning') }}
              </router-link>
              <router-link to="/login" class="px-8 py-4 border-2 border-gray-300 text-gray-700 rounded-xl font-bold text-lg hover:border-blue-600 hover:text-blue-600 transition-all">
                {{ t('hero.signIn') }}
              </router-link>
            </div>
          </div>
          <div class="relative overflow-hidden rounded-2xl shadow-2xl h-[500px]">
            <transition-group name="fade-slide" tag="div" class="relative w-full h-full">
              <img 
                v-for="(image, index) in images" 
                :key="image"
                v-show="currentImageIndex === index"
                :src="image" 
                alt="TVET Students" 
                class="absolute inset-0 w-full h-full object-cover"
              />
            </transition-group>
            <div class="absolute -bottom-6 -left-6 bg-white p-6 rounded-xl shadow-xl border border-gray-100 z-10">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <UserGroupIcon class="w-7 h-7 text-green-600" />
                </div>
                <div>
                  <p class="text-2xl font-bold text-gray-900">165+</p>
                  <p class="text-sm text-gray-600">{{ t('hero.schools') }}</p>
                </div>
              </div>
            </div>
            <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-10">
              <button 
                v-for="(image, index) in images" 
                :key="'dot-' + index"
                @click="currentImageIndex = index"
                class="w-2 h-2 rounded-full transition-all duration-500"
                :class="currentImageIndex === index ? 'bg-white w-8' : 'bg-white/50 hover:bg-white/75'"
              ></button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-16 bg-white dark:bg-gray-900 transition-colors duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="text-5xl font-bold text-blue-600 mb-2">165</div>
            <p class="text-gray-600 dark:text-gray-400 font-medium">{{ t('stats.schools') }}</p>
          </div>
          <div class="text-center">
            <div class="text-5xl font-bold text-green-600 mb-2">5</div>
            <p class="text-gray-600 dark:text-gray-400 font-medium">{{ t('stats.provinces') }}</p>
          </div>
          <div class="text-center">
            <div class="text-5xl font-bold text-purple-600 mb-2">100+</div>
            <p class="text-gray-600 dark:text-gray-400 font-medium">{{ t('stats.trades') }}</p>
          </div>
          <div class="text-center">
            <div class="text-5xl font-bold text-orange-600 mb-2">24/7</div>
            <p class="text-gray-600 dark:text-gray-400 font-medium">{{ t('stats.access') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 bg-gray-50 dark:bg-gray-800 transition-colors duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">{{ t('features.title') }}</h2>
          <p class="text-xl text-gray-600 dark:text-gray-300">{{ t('features.subtitle') }}</p>
        </div>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="bg-white dark:bg-gray-700 p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300">
            <div class="w-14 h-14 bg-blue-100 rounded-xl flex items-center justify-center mb-6">
              <ChatBubbleLeftRightIcon class="w-8 h-8 text-blue-600" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ t('features.communication') }}</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">{{ t('features.communicationDesc') }}</p>
          </div>
          <div class="bg-white dark:bg-gray-700 p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300">
            <div class="w-14 h-14 bg-green-100 rounded-xl flex items-center justify-center mb-6">
              <BookOpenIcon class="w-8 h-8 text-green-600" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ t('features.resources') }}</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">{{ t('features.resourcesDesc') }}</p>
          </div>
          <div class="bg-white dark:bg-gray-700 p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300">
            <div class="w-14 h-14 bg-purple-100 rounded-xl flex items-center justify-center mb-6">
              <VideoCameraIcon class="w-8 h-8 text-purple-600" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ t('features.video') }}</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">{{ t('features.videoDesc') }}</p>
          </div>
          <div class="bg-white dark:bg-gray-700 p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300">
            <div class="w-14 h-14 bg-orange-100 rounded-xl flex items-center justify-center mb-6">
              <GlobeAltIcon class="w-8 h-8 text-orange-600" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ t('features.network') }}</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">{{ t('features.networkDesc') }}</p>
          </div>
          <div class="bg-white dark:bg-gray-700 p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300">
            <div class="w-14 h-14 bg-red-100 rounded-xl flex items-center justify-center mb-6">
              <ShieldCheckIcon class="w-8 h-8 text-red-600" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ t('features.security') }}</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">{{ t('features.securityDesc') }}</p>
          </div>
          <div class="bg-white dark:bg-gray-700 p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300">
            <div class="w-14 h-14 bg-indigo-100 rounded-xl flex items-center justify-center mb-6">
              <ChartBarIcon class="w-8 h-8 text-indigo-600" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">{{ t('features.progress') }}</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">{{ t('features.progressDesc') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Image Showcase -->
    <section class="py-20 bg-white dark:bg-gray-900 transition-colors duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">{{ t('showcase.title') }}</h2>
          <p class="text-xl text-gray-600 dark:text-gray-300">{{ t('showcase.subtitle') }}</p>
        </div>
        <div class="grid md:grid-cols-2 gap-8">
          <img src="/images/IMG-20241006-WA0051.jpg" alt="TVET Workshop" class="rounded-2xl shadow-xl w-full h-80 object-cover" />
          <img src="/images/home_page_3.jpg" alt="Students Learning" class="rounded-2xl shadow-xl w-full h-80 object-cover" />
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-br from-blue-600 to-blue-800">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-4xl md:text-5xl font-bold text-white mb-6">{{ t('cta.title') }}</h2>
        <p class="text-xl text-blue-100 mb-8">{{ t('cta.subtitle') }}</p>
        <router-link to="/register" class="inline-flex items-center gap-2 px-10 py-5 bg-white text-blue-600 rounded-xl font-bold text-lg hover:bg-gray-100 transition-all shadow-2xl">
          <RocketLaunchIcon class="w-6 h-6" />
          {{ t('cta.button') }}
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 dark:bg-black text-white py-12 transition-colors duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-3 gap-8 mb-8">
          <div>
            <div class="flex items-center space-x-3 mb-4">
              <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <AcademicCapIcon class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl font-bold">TSSANYWHERE</h3>
            </div>
            <p class="text-gray-400">{{ t('footer.description') }}</p>
          </div>
          <div>
            <h4 class="font-bold mb-4">{{ t('footer.quickLinks') }}</h4>
            <ul class="space-y-2 text-gray-400">
              <li><router-link to="/login" class="hover:text-white transition-colors">{{ t('nav.login') }}</router-link></li>
              <li><router-link to="/register" class="hover:text-white transition-colors">{{ t('nav.getStarted') }}</router-link></li>
              <li><router-link to="/guide" class="hover:text-white transition-colors">User Guide</router-link></li>
              <li><router-link to="/downloads" class="hover:text-white transition-colors">Downloads</router-link></li>
            </ul>
          </div>
          <div>
            <h4 class="font-bold mb-4">{{ t('footer.contact') }}</h4>
            <p class="text-gray-400">Ministry of Education<br>Kigali, Rwanda<br>leotuyi100@outlook.com<br>+250796014801</p>
          </div>
        </div>
        <div class="border-t border-gray-800 pt-8">
          <div class="text-center text-gray-400 mb-4">
            <p>{{ t('footer.copyright') }}</p>
            <p class="mt-2 text-sm">{{ t('footer.developer') }}</p>
          </div>
          <div class="flex justify-center gap-4 text-sm">
            <router-link to="/about-developer" class="text-gray-400 hover:text-white transition-colors">{{ t('footer.aboutDeveloper') }}</router-link>
            <span class="text-gray-600">•</span>
            <router-link to="/contact" class="text-gray-400 hover:text-white transition-colors">{{ t('footer.contactLink') }}</router-link>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { 
  AcademicCapIcon, 
  SparklesIcon, 
  RocketLaunchIcon,
  UserGroupIcon,
  ChatBubbleLeftRightIcon,
  BookOpenIcon,
  VideoCameraIcon,
  GlobeAltIcon,
  ShieldCheckIcon,
  ChartBarIcon,
  MoonIcon,
  SunIcon
} from '@heroicons/vue/24/outline'
import en from '../locales/en.json'
import rw from '../locales/rw.json'
import fr from '../locales/fr.json'

const translations = { en, rw, fr }
const language = ref('en')
const images = ref([
  '/images/DSC_0106.JPG',
  '/images/IMG-20241006-WA0079.jpg',
  '/images/IMG-20241006-WA0051.jpg',
  '/images/home_page_3.jpg'
])

const currentImageIndex = ref(0)
const isDark = ref(false)
let intervalId = null

function t(key) {
  const keys = key.split('.')
  let value = translations[language.value]
  for (const k of keys) {
    if (value && typeof value === 'object') {
      value = value[k]
    } else {
      return key
    }
  }
  return value || key
}

function changeLanguage() {
  localStorage.setItem('language', language.value)
}

function toggleTheme() {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
  
  const savedLanguage = localStorage.getItem('language')
  if (savedLanguage) {
    language.value = savedLanguage
  }
  
  intervalId = setInterval(() => {
    currentImageIndex.value = (currentImageIndex.value + 1) % images.value.length
  }, 3000)
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 1.5s ease-in-out;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(30px) scale(0.95);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px) scale(0.95);
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform: translateX(0) scale(1);
}
</style>
