<script setup>
import Predictor from '@/assets/Predict.png'
import Bolt from '@/assets/svg/Bolt.vue'
import { usePredictionStore } from '@/stores/prediction.js'
import { ErrorCodes } from 'vue'

const predictionStore = usePredictionStore()

const handlePredict = async () => {
  try {
    await predictionStore.predict()
  } catch (error) {
    throw error
    console.log(error)
  }
}
</script>
<template>
  <div class="flex flex-col h-screen items-center justify-center max-w-3xl m-auto">
    <img :src="Predictor" alt="" class="rounded-lg max-w-200" />
    <h2 class="text-3xl font-bold font-headline my-5">Motor predictivo en espera</h2>
    <p class="font-body text-center">
      El entorno de simulación requiere la inicialización de conjuntos de datos históricos para
      calibrar sus algoritmos predictivos. Nuestro proceso de modelado emplea regresión
      multivariable e inferencia bayesiana para generar estimaciones de rendimiento precisas.
    </p>
    <p class="font-body text-neutral text-xs text-center my-5">
      Por favor, inicialice el sistema cargando un conjunto de datos CSV validado y definiendo sus
      zonas de entrenamiento clínico.
    </p>
    <Button
      @click="handlePredict"
      class="flex bg-primary-too-dark p-4 rounded-lg text-white font-label capitalize tracking-wide gap-2 hover:bg-primary-dark mt-5"
    >
      <Bolt />
      <p>Iniciar primera simulación</p>
    </Button>
  </div>
</template>
