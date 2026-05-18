<script setup>
import Bolt from '@/assets/svg/Bolt.vue'
import Calendar from '@/assets/svg/Calendar.vue'
import Location from '@/assets/svg/Location.vue'
import AuthTitle from '@/components/AuthTitle.vue'
import BarGraph from '@/components/BarGraph.vue'
import Button from '@/components/Button.vue'
import DashboardInfo from '@/components/DashboardInfo.vue'
import LineGraph from '@/components/LineGraph.vue'
import ScattlerPoint from '@/components/ScattlerPoint.vue'
import Sidebar from '@/components/Sidebar.vue'

import { useActivityStore } from '@/stores/activity'
import { computed, onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const activityStore = useActivityStore()
const router = useRouter()
const route = useRoute()

const activity = computed(() => activityStore.activity)
const streams = computed(() => activityStore.activityStream)
const user = computed(() => activityStore.userSnapshots)

const getHeartRates = computed(() => streams.value.map((s) => s.heartrate))
const getZones = computed(() => user.value.zones)

const getPace = computed(() => streams.value.map((s) => [s.pace.raw, s.pace.formatted]))
const getAvgPace = computed(() => activity.value.pace.avg_raw)

const aerobicTime = ref(0)
const perceivedEffort = ref(0)

let activityId = route.query.activity_id

const efficiencyData = computed(() => {
  return (
    streams.value?.map((s) => ({
      x: s.heartrate,
      y: s.pace.raw,
      formattedSpeed: s.pace.formatted,
    })) || []
  )
})

const handleEffort = async () => {
  console.log(perceivedEffort.value)
  const response = await activityStore.updateEffort({
    activityId: activityId,
    effort: perceivedEffort.value,
  })
  router.go(0)
}

const getActivity = async () => {
  try {
    await activityStore.getActivity(activityId)
    perceivedEffort.value =
      activity.value.perceived_effort !== '' ? activity.value.perceived_effort : ''
    if (activity.value?.zones?.[2] && activity.value?.duration?.seconds) {
      aerobicTime.value = (
        (activity.value.zones[2].raw / activity.value.duration.seconds) *
        100
      ).toFixed(2)
    }
  } catch (error) {
    console.log(error)
  }
}
const aerobicStatus = computed(() => {
  const percentage = parseFloat(aerobicTime.value)

  if (isNaN(percentage) || percentage <= 0) {
    return { label: 'Sin datos', insight: '' }
  }

  if (percentage < 50.0) {
    return {
      label: 'mejorable',
      insight: 'Has pasado demasiado tiempo fuera de tu zona de confort aeróbico (Z2).',
    }
  } else if (percentage <= 75.0) {
    return {
      label: 'buena',
      insight:
        'Estabilidad aeróbica sólida. Ritmo bien gestionado para construir base de resistencia.',
    }
  } else {
    return {
      label: 'excelente',
      insight:
        'Disciplina óptima en Zona 2. Este es el camino para mejorar tu eficiencia cardíaca a largo plazo.',
    }
  }
})
onMounted(getActivity)
</script>

<template>
  <main class="bg-neutral-back-auth flex-1 flex pt-5">
    <Sidebar class="hidden md:block" />
    <div class="md:ml-64 flex-1 px-16 py-8">
      <div class="flex items-end justify-between">
        <div class="">
          <AuthTitle title="Morning Interval Session" />
          <div class="flex items-center gap-4">
            <Calendar />
            <p>{{ activity?.date_human }}</p>
          </div>
        </div>
        <div class="flex gap-2">
          <DashboardInfo
            :value="activity?.distance_km"
            title="Distancia"
            comp="km"
            class="border-b-2 border-neutral/40"
          />
          <DashboardInfo
            :value="activity?.duration.formatted"
            title="Duración"
            comp="min"
            class="border-b-2 border-neutral/40"
          />
          <DashboardInfo
            :value="activity?.elevation.gain"
            title="Elevación"
            comp="m"
            class="border-b-2 border-neutral/40"
          />
          <DashboardInfo
            :value="parseInt(activity?.heartrate.avg)"
            title="Pulsación media"
            comp="ppm"
            class="border-b-2 border-neutral/40"
          />
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-9 mt-6 gap-6">
        <div class="md:col-span-7">
          <div class="h-60 bg-neutral-back">
            <ScattlerPoint :data="efficiencyData" />
          </div>
          <div class="p-4 bg-neutral-back mt-6">
            <div class="flex justify-between items-center">
              <h4 class="font-headline text-xl font-bold">Telemetría</h4>
              <div class="flex items-center gap-4">
                <div class="flex items-center gap-2">
                  <div class="h-3 w-3 bg-light-green rounded-full"></div>
                  <p class="uppercase text-xs font-label">Rango óptimo</p>
                </div>
                <div class="flex items-center gap-2">
                  <div class="h-3 w-3 bg-light-yellow rounded-full"></div>
                  <p class="uppercase text-xs font-label">Aviso de umbral</p>
                </div>
                <div class="flex items-center gap-2">
                  <div class="h-3 w-3 bg-light-red rounded-full"></div>
                  <p class="uppercase text-xs font-label">Esfuerzo crítico</p>
                </div>
              </div>
            </div>
            <div class="flex justify-between mt-5">
              <p class="uppercase text-xs font-label tracking-wide font-semibold text-neutral">
                Pulsaciones (PPM)
              </p>
              <p class="text-sm text-secondary-light font-semibold font-body">
                Máximo: {{ activity?.heartrate.max }} PPM
              </p>
            </div>
            <div class="h-20 bg-neutral-back-auth w-full" v-if="getHeartRates && getZones">
              <BarGraph class="h-20" :values="getHeartRates" :zones="getZones" />
            </div>
            <div class="flex justify-between mt-5">
              <p class="uppercase text-xs font-label tracking-wide font-semibold text-neutral">
                Valocidad (min/km)
              </p>
              <p class="text-sm text-neutral font-semibold font-body">
                Media: {{ activity?.pace.avg_formatted }} min/km
              </p>
            </div>
            <div class="h-20 bg-neutral-back-auth w-full" v-if="getPace && activity">
              <LineGraph :data="getPace" :middleValue="activity.pace.avg_raw" />
            </div>
          </div>
        </div>
        <div class="md:col-span-2">
          <div class="bg-primary text-white p-4 mb-6">
            <div class="flex items-center mb-4">
              <Bolt class="fill-primary-light stroke-primary-light/0" />
              <h4 class="font-bold text-md font-headline capitalize">Eficiencia Estructural</h4>
            </div>
            <p class="text-xs font-label text-white/60 leading-relaxed">
              Estabilidad aeróbica {{ aerobicStatus.label }}. Has mantenido el {{ aerobicTime }}% de
              la duración de la sesión dentro de tu Zona 2 base.
              {{ aerobicStatus.insight }}
            </p>
            <div class="bg-neutral/30 p-3">
              <div class="flex items-center justify-between text-[10px] text-white/60">
                <p class="uppercase text-[10px] tracking-wide font-body">Índice de eficiencia</p>
                <p class="font-body">
                  {{
                    parseInt(
                      (activity?.pace.avg_raw / activity?.heartrate.avg / activity?.max_ef_index) *
                        100,
                    )
                  }}%
                </p>
              </div>
              <div class="flex items-center justify-between bg-white/30 mt-1">
                <div
                  class="h-1 bg-primary-light"
                  :style="{
                    width: `${parseInt(
                      (activity?.pace.avg_raw / activity?.heartrate.avg / activity?.max_ef_index) *
                        100,
                    )}%`,
                  }"
                ></div>
              </div>
            </div>
          </div>
          <div class="bg-neutral-back p-3">
            <p class="text-xs font-label text-neutral tracking-wider uppercase font-semibold">
              Parámetros técnicos
            </p>
            <div class="mt-3 flex flex-col gap-4 font-body">
              <div class="flex items-center justify-between">
                <div class="">
                  <h4 class="text-md capitalize font-semibold">Pendiente media</h4>
                  <p class="text-xs text-neutral -mt-1">Inclinación vertical</p>
                </div>
                <p class="text-lg font-bold">
                  {{
                    ((activity?.elevation.gain / (activity?.distance_km * 1000)) * 100).toFixed(2)
                  }}
                  <span class="text-neutral text-[10px] -ml-0.5">%</span>
                </p>
              </div>
              <div class="flex items-center justify-between">
                <div class="">
                  <h4 class="text-md capitalize font-semibold">Factor de eficiencia</h4>
                  <p class="text-xs text-neutral -mt-1">Media de Ritmo/Pulsaciones</p>
                </div>
                <p class="text-lg font-bold" v-if="activity">
                  {{
                    parseInt(((activity.pace.avg_raw * 60) / activity.heartrate.avg) * 100) / 100
                  }}
                  <span class="text-neutral text-[10px] -ml-0.5">m/puls</span>
                </p>
              </div>
              <form @submit.prevent="handleEffort" class="" v-if="activity">
                <div class="grid md:grid-cols-3 items-center justify-between">
                  <div class="md:col-span-2">
                    <h4 class="text-md capitalize font-semibold">Esfuerzo percibido</h4>
                    <p class="text-xs text-neutral -mt-1">Valor de 1-10</p>
                  </div>

                  <input
                    type="numeric"
                    class="bg-neutral/20 w-full text-right"
                    v-model.number="perceivedEffort"
                  />
                </div>
                <div class="flex mt-4 items-center justify-between border-b pb-2 border-neutral/50">
                  <div class="">
                    <h4 class="text-md capitalize font-semibold">Estres</h4>
                    <p class="text-xs text-neutral -mt-1">EP/Tiempo</p>
                  </div>
                  <p class="text-lg font-bold" v-if="perceivedEffort">
                    {{ parseInt((perceivedEffort / activity?.pace.avg_raw) * 100) / 100 }}
                  </p>
                  <p class="text-xs font-bold" v-else>Tu esfuerzo percibido</p>
                </div>
                <Button
                  content="Actualizar esfuerzo"
                  colors="bg-neutral-back-auth text-neutral"
                  border=""
                  classes="text-xs uppercase p-3 mt-4"
                  hover="hover:bg-neutral-back-auth/50"
                />
              </form>
            </div>
          </div>
        </div>
      </div>
      <div class="bg-neutral-back mt-6">
        <div class="grid md:grid-cols-9 grid-cols-1 p-6">
          <div class="md:col-span-3">
            <h4 class="text-4xl font-headline font-bold">
              Métrica  <br />
              Base
            </h4>
            <p class="font-label text-neutral text-sm max-w-xs">
              Compara el rendimiento de la sesión actual frente al comportamiento histórico de tu "Estado Estable" (Steady State) indexado en los últimos 90 días.
            </p>
            <div class="flex gap-3 items-center mt-3">
              <div class="h-4 w-4 rounded-full bg-primary-dark"></div>
              <p class="uppercase font-label font-semibold text-xs tracking-wide">
                Sessión actual
              </p>
            </div>
            <div class="flex gap-3 items-center mt-3">
              <div class="h-4 w-4 rounded-full bg-neutral/60"></div>
              <p class="uppercase font-label font-semibold text-xs tracking-wide">
                Histórico (90 días)
              </p>
            </div>
          </div>
          <div class="bg-white md:col-span-2 mx-10 flex flex-col justify-center items-center">
            <div
              class="border-3 border-neutral/30 h-25 w-25 rounded-full flex items-center justify-center"
            >
              <p class="text-xl font-bold font-body text-primary-dark">
                {{
                  (
                    (activity?.duration.seconds / activity?.stats_90d.duration_baseline) * 100 -
                    100
                  ).toFixed(1)
                }}%
              </p>
            </div>
            <p class="text-xs uppercase text-neutral font-bold font-body mt-3">Tiempo de Sesión</p>
          </div>
          <div class="bg-white md:col-span-2 mx-10 flex flex-col justify-center items-center">
            <div
              class="border-3 border-neutral/30 h-25 w-25 rounded-full flex items-center justify-center"
            >
              <p class="text-xl font-bold font-body text-primary-dark">
                {{
                  ((activity?.heartrate.avg / activity?.stats_90d.hr_baseline) * 100 - 100).toFixed(
                    1,
                  )
                }}%
              </p>
            </div>
            <p class="text-xs uppercase text-neutral font-bold font-body mt-3">Deriva cardíaca</p>
          </div>
          <div class="bg-white md:col-span-2 mx-10 flex flex-col justify-center items-center">
            <div
              class="border-3 border-neutral/30 h-25 w-25 rounded-full flex items-center justify-center"
            >
              <p class="text-xl font-bold font-body text-primary-dark">
                {{
                  (
                    (activity?.distance_km / (activity?.stats_90d.distance_baseline / 1000)) * 100 -
                    100
                  ).toFixed(1)
                }}%
              </p>
            </div>
            <p class="text-xs uppercase text-neutral font-bold font-body mt-3">VOLUMEN DE SESIÓN</p>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
