import api from '@/api'

export const SupportService = {
  submitTicket: (content) => api.post('api/support/submit-ticket', content)
}
