// ==============================================================================
// ALMACÉN CENTRAL DE ESTADO REACTIVO PARA MODELOS Y SIMULACIONES (PINIA STORE)
// TFG: Análisis y predicción del rendimiento en corredores
// Autor: Jaume Antoni Soler Sánchez
// ==============================================================================

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { PredictionService } from '@/services/prediction'

export const usePredictionStore = defineStore('prediction', () => {
  const prediction = ref(false)
  const predictionSnapshots = ref(null) 
  const model = ref(null)
  const loading = ref(false)

  // 1. Carga Inicial de la API (/check)
  const checkPrediction = async () => {
    loading.value = true
    try {
      const response = await PredictionService.checkPrediction()
      prediction.value = response.data.prediction
      predictionSnapshots.value = response.data.PredictionSnapshots
      model.value = response.data.ModelSnapshots
    } catch (error) {
      console.error('Error en checkPrediction:', error)
    } finally {
      loading.value = false
    }
  }

  // 2. Predicción Oficial Real
  const predict = async (prediction) => {
    loading.value = true
    try {
      const response = await PredictionService.predict(prediction)
      // Sincronizamos la respuesta real si tu backend devuelve el snapshot completo
      predictionSnapshots.value = response.data.PredictionSnapshots
    } catch (error) {
      console.error('Error en predict:', error)
    } finally {
      loading.value = false
    }
  }

  // 3. Laboratorio de Simulación (El que dispara el formulario)
  const simulate = async (simulation) => {
    loading.value = true
    try {
      const response = await PredictionService.simulate(simulation)
      if (model.value && response.data?.ml_points) {
        model.value.ml_points = response.data.ml_points
      }

      console.log('¡Simulación inyectada con éxito en el modelo reactivo!')
    } catch (error) {
      console.error('Error en la ejecución del simulador:', error)
    } finally {
      loading.value = false
    }
  }

  return {
    prediction,
    predictionSnapshots,
    model,
    loading,
    checkPrediction,
    predict,
    simulate,
  }
})
