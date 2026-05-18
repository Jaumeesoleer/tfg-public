import api from '@/api'
import PasswordModal from '@/components/PasswordModal.vue'

export const authService = {
  login: (credentials) => api.post('/api/auth/login', credentials),
  register: (userData) => api.post('/api/auth/register', userData),
  logout: () => api.post('/api/auth/logout'),
  refresh: () => api.post('/api/auth/refresh'),
  getProfile: () => api.get('/api/auth/profile'),
  updateHeartRateData: (userData) => api.post('api/auth/update-heart-rate-data', userData),
  update: (userData) => api.post('api/auth/update', userData),
  updatePassword: (passwordData) => api.post('api/auth/update-password', passwordData),
  demoLogin: () => api.post('/api/auth/demo'),
}
