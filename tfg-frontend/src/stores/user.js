// ==============================================================================
// ALMACÉN CENTRAL DE IDENTIDAD, PERFIL BIOMÉTRICO Y CREDENCIALES (PINIA STORE)
// TFG: Análisis y predicción del rendimiento en corredores
// Autor: Jaume Antoni Soler Sánchez
// ==============================================================================

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authService } from '@/services/auth'

export const useUserStore = defineStore('user', () => {
  const storageCache = localStorage.getItem('user_cache')
  const user = ref(storageCache ? JSON.parse(storageCache) : null)
  const isAuthenticated = ref(!!localStorage.getItem('user_cache'))
  const loading = ref(false)
  // 1. Sincroniza y persiste in-memory y en disco el snapshot informacional del corredor.
  const setUser = (userData) => {
    user.value = userData
    localStorage.setItem('user_cache', JSON.stringify(userData))
  }
  // 2. Registro de Nuevos Atletas (/register)
  const registerUser = async (userData) => {
    loading.value = true
    try {
      const response = await authService.register(userData)
      if (response.data.user) {
        setUser(response.data.user)
        isAuthenticated.value = true
      }
      return response.data
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }
  // 3. Flujo de Autenticación Convencional (/login)
  const loginUser = async (credentials) => {
    loading.value = true
    try {
      const response = await authService.login(credentials)
      setUser(response.data.user)
      isAuthenticated.value = true
      return response.data
    } finally {
      loading.value = false
    }
  }
  // 4. Sincronización Automática de Perfil (/profile)
  const fetchProfile = async () => {
    try {
      const response = await authService.getProfile()
      setUser(response.data.user_snapshots)
      isAuthenticated.value = true
    } catch (error) {
      clearUser()
    }
  }
  // 5. Mutación General de Parámetros del Corredor (/update)
  const updateProfile = async (userData) => {
    try {
      const response = await authService.update(userData)
      if (response.data.user) {
        setUser(response.data.user)
      }
    } catch (error) {
      throw error
    }
  }
  // 6. Renovación Criptográfica de Contraseñas (/update-password)
  const newPassword = async (passwordData) => {
    try {
      const response = await authService.updatePassword(passwordData)
      if (response.data.user) {
        setUser(response.data.user)
      }
    } catch (error) {
      throw error
    }
  }
  // 7. Acceso Ágil de Evaluación Académica (/demo) 
  const demoLogin = async () => {
    try {
      const response = await authService.demoLogin()
      setUser(response.data.user)
      isAuthenticated.value = true
      return response.data
    } catch (error) {
      return error
    }
  }
  // 8. Revocación Asíncrona de Credenciales (/logout)
  const logoutUser = async () => {
    try {
      await authService.logout()
    } finally {
      clearUser()
    }
  }
  // 9. Purgador del Estado de Identidad (State Clearer)
  const clearUser = () => {
    user.value = null
    isAuthenticated.value = false
    localStorage.removeItem('user_cache')
    localStorage.removeItem('token')
  }
  // 10. Modificación de Zonas de Esfuerzo Fisiológico (/update-heart-rate-data)
  const updateHeartData = async (userData) => {
    loading.value = true
    try {
      const response = await authService.updateHeartRateData(userData)
      if (response.data.user) {
        setUser(response.data.user)
      }
      return response.data
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    isAuthenticated,
    loading,
    registerUser,
    loginUser,
    fetchProfile,
    logoutUser,
    clearUser,
    updateHeartData,
    updateProfile,
    newPassword,
    demoLogin,
  }
})
