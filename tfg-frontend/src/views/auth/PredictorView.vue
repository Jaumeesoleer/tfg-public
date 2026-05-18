<script setup>
import Sidebar from '@/components/Sidebar.vue'
import Predictor from '@/components/Predictor.vue'
import PredictorDefault from '@/components/PredictorDefault.vue'

import { computed, onMounted } from 'vue'
import { usePredictionStore } from '@/stores/prediction'

const predictionStore = usePredictionStore()
const prediction = computed(() => predictionStore.prediction)

onMounted(async () => {
  await predictionStore.checkPrediction()
})
</script>

<template>
  <main class="flex-1 bg-neutral-back-auth pt-5">
    <Sidebar class="hidden md:block" />
    <div class="md:ml-64 md:pl-13 lg:px-16 p-4 md:py-8">
      <PredictorDefault v-if="!prediction" />
      <Predictor v-if="prediction" />
    </div>
  </main>
</template>
