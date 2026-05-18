<script setup>
import AuthTitle from '@/components/AuthTitle.vue'
import DashboardInfo from '@/components/DashboardInfo.vue'
import Button from '@/components/Button.vue'
import Square from '@/components/Square.vue'
import PredictionCard from './PredictionCard.vue'

import { computed, onMounted, ref } from 'vue'
import { usePredictionStore } from '@/stores/prediction'
import ScattlerPlotPred from './ScattlerPlotPred.vue'

const simulationForm = ref({
  loadFactor: 0, // Por defecto sin alteración (0%)
  activityDepth: 30, // Bloque óptimo por defecto (30 carreras)
  temperature: 15, // 15ºC es la temperatura estándar ideal de carrera
})
const prediction = ref({ activityDepth: 30 })

const handleSimulate = async () => {
  console.log('Enviando parámetros al backend/modelo:', simulationForm.value)
  await predictionStore.simulate({
    loadFactor: simulationForm.value.loadFactor, 
    activityDepth: simulationForm.value.activityDepth,
    temperature: simulationForm.value.temperature, 
  })
}

const handlePrediction = async () => {
  await predictionStore.predict({ activityDepth: prediction.value.activityDepth })
  console.log(predictionSnapshots.value)
}

const predictionStore = usePredictionStore()
const predictionSnapshots = computed(() => predictionStore.predictionSnapshots)
const model = computed(() => predictionStore.model)
const modelMetrics = computed(() => predictionStore.model.model_metrics)

const improvement = computed(() => {
  const metrics = modelMetrics.value

  // Validación: Si el array está vacío o no existe, devolvemos 0
  if (!metrics || metrics.length === 0) return 0

  const sumaTotal = metrics.reduce(
    (acumulador, m) => acumulador + (m.riegel_mae_seconds - m.mae_seconds) / m.riegel_mae_seconds,
    0,
  )

  // Dividimos la suma entre el total de elementos
  return sumaTotal / metrics.length
})

onMounted(async () => {
  await predictionStore.checkPrediction()
})

const getPreviousTime = (dist) => {
  if (!predictionSnapshots.value?.pred) return null
  const key = Math.floor(dist) + 'k'
  return predictionSnapshots.value.pred[key]
}

