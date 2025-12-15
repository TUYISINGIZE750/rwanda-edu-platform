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
      <div class="max-w-5xl mx-auto px-6">
        <div class="text-center mb-12">
          <h1 class="text-5xl font-bold text-gray-900 mb-4">About the Developer</h1>
          <p class="text-xl text-gray-600">Meet the mind behind TSSANYWHERE</p>
        </div>

        <!-- Developer Profile -->
        <div class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl overflow-hidden border-2 border-blue-200">
          <div class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 p-8 text-white">
            <div class="flex items-center gap-6">
              <div class="w-32 h-32 bg-white/20 backdrop-blur-xl rounded-full flex items-center justify-center text-6xl font-bold border-4 border-white/30">
                LT
              </div>
              <div>
                <h2 class="text-4xl font-bold mb-2">Leonard TUYISINGIZE</h2>
                <p class="text-xl text-white/90 mb-2">Software Developer & Technical Trainer</p>
                <div class="flex items-center gap-4 text-sm">
                  <span class="flex items-center gap-1">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    Kigali, Rwanda
                  </span>
                  <span class="flex items-center gap-1">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    Technical Trainer
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="p-8">
            <!-- About Section -->
            <div class="mb-8">
              <h3 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <svg class="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                About Leonard
              </h3>
              <p class="text-gray-700 leading-relaxed mb-4">
                Leonard TUYISINGIZE is a passionate software developer and technical trainer dedicated to transforming education through technology. With extensive experience in full-stack development and a deep understanding of Rwanda's TVET/TSS education system, Leonard designed and built TSSANYWHERE to bridge the gap between traditional classroom learning and modern digital education.
              </p>
              <p class="text-gray-700 leading-relaxed">
                His vision is to ensure that every technical student in Rwanda has access to quality education resources anytime, anywhere - during holidays, after school, or whenever they need to learn.
              </p>
            </div>

            <!-- Expertise -->
            <div class="mb-8">
              <h3 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <svg class="w-7 h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
                Technical Expertise
              </h3>
              <div class="grid md:grid-cols-2 gap-4">
                <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4 border-2 border-blue-200">
                  <h4 class="font-bold text-gray-900 mb-2">Frontend Development</h4>
                  <p class="text-sm text-gray-600">Vue.js, React, Tailwind CSS, Modern UI/UX Design</p>
                </div>
                <div class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-4 border-2 border-green-200">
                  <h4 class="font-bold text-gray-900 mb-2">Backend Development</h4>
                  <p class="text-sm text-gray-600">Python, FastAPI, Node.js, RESTful APIs</p>
                </div>
                <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 border-2 border-purple-200">
                  <h4 class="font-bold text-gray-900 mb-2">Database & Cloud</h4>
                  <p class="text-sm text-gray-600">PostgreSQL, Redis, AWS, Cloud Architecture</p>
                </div>
                <div class="bg-gradient-to-br from-orange-50 to-red-50 rounded-xl p-4 border-2 border-orange-200">
                  <h4 class="font-bold text-gray-900 mb-2">Education Technology</h4>
                  <p class="text-sm text-gray-600">E-Learning Platforms, LMS, Educational Tools</p>
                </div>
              </div>
            </div>

            <!-- Project Impact -->
            <div class="mb-8">
              <h3 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <svg class="w-7 h-7 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                TSSANYWHERE Impact
              </h3>
              <div class="grid grid-cols-3 gap-4">
                <div class="text-center bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border-2 border-blue-200">
                  <div class="text-4xl font-bold text-blue-600 mb-2">165</div>
                  <p class="text-sm text-gray-700 font-medium">TVET/TSS Schools</p>
                </div>
                <div class="text-center bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 border-2 border-green-200">
                  <div class="text-4xl font-bold text-green-600 mb-2">5</div>
                  <p class="text-sm text-gray-700 font-medium">Provinces Covered</p>
                </div>
                <div class="text-center bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6 border-2 border-purple-200">
                  <div class="text-4xl font-bold text-purple-600 mb-2">24/7</div>
                  <p class="text-sm text-gray-700 font-medium">Learning Access</p>
                </div>
              </div>
            </div>

            <!-- Vision -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 text-white">
              <h3 class="text-2xl font-bold mb-3">Vision for Rwanda's Education</h3>
              <p class="text-white/90 leading-relaxed">
                "My vision is to ensure that every technical student in Rwanda has the opportunity to learn and grow, regardless of time or location. TSSANYWHERE is not just a platform - it's a movement towards continuous, accessible, and quality technical education that aligns with Rwanda's Vision 2050."
              </p>
              <p class="text-white/80 text-sm mt-4 italic">- Leonard TUYISINGIZE</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact CTA -->
    <section class="py-16 bg-white">
      <div class="max-w-4xl mx-auto px-6 text-center">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">Get in Touch</h2>
        <p class="text-gray-600 mb-8">Have questions about TSSANYWHERE or want to collaborate?</p>
        <router-link to="/contact" class="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-bold text-lg hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg hover:shadow-xl">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          Contact Developer
        </router-link>
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
// No additional logic needed for this static page
</script>
