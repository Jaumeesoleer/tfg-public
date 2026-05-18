import api from '@/api'

export const PredictionService = {
  checkPrediction: () => api.get('/api/prediction/check'),
  predict: (prediction) => api.post('/api/prediction/prediction', prediction),
  simulate: (simulation) => api.post('/api/prediction/simulate', simulation),
}