const mergedPredictions = computed(() => {
  if (!predictionSnapshots.value?.pred || !model.value?.ml_points) return []

  const points = Object.entries(predictionSnapshots.value.pred).map(([key, timeValue]) => {
    const numericDistance = parseInt(key)

    const modelPoint = model.value.ml_points.find(
      (point) => Math.floor(point.distance) === numericDistance,
    )

    return {
      distance: modelPoint ? modelPoint.distance : numericDistance,
      time: timeValue,
      confidence_range: modelPoint
        ? modelPoint.confidence_range
        : [timevalue * 0.05, timeValue * 1.05],
    }
  })
  return points.sort((a, b) => a.distance - b.distance)
})
</script>
<template>
  <AuthTitle
    title="Predictor simulator"
    subtitle="Execute high-fidelty simulaions using the clinical Linear Regression engine. Adjust parameters in the sidebar to observer real-time variance in estimated performance outcomes."
  />
  <div class="grid grid-cols-1 lg:grid-cols-4 mt-4">
    <div class="grid-cols-1 lg:col-span-3 p-2">
      <div class="grid lg:grid-cols-3 gap-4">
        <DashboardInfo
          title="R-squared (Avg)"
          :value="model.r2_avg.toFixed(3)"
          :diff="model.model_metrics[0].r2.toFixed(2)"
          comp="Global fit"
          bg="bg-neutral-back/60"
        />
        <DashboardInfo
          title="Mean Absolute Error"
          :value="(model.mae_avg / 60).toFixed(1) + ' min'"
          :diff="
            improvement > 0
              ? '-' + Math.abs(parseInt(improvement * 100))
              : Math.abs(parseInt(improvement * 100))
          "
          comp="MAE Deviation"
          bg="bg-neutral-back/60"
        />
        <DashboardInfo
          title="Model Training"
          :value="model.train_samples"
          :diff="model.runs_used.toString()"
          comp="Activities Used"
          bg="bg-neutral-back/60"
        />
      </div>
      <div class="my-4">
        <ScattlerPlotPred
          :user_bests="model.user_bests"
          :ml_points="model.ml_points"
          :pred="predictionSnapshots.pred"
          v-if="model"
        />
      </div>
      <div
        v-if="model && predictionSnapshots"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-6"
      >
        <PredictionCard
          v-for="(item, index) in mergedPredictions"
          :key="index"
          :distance="item.distance"
          :time="item.time"
          :range="item.confidence_range"
          :version="model.model_version"
          :previous-time="getPreviousTime(item.distance)"
        />
      </div>
      <Square
        svg="Light"
        title="Architect's Insight"
        :text="
          'El modelo presenta una alta sensibilidad a <b>' +
          model.runs_used +
          ' actividades</b> de historial. <br> Para estabilizar la varianza (MAE: ' +
          (model.mae_avg / 60).toFixed(1) +
          ' min), se recomienda incrementar la profundidad del dataset en un 15% antes del próximo re-entrenamiento.'
        "
        :html="true"
        titleClass="font-label text-lg font-bold -mt-1"
      />
    </div>
    <div class="col-span-1 bg-neutral-back/60 p-8 m-2 mr-0 rounded-md border border-white/5">
      <h4 class="font-headline font-semibold text-2xl text-primary/80">Simulation Controls</h4>
      <p class="text-[11px] text-neutral-500 mt-1">
        Ajusta los parámetros para estresar el modelo predictivo.
      </p>

      <form @submit.prevent="handleSimulate" class="mt-4">
        <div class="mb-5">
          <label
            for="load-range"
            class="block mb-2 text-xs font-label uppercase font-semibold text-neutral/70"
          >
            Simulated Training Load (Fatigue Factor)
          </label>
          <input
            id="load-range"
            type="range"
            min="-20"
            max="20"
            step="5"
            v-model.number="simulationForm.loadFactor"
            class="w-full bg-neutral-light h-1.5 accent-secondary-light rounded-full appearance-none cursor-pointer"
          />
          <div
            class="flex justify-between uppercase font-label text-[9px] font-semibold text-neutral-500 mt-2"
          >
            <p class="text-primary-semi-light">Overtraining: -20%</p>
            <p class="text-secondary-light font-bold">{{ simulationForm.loadFactor }}%</p>
            <p class="text-amber-500">Peak Volume: +20%</p>
          </div>
        </div>

        <div class="mt-5">
          <label
            for="history-depth"
            class="text-xs font-label text-neutral/70 font-semibold uppercase block mb-2"
          >
            Dataset Depth (Recent Runs Used)
          </label>
          <select
            id="history-depth"
            v-model.number="simulationForm.activityDepth"
            class="bg-neutral-light/60 border border-white/10 w-full pl-3 pr-5 py-2 font-label text-xs outline-none text-primary"
          >
            <option :value="15">Last 15 activities (Short-term form)</option>
            <option :value="30">Last 30 activities (Optimal block)</option>
            <option :value="60">Last 60 activities (Macrocycle overview)</option>
          </select>
        </div>

        <div class="mt-5">
          <label
            for="weather-factor"
            class="font-label text-xs uppercase text-neutral/70 font-semibold block mb-2"
          >
            Race Day Temperature Impact
          </label>
          <div
            class="bg-neutral-light/60 border border-white/10 w-full pl-3 pr-5 py-2 font-label text-xs outline-none text-primary flex items-center"
          >
            <input
              id="weather-factor"
              type="number"
              v-model.number="simulationForm.temperature"
              class="bg-transparent w-full text-priamry font-mono outline-none text-sm"
              min="5"
              max="35"
              step="1"
            />
            <p class="font-label text-neutral-500 uppercase font-semibold text-[10px] ml-2">ºC</p>
          </div>
        </div>

        <Button
          change="Recalculating marks..."
          content="Run Simulation"
          colors="bg-secondary-light text-white w-full justify-center"
          hover="hover:bg-secondary-light/70"
          class="mt-6 w-full py-2.5 rounded-md font-semibold text-sm transition-all"
          :loading="predictionStore.loading"
        />
      </form>
      <div class="w-full h-0.5 bg-neutral/20 rounded-md my-8"></div>
      <h4 class="font-headline font-semibold text-2xl text-primary/80">Simulation Controls</h4>
      <p class="text-[11px] text-neutral-500 mt-1">
        Ajusta los parámetros para estresar el modelo predictivo.
      </p>
      <form @submit.prevent="handlePrediction">
        <div class="mt-5">
          <label
            for="prediction-history-depth"
            class="text-xs font-label text-neutral-400 font-semibold uppercase block mb-2"
          >
            Dataset Depth (Recent Runs Used)
          </label>
          <select
            id="prediction-history-depth"
            v-model.number="prediction.activityDepth"
            class="bg-neutral-light/60 border border-white/10 w-full pl-3 pr-5 py-2 font-label text-xs outline-none text-primary"
          >
            <option :value="15">Last 15 activities (Short-term form)</option>
            <option :value="30">Last 30 activities (Optimal block)</option>
            <option :value="60">Last 60 activities (Macrocycle overview)</option>
          </select>
          <Button
            change="Running prediction..."
            content="Run Prediction"
            colors="bg-secondary-light text-white w-full justify-center"
            hover="hover:bg-secondary-light/70"
            class="mt-6 w-full py-2.5 rounded-md font-semibold text-sm transition-all"
            :loading="predictionStore.loading"
          />
        </div>
      </form>
    </div>
  </div>
</template>
