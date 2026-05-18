// ==============================================================================
// ALMACÉN CENTRAL DE ESTADO RECTIVO DE ENTRENAMIENTOS Y TELEMETRÍA (PINIA STORE)
// TFG: Análisis y predicción del rendimiento en corredores
// Autor: Jaume Antoni Soler Sánchez
// ==============================================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { activityService } from '@/services/activity'
import { useUserStore } from './user'

export const useActivityStore = defineStore('activity', () => {
  const userStore = useUserStore()
  const activity = ref(null)
  const activities = ref([])
  const cards = ref([])
  const userSnapshots = ref([])
  const activityStream = ref([])
  const loading = ref(false)
  const pagination = ref([])
  const audit = ref([])

  const currentUser = computed(() => userStore.user)
  // 1. Ingesta del Dashboard Inicial (/last-activity)
  const getDashboardData = async () => {
    loading.value = true
    try {
      const response = await activityService.getLastActivity()
      activity.value = response.data.activity
      activityStream.value = response.data.streams
      cards.value = response.data.streams_card
      userSnapshots.value = response.data.user_snapshots
    } catch (error) {
      console.error(error)
    } finally {
      loading.value = false
    }
  }
  // 2. Histórico de Actividades Paginado (/activities)
  const getActivityPagination = async (page, perPage, filter) => {
    try {
      const response = await activityService.getActivityPagination(page, perPage, filter)
      activities.value = response.data.activities
      pagination.value = response.data.pagination
      audit.value = response.data.audit
    } catch (error) {
      console.error(error)
    }
  }
  // 3. Extracción de Detalle de Actividad Específica (/activity)
  const getActivity = async (activityId) => {
    try {
      const response = await activityService.getActivityDetail(activityId)
      activity.value = response.data.activity
      activityStream.value = response.data.streams
      userSnapshots.value = response.data.user_snapshots
    } catch (error) {
      console.log(error)
    }
  }
  // 4. Actualización Escala de Esfuerzo Subjetivo RPE (/update-effort)
  const updateEffort = async (perceivedEffort) => {
    loading.value = true
    try {
      const response = await activityService.updateEffort(perceivedEffort)
      if (response.data.activity) {
        activity.value = response.activity.user
      }
      return response.data
    } catch (error) {
      return error
    } finally {
      loading.value = false
    }
  }

  return {
    activity,
    activities,
    activityStream,
    currentUser,
    cards,
    userSnapshots,
    pagination,
    audit,
    getDashboardData,
    getActivityPagination,
    getActivity,
    updateEffort,
  }
})
