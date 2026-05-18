<script setup>
import AuthTitle from '@/components/AuthTitle.vue'
import Sidebar from '@/components/Sidebar.vue'
import Button from '@/components/Button.vue'
import DataLabels from '@/components/DataLabels.vue'
import Blockquote from '@/assets/svg/Blockquote.vue'
import Science from '@/assets/svg/Science.vue'
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import DataTable from '@/components/DataTable.vue'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const max_hr = ref('')
const rest_hr = ref('')
const zones = ref([])
const errorMessage = ref('')

const handleUpdate = async () => {
  try {
    const response = await userStore.updateHeartData({
      max_hr: max_hr.value,
      rest_hr: rest_hr.value,
      custome_zones: zones.value.map((z) => ({
        min: parseInt(z.min),
        max: parseInt(z.max),
      })),
    })
    router.go(0)
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Error al conectar con el servidor'
  }
}

const user = computed(() => userStore.user)

onMounted(async () => {
  await userStore.fetchProfile()
  if (user) {
    max_hr.value = user.value.max_hr
    rest_hr.value = user.value.rest_hr ?? 60
    zones.value = user.value.zones
  }
})
</script>
<template>
  <main class="flex-1 bg-neutral-back-auth pt-5">
    <Sidebar class="hidden md:block" />
    <div class="grid grid-cols-1 lg:grid-cols-4 md:ml-64 md:pl-13 lg:px-16 p-4 md:py-8 gap-10">
      <div class="md:col-span-3">
        <div class="">
          <AuthTitle
            title="Parámetros fisiológicos"
            subtitle="Datos fundamentales para el modelado de estrés cardíaco"
          />
          <form action="" class="bg-neutral-back/60 p-10 grid grid-cols-2 gap-5 mt-4 rounded-md">
            <DataLabels
              title="Frecuencia cardíaca máxima (FC máx)"
              text="Valor de esfuerzo pico, calculado o medido"
              id="max_hr"
              placeholder="194"
              v-model="max_hr"
            />
            <DataLabels
              title="Frecuencia cardíaca en reposo (FCR)"
              text="Ritmo cardíaco metabólico basal en estado de reposo absoluto."
              placeholder="60"
              v-model="rest_hr"
            />
          </form>

          <div class="mt-10">
            <div class="bg-neutral-back/60 p-10 rounded-t-md">
              <AuthTitle
                title="Zonas de frecuencia cardíaca (Z1-Z5)"
                title-class="text-3xl font-headline font-bold capitalize text-primary-too-dark"
                subtitle="Estratificación algorítmica de la intensidad basada en la frecuencia cardíaca de reserva."
                subtitle-class="text-sm text-neutral font-body tracking-tight"
              />
            </div>
            <form @submit.prevent="handleUpdate">
              <table class="w-full">
                <thead>
                  <tr
                    class="grid grid-cols-4 bg-neutral-light/60 px-10 py-7 uppercase text-sm items-center text-black/60 font-label"
                  >
                    <th class="text-left">Zona</th>
                    <th>
                      rango de<br />
                      intensidad
                    </th>
                    <th>Cálculo <br />ppm</th>
                    <th class="text-right">Cambio <br />manual</th>
                  </tr>
                </thead>
                <tbody v-if="zones">
                  <DataTable :zones="zones" @update:zones="(val) => (zones = val)" />
                </tbody>
                <tfoot>
                  <tr class="grid grid-cols-4">
                    <td>
                      <input type="numeric" class="hidden" name="max_hr" :value="max_hr" />
                      <input type="numeric" class="hidden" name="rest_hr" :value="rest_hr" />
                    </td>
                    <Button
                      class="col-start-4 mt-5"
                      content="Guardar cambios"
                      :colors="errorMessage ? '' : 'bg-primary text-white'"
                      hover="hover:bg-primary/90"
                      classes="text-sm tracking-widest py-3"
                      :loading="userStore.loading"
                    />
                    <p v-if="errorMessage">{{ errorMessage }}</p>
                  </tr>
                </tfoot>
              </table>
            </form>
          </div>
        </div>
      </div>
      <div class="md:col-span-3 lg:col-span-1">
        <div class="bg-neutral-back/60 p-5">
          <div class="flex items-center gap-3">
            <Blockquote class="stroke-secondary-light" />
            <h4 class="text-2xl font-headline font-bold">
              Resumen <br />
              clínico
            </h4>
          </div>

          <div class="bg-neutral/30 font-label rounded-sm mt-4 p-3 text-xs text-neutral">
            <h5 class="font-bold text-md capitalize my-1 text-primary-too-dark">
              La fórmula de Karvonen
            </h5>
            <p class="my-2">
              Frecuencia cardíaca objetivo = <br />
              ((Max HR - RHR ) * % Intensity) + RHR
            </p>
            <p class="my-2">
              Este método tiene en cuenta la Frecuencia Cardíaca de Reserva (FCR) del atleta,
              proporcionando un perfil fisiológico más individualizado que los cálculos estándar
              basados únicamente en la edad.
            </p>
          </div>
          <h5 class="mt-3 text-sm font-bold uppercase tracking-wide text-primary-too-dark">
            Recuperación (Z1)
          </h5>
          <p class="text-sm font-body text-primary-too-dark/70">
            Baja intensidad. Promueve el flujo sanguíneo a los músculos sin introducir un estrés
            sistémico significativo. Ideal para días posteriores a la competición.
          </p>
          <h5 class="mt-3 text-sm font-bold uppercase tracking-wide text-primary-too-dark">
            Aeróbico (Z2)
          </h5>
          <p class="text-sm font-body text-primary-too-dark/70">
            La base de la resistencia. Optimiza la oxidación de grasas y la densidad mitocondrial.
            Debería representar el 70-80% del volumen total de entrenamiento.
          </p>
          <h5 class="mt-3 text-sm font-bold uppercase tracking-wide text-primary-too-dark">
            Umbral de Lactato (Z4)
          </h5>
          <p class="text-sm font-body text-primary-too-dark/70">
            El punto en el que el lactato comienza a acumularse más rápido de lo que puede ser
            eliminado. El entrenamiento en esta zona desplaza el punto de ruptura metabólica.
          </p>

          <div class="border-t mt-7 border-neutral-light/60 flex pt-7 gap-3 items-center">
            <Science class="stroke-primary-too-dark fill-primary-too-dark" />
            <h5 class="font-body font-bold text-sm">Protocolo revisado por pares</h5>
          </div>
          <p class="mt-2 text-xs text-neutral/60 font-body">
            Referencia: Guías del ACSM para Pruebas de Esfuerzo y Prescripción Médica, 11ª Edición.
          </p>
        </div>
        <div
          class="bg-primary-too-dark/90 flex flex-col justify-between mt-6 rounded-md p-5 text-white"
        >
          <p
            class="p-2 bg-[#304C36] w-fit font-label uppercase tracking-wider text-xs text-primary-light border-primary-light rounded-xs border-[0.5px]"
          >
            Active Profile
          </p>
          <div class="mt-10 flex flex-col">
            <p class="text-3xl font-headline font-bold">{{ user?.name + ' ' + user?.surname }}</p>
            <p class="-mt-2 text-primary-light font-label text-xs">{{ user?.nickname }}</p>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
