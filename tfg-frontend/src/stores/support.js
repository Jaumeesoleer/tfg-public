import { defineStore } from 'pinia'
import { ref } from 'vue'
import { SupportService } from '@/services/support'

export const useSupportStore = defineStore('support', () => {
  const loading = ref(false)
  const success = ref(false)
  // 1. Envío de Ticket de Soporte (/submit-ticket)
  const ticket = async (content) => {
    loading.value = true
    try {
      const response = await SupportService.submitTicket(content)
      success.value = response.data.success
    } catch (error) {
      success.value = false
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    success,
    ticket,
  }
})
