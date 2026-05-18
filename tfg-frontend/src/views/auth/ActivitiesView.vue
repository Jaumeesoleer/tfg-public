<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import Calendar from '@/assets/svg/Calendar.vue'
import Heart from '@/assets/svg/Heart.vue'
import Left from '@/assets/svg/Left.vue'
import Right from '@/assets/svg/Right.vue'
import { RouterLink, useRoute } from 'vue-router'
import Square from '@/components/Square.vue'
import Sidebar from '@/components/Sidebar.vue'
import AuthTitle from '@/components/AuthTitle.vue'
import { useActivityStore } from '@/stores/activity'
import { parse } from 'vue/compiler-sfc'

const activityStore = useActivityStore()
const route = useRoute()
const loading = ref(true)
const activities = computed(() => activityStore.activities)
const pagination = computed(() => activityStore.pagination)
const error = ref(null)
const audit = computed(() => activityStore.audit)

const perPage = ref(10)
let filter = route.query.filter || '30_last_days'

const pace = (pace) => {
  let p = pace.split(':')
  let min = parseInt(p[0], 10)
  return `${min}'${p[1]}"`
}
const getFilterClass = (filterType) => {
  const baseClass = 'capitalize p-1 md:p-2 flex flex-1 items-center md:text-xs'
  if (filter === filterType) {
    return `
      ${baseClass}
      bg-white   sm:py-3  text-secondary-light stroke-secondary-light shadow-md/30  gap-2
    `
  } else {
    return `${baseClass} sm:py-2 text-neutral bg-neutral-light/40`
  }
}
const loadActivities = async () => {
  loading.value = true
  let page = parseInt(route.query.page) || 1
  filter = route.query.filter || '30_last_days'

  try {
    await activityStore.getActivityPagination(page, perPage.value, filter)
    page = pagination.current_page
  } catch (err) {
    error.value = 'No se han podido cargar las actividades'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const auditTextHtml = computed(() => {
  const inc = audit?.inc_intensity ?? 0
  const name = audit?.last_thre_name ?? 'Threshold Run'
  const vcl = audit?.calc_var ?? 0

  const tipoCarga = inc >= 0 ? 'aumento' : 'descenso'
  const valorAbsoluto = Math.abs(inc)

  return `La carga de trabajo total para el periodo seleccionado muestra un <strong>${tipoCarga}</strong> del 
  <span>${valorAbsoluto}%</span> 
  en intervalos de alta intensidad en comparación con la línea base de los 30 días anteriores. 
  La consistencia de la velocidad de carrera en la serie 
  <span>${name}</span> 
  se mantiene estable con una varianza del 
  <span>${vcl}%</span>, 
  lo que sugiere protocolos de adaptación óptimos.`
})

watch(
  () => route.query,
  () => {
    loadActivities()
  },
  { deep: true },
)
onMounted(loadActivities)
</script>
<template>
  <main class="flex-1 pb-10 pt-5 bg-neutral-back-auth">
    <div class="gap-6">
      <Sidebar class="hidden md:block" />ß
      <div class="md:ml-64 px-16">
        <AuthTitle title="Archivo de sesiones" subtitle="Repositorio de datos históricos" />
        <div
          class="flex my-10 font-body items-stretch md:items-center gap-4 text-[10px] sm:text-xs font-semibold tracking-wider sm:max-w-3/4"
        >
          <p class="sm:py-2 uppercase text-neutral-light hidden sm:flex items-center">filters:</p>
          <RouterLink
            :to="{ path: '/dashboard/activities', query: { filter: '30_last_days' } }"
            :class="[getFilterClass('30_last_days')]"
            exact-active-class=""
          >
            <Calendar class="hidden md:flex w-4 y-4 lg:w-5 lg:y-5" /> <span>Últimos 30 días</span>
          </RouterLink>

          <RouterLink
            :to="{ path: '/dashboard/activities', query: { filter: 'high_intensity' } }"
            :class="[getFilterClass('high_intensity')]"
            exact-active-class=""
          >
            Intensidad alta
          </RouterLink>
          <RouterLink
            :to="{ path: '/dashboard/activities', query: { filter: 'recovery' } }"
            :class="[getFilterClass('recovery')]"
            exact-active-class=""
          >
            Recuperación
          </RouterLink>
          <RouterLink
            :to="{ path: '/dashboard/activities', query: { filter: 'aerobic' } }"
            :class="[getFilterClass('aerobic')]"
            exact-active-class=""
          >
            Base aeróbica
          </RouterLink>
        </div>
        <div v-if="loading">Cargando tus carreras...</div>
        <div v-else-if="error" class="error-msg">{{ error }}</div>
        <div v-else class="overflow-x-auto">
          <table
            v-if="activities"
            class="table-auto lg:table-layout bg-white shadow-md/30 min-w-200 w-full"
          >
            <thead class="text-neutral-light font-label text-[10px] uppercase tracking-widest">
              <tr>
                <th class="text-left p-2">Fecha / Session Id</th>
                <th class="text-left py-2">Nombre</th>
                <th class="py-2">Distancia (km)</th>
                <th class="py-2">Avg Heart rate</th>
                <th class="py-2">Ritmo medio</th>
                <th class="text-right p-2">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="activity in activities" :key="activity.activity_id">
                <td
                  class="flex flex-col p-2 text-secondary-light font-body text-left uppercase font-bold"
                >
                  {{ activity.date_human
                  }}<span class="text-[10px] text-neutral-light/60"
                    >#{{ activity.activity_id }}</span
                  >
                </td>
                <td class="text-left font-bold font-label">
                  {{ activity.title }}
                </td>
                <td class="font-bold text-center">
                  {{ activity.distance_km
                  }}<span class="text-[10px] text-neutral-light uppercase"> km</span>
                </td>
                <td v-if="activity.heartrate.avg > 0">
                  <div class="flex items-center gap-2 justify-center h-full">
                    <Heart class="w-5 h-5 group-hover:animate-pulse" />
                    <p class="font-bold">
                      {{ parseInt(activity.heartrate.avg) }}
                      <span class="text-[10px] text-neutral-light uppercase">bpm</span>
                    </p>
                  </div>
                </td>
                <td v-else></td>

                <td class="text-center font-bold">
                  {{ pace(activity.pace.avg_formatted)
                  }}<span class="text-[10px] text-neutral-light uppercase">/km</span>
                </td>
                <th>
                  <div class="mx-3 my-1 flex">
                    <RouterLink
                      class="uppercase text-white mx-2 text-sm py-1 w-full bg-primary-semi-light/90 hover:bg-primary-semi-light/70"
                      :to="{
                        path: '/dashboard/activity',
                        query: { activity_id: activity.activity_id },
                      }"
                    >
                      View report
                    </RouterLink>
                  </div>
                </th>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="6">
                  <p
                    v-if="activities.length === 0 && !loading"
                    class="uppercase font-label font-semibold text-secondary-semi-light text-center pb-2"
                  >
                    Aún no tienes actividades. ¡Sube tu primer CSV!
                  </p>
                  <div class="flex justify-between m-4 items-center" v-if="activities.length != 0">
                    <p class="text-xs text-neutral font-label">
                      Mostrando {{ pagination.total_page_items }} de
                      {{ pagination.total_items }} sesiones
                    </p>

                    <div class="flex gap-2 items-center font-xs font-label">
                      <RouterLink
                        v-if="pagination.has_prev"
                        :to="{
                          path: '/dashboard/activities',
                          query: { page: pagination.current_page - 1, filter: filter },
                        }"
                        exact-active-class=""
                      >
                        <Left class="hover:stroke-neutral/60 stroke-neutral" />
                      </RouterLink>
                      <RouterLink
                        v-if="pagination.has_prev"
                        :to="{
                          path: '/dashboard/activities',
                          query: { page: pagination.current_page - 1, filter: filter },
                        }"
                        exact-active-class=""
                      >
                        <p class="py-1 px-3 hover:bg-secondary-light/20 hover:rounded-sm">
                          {{ pagination.current_page - 1 }}
                        </p>
                      </RouterLink>

                      <p class="bg-secondary-light py-1 px-3 text-white rounded-sm">
                        {{ pagination.current_page }}
                      </p>
                      <RouterLink
                        v-if="pagination.has_next"
                        :to="{
                          path: '/dashboard/activities',
                          query: { page: pagination.current_page + 1, filter: filter },
                        }"
                        exact-active-class=""
                      >
                        <p class="py-1 px-3 hover:bg-secondary-light/20 hover:rounded-sm">
                          {{ pagination.current_page + 1 }}
                        </p>
                      </RouterLink>
                      <RouterLink
                        exact-active-class=""
                        v-if="pagination.has_next"
                        :to="{
                          path: '/dashboard/activities',
                          query: { page: pagination.current_page + 1, filter: filter },
                        }"
                      >
                        <Right class="hover:stroke-neutral/60 stroke-neutral" />
                      </RouterLink>
                    </div>
                  </div>
                </td>
              </tr>
            </tfoot>
          </table>
        </div>

        <section>
          <div class="grid grid-cols-1 lg:grid-cols-12 mt-10 gap-6">
            <Square
              title="Auditoría de inteligencia de archivo"
              :text="auditTextHtml"
              bgColor="bg-white/80"
              class="lg:col-span-8 border-l-2 border-neutral-light/70"
              title-color="text-secondary-light font-semibold text-md"
              text-color="text-primary-dark"
              :tips="true"
              :html="true"
              :hr="parseInt(audit?.avg_hr)"
              :eff="parseFloat(audit?.avg_efficiency).toFixed(4)"
            />
            <Square
              svg="Cloud"
              title="Integridad del respaldo"
              text-color="text-white"
              title-color="text-white font-semibold"
              class="lg:col-span-4"
              text="Todas las sesiones están firmadas criptográficamente y cuentan con una copia de seguridad en el repositorio seguro en la nube del laboratorio."
            />
          </div>
        </section>
      </div>
    </div>
  </main>
</template>
