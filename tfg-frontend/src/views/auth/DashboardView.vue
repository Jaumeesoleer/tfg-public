<script setup>
import Sidebar from '@/components/Sidebar.vue'
import Card from '@/components/Card.vue'
import DashboardInfo from '@/components/DashboardInfo.vue'
import AuthTitle from '@/components/AuthTitle.vue'
import { useActivityStore } from '@/stores/activity'
import { computed, onMounted } from 'vue'
import DashboardGraph from '@/components/DashboardGraph.vue'

const activityStore = useActivityStore()

const activity = computed(() => activityStore.activity)
const streams = computed(() => activityStore.activityStream)
const cards = computed(() => activityStore.cards)
const userSnapshots = computed(() => activityStore.userSnapshots)

const timestamps = computed(() => {
  return streams.value.map((s) => s.timestamp) || []
})
const speedsRaw = computed(() => {
  return streams.value.map((s) => s.pace.raw)
})
const speeds = computed(() => {
  return streams.value.map((s) => s.pace.formatted)
})
const distances = computed(() => {
  return streams.value.map((s) => s.distance_m)
})
const heartrates = computed(() => {
  return streams.value.map((s) => s.heartrate)
})

onMounted(async () => {
  await activityStore.getDashboardData()
})
</script>
<template>
  <main class="bg-neutral-back-auth flex-1 flex pt-5">
    <Sidebar class="hidden md:block" />
    <div class="md:ml-64 flex-1 px-16 py-8" v-if="activity">
      <AuthTitle
        title="Arquitectura del rendimiento"
        subtitle="Análisis de varianza biométrica y cinemática de sesión para el Atleta."
      />
      <div class="mt-10">
        <div class="grid grid-cols-1 lg:grid-cols-10 gap-3">
          <div class="bg-white lg:col-span-7 p-4 overflow-x-auto">
            <div class="flex justify-between">
              <div class="">
                <div class="flex gap-2">
                  <p
                    class="bg-primary-light text-primary px-2 my-auto text-xs uppercase font-semibold"
                  >
                    Última <br />
                    Sesión
                  </p>
                  <h3 class="font-headline text-3xl font-bold">
                    {{ activity.title }}: <br />
                    Sesión #{{ activity.activity_id }}
                  </h3>
                </div>
                <p class="text-neutral font-body">
                  {{ activity.type }} · Duración: {{ activity.duration.formatted }}
                </p>
              </div>
              <div class="flex gap-3">
                <div
                  class="border-r px-3 border-neutral/60 flex flex-col justify-between xl:justify-center"
                >
                  <h4 class="uppercase text-neutral-light text-xs">FC media</h4>
                  <p class="text-3xl font-headline font-bold flex flex-col items-end">
                    {{ Math.floor(activity.heartrate.avg) }}
                    <span class="text-sm font-normal font-neutral-light">PPM</span>
                  </p>
                </div>
                <div class="flex flex-col justify-between xl:justify-center">
                  <h4 class="uppercase text-neutral-light text-xs">Eficiencia</h4>
                  <p class="text-3xl font-headline font-bold flex flex-col items-end">
                    {{ (activity.training_metrics.workout_density * 100).toFixed(2) }}
                    <span class="text-sm font-normal font-neutral-light">%</span>
                  </p>
                </div>
              </div>
            </div>
            <DashboardGraph
              :timestamps="timestamps"
              :speeds-raw="speedsRaw"
              :speeds="speeds"
              :distances-raw="distances"
              :heartrates="heartrates"
            />
          </div>

          <div class="lg:col-span-3">
            <div class="flex flex-col gap-4 p-5">
              <h4 class="font-headline font-bold text-md">Flujo de Actividad</h4>
              <div class="bg-white p-4 flex flex-col gap-2">
                <Card
                  :date="activity.date_human"
                  title="Potencia explosiva"
                  :lasts="cards.explosive_drills"
                />
              </div>
              <div class="bg-white p-4 flex flex-col gap-2">
                <Card
                  :date="activity.date_human"
                  title="Factor de eficiencia"
                  :lasts="cards.efficiency_factor"
                />
              </div>
              <div class="bg-white p-4 flex flex-col gap-2">
                <Card
                  :date="activity.date_human"
                  title="Desacoplamiento aeróbico"
                  :lasts="cards.aerobic_decoupling"
                />
              </div>
            </div>
            <div class="bg-primary-too-dark p-5 rounded-lg">
              <p
                class="font-body text-md text-primary-light/40 uppercase font-semibold tracking-widest"
              >
                Progreso del Archivo
              </p>
              
              <p class="text-sm text-primary-light text-body">
                El comportamiento con tendencia negativa del coeficiente de determinación (R 2 ) en
                el modelo de Machine Learning es un comportamiento esperado debido a las
                restricciones de escala del dataset actual (97 muestras). La fórmula de Riegel
                muestra una desviación marginal inferior al asumir una degradación de fatiga
                puramente teórica e idealizada.
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
        <DashboardInfo svg="Chrono" title="Tiempo Z2" :value="activity.zones[2].time" v="" />
        <DashboardInfo
          svg="Speed"
          title="Velocidad máxima"
          :value="activity.pace.max_formatted"
          v="/km"
        />
        <DashboardInfo
          svg="Bolt"
          title="Potencia"
          :value="
            (
              userSnapshots.weight * activity.pace.avg_raw * 1.04 +
              (userSnapshots.weight * 9.98 * activity.elevation.gain) / activity.duration.seconds
            ).toFixed(2)
          "
          v="W"
        />
        <DashboardInfo svg="Heart" title="TRIP" :value="activity.training_metrics.trimp" />
      </div>
    </div>
  </main>
</template>
