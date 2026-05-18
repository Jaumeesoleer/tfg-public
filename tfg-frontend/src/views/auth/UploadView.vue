<script setup>
import { ref } from 'vue'
import { activityService } from '@/services/activity'
import Sidebar from '@/components/Sidebar.vue'
import AuthTitle from '@/components/AuthTitle.vue'
import Button from '@/components/Button.vue'
import UploadFormat from '@/components/UploadFormat.vue'
import Square from '@/components/Square.vue'
import Upload from '@/assets/svg/Upload.vue'
import Info from '@/assets/svg/Info.vue'
import Strava from '@/assets/svg/Strava.vue'

const selectedFiles = ref([])
const uploadStatus = ref('')
const isUploading = ref(false)
const serverErrors = ref([])
const fileInput = ref(null)

const handleFileChange = (event) => {
  selectedFiles.value = Array.from(event.target.files)
}

const uploadActivities = async () => {
  if (selectedFiles.value.length === 0) return

  const formData = new FormData()

  selectedFiles.value.forEach((file) => {
    formData.append('activities', file)
  })

  isUploading.value = true
  uploadStatus.value = 'Procesando archivos...'

  try {
    const response = await activityService.uploadCSV(formData)
    uploadStatus.value = response.data.message

    if (response.data.errors && response.data.errors.length > 0) {
      serverErrors.value = response.data.errors
    } else {
      serverErrors.value = []
      selectedFiles.value = []
    }
  } catch (error) {
    uploadStatus.value = 'Error crítico en la subida'
    serverErrors.value = error.response?.data?.errors || [error.response?.data?.error]
  } finally {
    isUploading.value = false
  }
}

const triggerFileInput = () => {
  fileInput.value.click()
}
</script>

<template>
  <main class="bg-neutral-back-auth flex-1 pt-5">
    <Sidebar class="hidden md:block" />
    <div class="md:ml-64 md:px-16 p-4 md:py-8">
      <AuthTitle
        title="Ingesta de datos de investigación"
        subtitle="Cargue su telemetría bruta o conjuntos de datos científicos. Asegúrese de que sus archivos cumplan con las especificaciones clínicas detalladas a continuación para una integración fluida con el motor analítico."
      />

      <div class="grid grid-cols-1 lg:grid-cols-6 gap-5">
        <div class="lg:col-span-2">
          <div class="mt-5">
            <div class="flex items-center justify-center w-full">
              <div
                class="flex flex-col items-center justify-center w-full h-64 bg-neutral-secondary-medium border border-dashed border-default-strong rounded-xl bg-neutral-back border-neutral/60"
              >
                <div class="flex flex-col items-center justify-center text-body pt-5 pb-6">
                  <Upload class="bg-neutral-back-auth rounded-md w-15 h-15 p-3" />
                  <p class="mb-2 text-sm">Drag & Drop</p>
                  <p class="text-xs mb-4">Soporte para varios .CSV.</p>
                  <Button
                    v-if="selectedFiles.length === 0"
                    content="Browse files"
                    change="Uploading..."
                    w=""
                    class="p-2"
                    :click="triggerFileInput"
                    :disabled="isUploading"
                    classes="text-xs capitalize"
                    bold=""
                  />
                  <Button
                    v-else
                    :content="`Upload ${selectedFiles.length} files`"
                    change="Uploading..."
                    w=""
                    class="p-2"
                    :click="uploadActivities"
                    :disabled="isUploading"
                    classes="text-xs capitalize"
                    bold=""
                  />
                </div>
              </div>

              <input
                type="file"
                multiple
                ref="fileInput"
                accept=".csv"
                @change="handleFileChange"
                class="hidden"
              />
              <p v-if="uploadStatus">{{ uploadStatus }}</p>
              <div v-if="serverErrors.length > 0" class="error-list">
                <h3>Algunos archivos no se pudieron procesar:</h3>
                <ul>
                  <li v-for="(err, index) in serverErrors" :key="index">
                    {{ err }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="bg-neutral-back/60 border rounded-xl border-neutral/30 p-4 mt-5 shadow-inner">
            <div class="flex items-align justify-between font-label font-semibold uppercase">
              <h4 class="tracking-wider text-primary-too-dark text-xs">Flujo directo</h4>
              <p class="text-[10px] bg-neutral/20 rounded-xl p-1 tracking-wide">Desactivado</p>
            </div>
            <div class="flex gap-2 items-center">
              <Strava class="stroke-orange-400 bg-orange-200 rounded p-1 w-8 h-8" />
              <div class="font-label tracking-wide">
                <h4 class="text-xs font-bold text-primary-too-dark">Conectar con Strava</h4>
                <p class="text-[10px] text-neutral-light">
                  Sincronización automática de actividades
                </p>
              </div>
            </div>
            <Button
              class="mt-4"
              :disabled="true"
              content="Servicio no disponible"
              :isLock="true"
              colors="text-neutral-light"
              hover="hover:bg-neutral-back-auth"
              classes="capitalize py-2 text-md"
              cursor="cursor-not-allowed"
            />
          </div>
          <Square
            class="mt-5 border-l-4 border-primary-light"
            title="Integridad de la carga"
            text="Motor de validación activo. Todos los datos se procesan localmente antes de ser transmitidos al clúster de cómputo principal."
            bgColor="bg-neutral-back"
            titleColor="text-primary-too-dark font-bold"
            padding="p-5"
            textColor="text-neutral/60"
          />
        </div>
        <div class="lg:col-span-4 py-4 px-4">
          <div class="p-4">
            <h4 class="capitalize font-headline font-bold text-2xl">Especificaciones de datos</h4>
            <p class="font-label tracking-wider text-neutral uppercase text-[10px]">
              Documentación del esquema aceptado
            </p>
          </div>
          <div class="bg-neutral-back p-4 rounded-t-lg">
            <div class="">
              <p class="font-body text-sm">
                Nuestro flujo de ingesta requiere archivos de valores separados por comas (CSV) con
                codificación UTF-8. El sistema espera una fila de encabezado que contenga los
                nombres exactos de los campos definidos en los protocolos siguientes. Los campos
                opcionales ausentes se tratarán como nulos, mientras que los campos obligatorios de
                telemetría deben contener valores numéricos válidos o con formato ISO-8601.
              </p>
            </div>
            <UploadFormat
              title="Formato A: Protocolo de Telemetría"
              text="Datos detallados de series temporales para el seguimiento del rendimiento de alta frecuencia."
              atr="altitude (Opcional), velocity_smooth (Opcional), time, heartrate, grade_smooth (Opcional), distance, lat (Opcional), lng (Opcional), activity_id"
              color="primary"
            />
            <UploadFormat
              title="Formato B: Resumen de Actividad"
              text="Estadísticas agregadas para el análisis comparativo a nivel de sesión."
              atr="id, type, name (Opcional), distance, moving_time, elapsed_time, total_elevation_gain, start_date (Opcional), start_latlng (Opcional), kilojoules, average_heartrate, max_heartrate (Opcional), elev_high (Opcional), elev_low (Opcional), average_speed, max_speed (Opcional)"
              color="secondary"
            />
          </div>
          <div class="p-4 bg-neutral-light/10 flex justify-between items-center rounded-b-xl">
            <div class="flex items-center gap-2">
              <Info class="w-4 fill-neutral-light" />
              <p class="text-[10px] font-body text-neutral-light">
                Verifique los encabezados con precisión para evitar errores de validación.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
