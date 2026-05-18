// ==============================================================================
// CLIENTE INTERMEDIO HTTP Y ARQUITECTURA DE INTERCEPTORES DE RED (AXIOS)
// TFG: Análisis y predicción del rendimiento en corredores
// Autor: Jaume Antoni Soler Sánchez
// ==============================================================================

import axios from 'axios'
import router from '@/router'

const API_URL = import.meta.env.VITE_API_URL
console.log(API_URL)
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  xsrfCookieName: 'csrf_access_token',
  xsrfHeaderName: 'X-CSRF-TOKEN',
})
// --- PIPELINE DE INTERCEPCIÓN ASÍNCRONA DE RESPUESTAS (MANEJO DE TOKENS) ---
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    if (error.response && error.response.status === 401) {
      if (originalRequest.url.includes('/api/auth/refresh')) {
        console.error('EL refresh ha fallado')
        handleLogout()
        return Promise.reject(error)
      }
      // Implementación del patrón reintento unificado (Retry Pattern)
      if (!originalRequest._retry) {
        originalRequest._retry = true

        try {
          await api.post('/api/auth/refresh')
          return api(originalRequest)
        } catch (refreshError) {
          handleLogout()
          return Promise.reject(refreshError)
        }
      }
    } else {
      handleLogout()
    }
    return Promise.reject(error)
  },
)
/**
 * Purga las banderas de estado in-memory y redirige defensivamente al corredor a la raíz de la SPA.
 */
function handleLogout() {
  localStorage.removeItem('isLoggedIn')
  router.push('/')
}

export default api
