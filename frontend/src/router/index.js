import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('../views/LandingView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/ModernLoginView.vue')
  },
  {
    path: '/admin-login',
    name: 'AdminLogin',
    component: () => import('../views/AdminLoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/ModernRegisterView.vue')
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/hubs/:groupId',
    name: 'Hubs',
    component: () => import('../views/HubsViewModern.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/hubs/:groupId/channels/:channelId',
    name: 'Channel',
    component: () => import('../views/ChannelView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chat/:channelId',
    name: 'SimpleChat',
    component: () => import('../views/SimpleChat.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/direct-messages',
    name: 'DirectMessages',
    component: () => import('../views/DirectMessages.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/student-dashboard',
    name: 'StudentDashboard',
    component: () => import('../views/StudentDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/teacher-dashboard',
    name: 'TeacherDashboard',
    component: () => import('../views/TeacherDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dos-dashboard',
    name: 'DOSDashboard',
    component: () => import('../views/DOSDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/super-admin',
    name: 'SuperAdmin',
    component: () => import('../views/SuperAdminView.vue')
  },
  {
    path: '/create-group',
    name: 'CreateGroup',
    component: () => import('../views/CreateGroup.vue'),
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/admin/school-selection',
    name: 'AdminSchoolSelection',
    component: () => import('../views/AdminSchoolSelectionView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/modules',
    name: 'AdminModules',
    component: () => import('../views/AdminModulesView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/dm-requests',
    name: 'DMRequests',
    component: () => import('../views/DMRequestsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/moderation',
    name: 'Moderation',
    component: () => import('../views/ModerationView.vue'),
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/moderate-messages',
    name: 'ModerateMessages',
    component: () => import('../views/ModerateMessages.vue'),
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/upload-resource',
    name: 'UploadResource',
    component: () => import('../views/UploadResource.vue'),
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/start-session',
    name: 'StartSession',
    component: () => import('../views/StartSession.vue'),
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('../views/Reports.vue'),
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/groups/:groupId/members',
    name: 'GroupMembers',
    component: () => import('../views/GroupMembers.vue'),
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/students/:studentId/profile',
    name: 'StudentProfile',
    component: () => import('../views/StudentProfile.vue'),
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/my-resources',
    name: 'MyResources',
    component: () => import('../views/MyResources.vue'),
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/SettingsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/AdminUsersView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/reports',
    name: 'AdminAnalytics',
    component: () => import('../views/AdminAnalyticsView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/settings',
    name: 'AdminSettings',
    component: () => import('../views/AdminSettingsView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/moderation',
    name: 'AdminModeration',
    component: () => import('../views/AdminModerationView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/backup',
    name: 'AdminBackup',
    component: () => import('../views/AdminBackupView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/inter-school',
    name: 'InterSchool',
    component: () => import('../views/InterSchoolConnect.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/about-developer',
    name: 'AboutDeveloper',
    component: () => import('../views/AboutDeveloper.vue')
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/ContactView.vue')
  },
  {
    path: '/guide',
    name: 'Guide',
    component: () => import('../views/GuideView.vue')
  },
  {
    path: '/downloads',
    name: 'Downloads',
    component: () => import('../views/DownloadsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth on first load
  if (authStore.token && !authStore.user) {
    await authStore.fetchUser()
  }
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresTeacher && authStore.user?.role?.toLowerCase() !== 'teacher') {
    next('/home')
  } else if (to.meta.requiresAdmin && authStore.user?.role?.toLowerCase() !== 'admin') {
    next('/home')
  } else if ((to.path === '/' || to.path === '/login') && authStore.isAuthenticated) {
    next('/home')
  } else if (to.path === '/admin-login' && authStore.isAuthenticated && authStore.user?.role?.toLowerCase() === 'admin') {
    next('/admin-dashboard')
  } else {
    next()
  }
})

export default router
