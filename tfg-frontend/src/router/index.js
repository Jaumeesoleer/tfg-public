// ==============================================================================
// SISTEMA DE ENRUTAMIENTO GENERAL Y CONTROL DE ACCESOS PERIMETRALES (VUE ROUTER)
// TFG: Análisis y predicción del rendimiento en corredores
// Autor: Jaume Antoni Soler Sánchez
// ==============================================================================

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    // --- GRUPO DE RUTAS PÚBLICAS / LANDING Y SECCIONES LEGALES ---
    {
      path: '/',
      meta: { HideNavBar: false },
      children: [
        { path: '', component: HomeView },
        { path: 'privacy', component: () => import('@/views/PrivacyProtocol.vue') },
        { path: 'license', component: () => import('@/views/License.vue') },
        { path: 'support', component: () => import('@/views/Support.vue') },
      ],
    },
    // --- ACCESO PERIMETRAL: MÓDULOS DE AUTENTICACIÓN Y REGISTRO ---
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { HideNavBar: true, Login: true },
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('@/views/LoginView.vue'),
      meta: { HideNavBar: true, Login: false },
    },
    // --- GRUPO DE RUTAS PRIVADAS / PROTEGIDAS (ZONA CORE DEL ATLETA) ---
    {
      path: '/dashboard',
      meta: { HideNavBar: true },
      children: [
        { path: '', component: () => import('@/views/auth/DashboardView.vue') },
        { path: 'upload', component: () => import('@/views/auth/UploadView.vue') },
        { path: 'predictor', component: () => import('@/views/auth/PredictorView.vue') },
        { path: 'activities', component: () => import('@/views/auth/ActivitiesView.vue') },
        { path: 'data', component: () => import('@/views/auth/DataView.vue') },
        { path: 'profile', component: () => import('@/views/auth/ProfileView.vue') },
        { path: 'edit-profile', component: () => import('@/views/auth/EditProfile.vue') },
        { path: 'activity', component: () => import('@/views/auth/ActivityStreamView.vue') },
      ],
    },
    // --- CONTROLADOR DE CAPTURA TOTAL (CATCH-ALL RETROCOMPATIBLE 404) ---
    {
      path: '/:pathMatch(.*)*',
      redirect: (to) => {
        return localStorage.getItem('isLoggedIn') === 'true' ? '/dashboard' : '/'
      },
    },
  ],
  // Clase de utilidad dinámica inyectada automáticamente para resaltar el menú de navegación activo
  linkExactActiveClass: 'font-semibold text-secondary-light border-b-1',
})
// --- GUARDIÁN DE NAVEGACIÓN GLOBAL ASÍNCRONO (NAVIGATION GUARD) ---
router.beforeEach((to, from) => {
  const requiresAuth = to.matched.some((record) => record.meta.isLogin)

  const isAuthenticated = localStorage.getItem('isLoggedIn') === 'true'

  if (requiresAuth && !isAuthenticated) {
    return { name: 'login' }
  } else if ((to.name === 'login' || to.name === 'signup') && isAuthenticated) {
    return '/dashboard'
  } else {
    return true
  }
})

export default router
