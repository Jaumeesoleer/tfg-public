import api from '@/api'

export const activityService = {
  getLastActivity: () => api.post('/api/activities/last-activity'),
  getActivityDetail: (activityId) =>
    api.get(`/api/activities/activity`, {
      params: { activity_id: activityId },
    }),
  getActivityPagination: (page, perPage, filter) =>
    api.post('api/activities/activities', {
      params: { page: page, per_page: perPage, filter: filter },
    }),
  uploadCSV: (formData) => api.post('api/upload/upload', formData),
  updateEffort: (perceivedEffort) => api.post('api/activities/update-effort', perceivedEffort),
}
