<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
    <!-- Navigation -->
    <nav class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl shadow-lg border-b border-blue-200 dark:border-gray-700 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <router-link to="/" class="flex items-center gap-2 text-blue-600 hover:text-blue-700 font-semibold">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back
          </router-link>
          <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">TSSANYWHERE Guide</h1>
          <div class="w-20"></div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-6 py-12">
      <!-- Table of Contents -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 mb-12">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">📚 Complete User Guide</h2>
        <div class="grid md:grid-cols-2 gap-4">
          <a href="#students" class="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/40 transition-all border-l-4 border-blue-600">
            <h3 class="font-bold text-blue-600 dark:text-blue-400">👨‍🎓 Student Guide</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">Learn how to access courses and collaborate</p>
          </a>
          <a href="#teachers" class="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/40 transition-all border-l-4 border-green-600">
            <h3 class="font-bold text-green-600 dark:text-green-400">👨‍🏫 Teacher Guide</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">Create classes and manage students</p>
          </a>
          <a href="#admin" class="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-900/40 transition-all border-l-4 border-purple-600">
            <h3 class="font-bold text-purple-600 dark:text-purple-400">⚙️ Admin Guide</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">Manage schools and users</p>
          </a>
          <a href="#dos" class="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg hover:bg-orange-100 dark:hover:bg-orange-900/40 transition-all border-l-4 border-orange-600">
            <h3 class="font-bold text-orange-600 dark:text-orange-400">🏛️ DOS Guide</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">District oversight and analytics</p>
          </a>
        </div>
      </div>

      <!-- Student Guide -->
      <section id="students" class="mb-12">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
          <h2 class="text-3xl font-bold text-blue-600 dark:text-blue-400 mb-6">👨‍🎓 Student Guide</h2>
          
          <div class="space-y-8">
            <!-- Step 1 -->
            <div class="border-l-4 border-blue-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Step 1: Registration</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                Click "Get Started" on the homepage and fill in your details:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>Full Name</li>
                <li>Email Address</li>
                <li>Password (minimum 6 characters)</li>
                <li>Select your Province, District, and School</li>
                <li>Choose your Trade Program and Level</li>
                <li>Select your preferred language</li>
              </ul>
              <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <p class="text-sm text-blue-700 dark:text-blue-300">💡 Tip: Make sure to select the correct school and trade program</p>
              </div>
            </div>

            <!-- Step 2 -->
            <div class="border-l-4 border-blue-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Step 2: Login & Dashboard</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                After registration, login with your email and password. You'll see your Student Dashboard with:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li><strong>Classes:</strong> View all your enrolled classes</li>
                <li><strong>Unread Messages:</strong> See new messages from teachers</li>
                <li><strong>Resources:</strong> Access study materials</li>
                <li><strong>Activity Feed:</strong> Track recent activities</li>
              </ul>
            </div>

            <!-- Step 3 -->
            <div class="border-l-4 border-blue-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Step 3: Join Classes</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                Classes are automatically added based on your school and trade. You can:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>View class announcements</li>
                <li>Access discussion channels</li>
                <li>Download resources</li>
                <li>Participate in live sessions</li>
              </ul>
            </div>

            <!-- Step 4 -->
            <div class="border-l-4 border-blue-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Step 4: Communicate</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                Use the messaging system to:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>Send direct messages to teachers</li>
                <li>Participate in group discussions</li>
                <li>Share files and resources</li>
                <li>Join live video sessions</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Teacher Guide -->
      <section id="teachers" class="mb-12">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
          <h2 class="text-3xl font-bold text-green-600 dark:text-green-400 mb-6">👨‍🏫 Teacher Guide</h2>
          
          <div class="space-y-8">
            <!-- Step 1 -->
            <div class="border-l-4 border-green-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Step 1: Registration</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                Register as a teacher with your school details. You'll need:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>Full Name</li>
                <li>Email Address</li>
                <li>Password</li>
                <li>Select your School</li>
              </ul>
            </div>

            <!-- Step 2 -->
            <div class="border-l-4 border-green-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Step 2: Teacher Dashboard</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                Access your Teacher Dashboard to manage:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li><strong>My Classes:</strong> View and manage your classes</li>
                <li><strong>Groups & Clubs:</strong> Create and manage student groups</li>
                <li><strong>Students:</strong> View enrolled students</li>
                <li><strong>Resources:</strong> Upload study materials</li>
              </ul>
            </div>

            <!-- Step 3 -->
            <div class="border-l-4 border-green-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Step 3: Create a Class/Group</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                Click "Create Group" and fill in:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>Group Name (e.g., "Welding Level 2")</li>
                <li>Description</li>
                <li>Group Type (Class, Club, or Discussion)</li>
              </ul>
              <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                <p class="text-sm text-green-700 dark:text-green-300">💡 Tip: Default channels (Announcements, Discussion, Resources) are created automatically</p>
              </div>
            </div>

            <!-- Step 4 -->
            <div class="border-l-4 border-green-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Step 4: Manage Students</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                Add students to your class by:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>Going to Group Members</li>
                <li>Searching for students by email</li>
                <li>Adding them to your class</li>
              </ul>
            </div>

            <!-- Step 5 -->
            <div class="border-l-4 border-green-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Step 5: Upload Resources</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                Share learning materials:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>Click "Upload Resource"</li>
                <li>Select your class/group</li>
                <li>Upload files (PDF, images, videos)</li>
                <li>Add descriptions</li>
              </ul>
            </div>

            <!-- Step 6 -->
            <div class="border-l-4 border-green-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Step 6: Start Live Sessions</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                Conduct live classes:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>Click "Start Session"</li>
                <li>Select your class</li>
                <li>Share your screen or video</li>
                <li>Students can join and interact</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Admin Guide -->
      <section id="admin" class="mb-12">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
          <h2 class="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-6">⚙️ Admin Guide</h2>
          
          <div class="space-y-8">
            <div class="border-l-4 border-purple-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Admin Dashboard Features</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                As an admin, you can:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li><strong>Manage Users:</strong> Add, edit, or remove users</li>
                <li><strong>Manage Schools:</strong> Add schools and configure settings</li>
                <li><strong>View Analytics:</strong> See platform usage statistics</li>
                <li><strong>Moderate Content:</strong> Review and approve messages</li>
                <li><strong>System Settings:</strong> Configure platform settings</li>
              </ul>
            </div>

            <div class="border-l-4 border-purple-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Add New School</h3>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>Go to Admin Dashboard</li>
                <li>Click "Manage Schools"</li>
                <li>Fill in school details</li>
                <li>Select available trade programs</li>
                <li>Save and activate</li>
              </ul>
            </div>

            <div class="border-l-4 border-purple-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Manage Users</h3>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>View all registered users</li>
                <li>Assign roles (Student, Teacher, Admin)</li>
                <li>Deactivate inactive accounts</li>
                <li>View user activity logs</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- DOS Guide -->
      <section id="dos" class="mb-12">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
          <h2 class="text-3xl font-bold text-orange-600 dark:text-orange-400 mb-6">🏛️ DOS (District Officer) Guide</h2>
          
          <div class="space-y-8">
            <div class="border-l-4 border-orange-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">DOS Dashboard</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">
                Monitor district-wide activities:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li><strong>District Overview:</strong> View all schools in your district</li>
                <li><strong>Student Statistics:</strong> Track enrollment and progress</li>
                <li><strong>Teacher Performance:</strong> Monitor teacher activities</li>
                <li><strong>Reports:</strong> Generate district reports</li>
              </ul>
            </div>

            <div class="border-l-4 border-orange-600 pl-6">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">View Analytics</h3>
              <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 mb-4">
                <li>Total students and teachers</li>
                <li>Active classes and sessions</li>
                <li>Resource usage statistics</li>
                <li>Student engagement metrics</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Common Features -->
      <section class="mb-12">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">🎯 Common Features for All Users</h2>
          
          <div class="grid md:grid-cols-2 gap-8">
            <div class="border-l-4 border-blue-600 pl-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">📱 Direct Messaging</h3>
              <p class="text-gray-600 dark:text-gray-400">
                Send private messages to other users. Click on any user profile and select "Send Message".
              </p>
            </div>

            <div class="border-l-4 border-green-600 pl-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">📁 File Sharing</h3>
              <p class="text-gray-600 dark:text-gray-400">
                Share documents, images, and videos in channels. Supported formats: PDF, DOC, JPG, PNG, MP4, MP3.
              </p>
            </div>

            <div class="border-l-4 border-purple-600 pl-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">🔔 Notifications</h3>
              <p class="text-gray-600 dark:text-gray-400">
                Get real-time notifications for messages, announcements, and session invitations.
              </p>
            </div>

            <div class="border-l-4 border-orange-600 pl-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">🌐 Language Support</h3>
              <p class="text-gray-600 dark:text-gray-400">
                Switch between English, Kinyarwanda, and French in your settings.
              </p>
            </div>

            <div class="border-l-4 border-red-600 pl-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">🔒 Security</h3>
              <p class="text-gray-600 dark:text-gray-400">
                Your data is encrypted and protected. Change your password regularly in settings.
              </p>
            </div>

            <div class="border-l-4 border-indigo-600 pl-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">🎨 Dark Mode</h3>
              <p class="text-gray-600 dark:text-gray-400">
                Toggle dark mode in the navigation bar for comfortable viewing.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section class="mb-12">
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">❓ Frequently Asked Questions</h2>
          
          <div class="space-y-4">
            <details class="border-l-4 border-blue-600 pl-6 pb-4">
              <summary class="font-bold text-gray-900 dark:text-white cursor-pointer">How do I reset my password?</summary>
              <p class="text-gray-600 dark:text-gray-400 mt-2">
                Click "Forgot Password" on the login page, enter your email, and follow the instructions sent to your email.
              </p>
            </details>

            <details class="border-l-4 border-green-600 pl-6 pb-4">
              <summary class="font-bold text-gray-900 dark:text-white cursor-pointer">Can I join multiple classes?</summary>
              <p class="text-gray-600 dark:text-gray-400 mt-2">
                Yes! Students can be part of multiple classes. Teachers can manage multiple classes and groups.
              </p>
            </details>

            <details class="border-l-4 border-purple-600 pl-6 pb-4">
              <summary class="font-bold text-gray-900 dark:text-white cursor-pointer">How do I download resources?</summary>
              <p class="text-gray-600 dark:text-gray-400 mt-2">
                Go to the Resources channel in your class, find the file, and click the download button.
              </p>
            </details>

            <details class="border-l-4 border-orange-600 pl-6 pb-4">
              <summary class="font-bold text-gray-900 dark:text-white cursor-pointer">What if I have technical issues?</summary>
              <p class="text-gray-600 dark:text-gray-400 mt-2">
                Contact your school admin or email leotuyi100@outlook.com with details of the issue.
              </p>
            </details>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl shadow-lg p-8 text-center text-white mb-12">
        <h2 class="text-3xl font-bold mb-4">Ready to Get Started?</h2>
        <p class="text-lg mb-6">Join TSSANYWHERE today and start your learning journey!</p>
        <router-link to="/register" class="inline-block px-8 py-3 bg-white text-blue-600 rounded-lg font-bold hover:bg-gray-100 transition-all">
          Create Your Account
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('students')
</script>

<style scoped>
details summary::-webkit-details-marker {
  display: none;
}

details summary::before {
  content: '▶ ';
  display: inline-block;
  transition: transform 0.3s;
  margin-right: 0.5rem;
}

details[open] summary::before {
  transform: rotate(90deg);
}
</style>
