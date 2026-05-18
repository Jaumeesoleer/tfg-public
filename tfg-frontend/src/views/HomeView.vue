<script setup>
import Tips from '@/components/Tips.vue'
import Login from '@/components/Login.vue'
import Regression from '@/views/Regression.vue'
import Square from '@/components/Square.vue'
import Button from '@/components/Button.vue'

import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
const userStore = useUserStore()
const router = useRouter()

const handleDemoLogin = async () => {
  try {
    const response = await userStore.demoLogin()
    if (response) {
      router.push('/dashboard')
    }
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <main class="pt-24 min-h-screen bg-neutral-back">
    <section
      class="max-w-7xl mx-auto px-8 py-12 gap-12 grid grid-cols-1 lg:grid-cols-12 items-center"
    >
      <div class="lg:col-span-7 space-y-8">
        <div class="space-y-4">
          <h4 class="text-xs text-secondary-light font-label font-bold uppercase tracking-widest">
            Inteligencia deportiva clínica
          </h4>
          <h1
            class="text-6xl md:text-8xl text-primary-too-dark leading-[0.9] font-headline mt-5 tracking-tighter"
          >
            Arquitectando <br />
            el rendimiento.
          </h1>
        </div>
        <p class="text-xl text-on-surface-variant max-w-xl leading-relaxed font-body text-neutral">
          Un enfoque revisado por pares para la optimización del atleta. Utilizamos arquitecturas
          rigurosas de Scikit-learn para traducir datos fisiológicos brutos en métricas predictivas
          de carácter clínico.
        </p>
        <div class="grid grid-cols-3 gap-8 pt-8">
          <Tips value="91.2%" name="Model accuracy" />
          <Tips value="12.2k" name="Data points/sec" />
          <Tips value="0.15ms" name="Inference latency" />
        </div>
      </div>
      <div
        class="lg:col-span-5 p-10 rounded-xl whisper-border relative overflow-hidden shadow-[0_12px_32px_-4px_rgba(23,28,31,0.06)] bg-white"
      >
        <Login />
      </div>
    </section>
    <section class="bg-neutral-back2 mx-auto px-8 py-24">
      <div class="max-w-7xl mx-auto">
        <div class="mb-16">
          <h4
            class="text-xs text-secondary-light font-label tracking-widest font-bold uppercase max-w-2xl"
          >
            La metodología
          </h4>
          <h2 class="text-5xl font-headline mt-4 text-primary-too-dark">
            Rigor predictivo mediante la validación <br />cruzada de algoritmos.
          </h2>
          <p class="leading-relaxed font-body text-neutral mt-6 text-pretty">
            Nuestro motor analiza 97 actividades con datos de pulso personalizados (FC Máx: 203,
            Reserva: 143 bpm) distribuidos en 5 zonas de intensidad. Para la predicción de tiempos
            de carrera (5k a 42k), confrontamos el modelo matemático tradicional de Riegel frente a
            Machine Learning (Random Forest). En tu perfil actual de nivel iniciación, el modelo de
            Riegel ofrece la mayor precisión clínica con un margen de error mínimo (MAE de solo 1.1
            min en 5k). El sistema optimiza tus proyecciones aislando variables críticas: la
            variabilidad de la pendiente (stream_grade) y la velocidad media (speed_ms) son los
            factores con mayor peso predictivo en tu rendimiento
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 h-auto md:h-150">
          <Regression />
          <div class="md:col-span-4 flex flex-col gap-6">
            <Square
              svg="Neural"
              title="Modelado No Lineal"
              text="Algoritmos basados en datos secuenciales que aíslan patrones en el comportamiento del corredor."
            />
            <Square
              svg="History"
              title="Inteligencia de Datos Históricos"
              text="Referenciación cruzada del perfil biométrico actual (FC Reserva: 143 bpm) con un histórico personalizado de 97 actividades y flujos continuos de datos."
              bgColor="bg-[#dfe3e6]"
              title-color="text-black"
              text-color="text-neutral"
            />
          </div>
        </div>
      </div>
    </section>
  </main>

  <section class="px-8 py-24 bg-neutral-back">
    <div class="max-w-7-xl mx-auto flex flex-col items-center text-center">
      <div class="h-24 w-px bg-linear-to-b from-transparent to-[#c7c5d3] mb-12"></div>
      <h2 class="font-headline text-primary-too-dark max-w-3xl leading-tight text-6xl">
        ¿Listo para validar <br />
        el modelo?
      </h2>
      <p class="text-neutral max-w-xl mt-8 font-body">
        Un entorno diseñado para investigadores y entrenadores de alto rendimiento que buscan
        precisión científica en la toma de decisiones.
      </p>
      <div class="mt-12 flex gap-4">
        <Button
          content="Probar demostración"
          change=""
          hover="hover:-translate-y-1 hover:shadow-2xl"
          bold="font-bold"
          w=""
          class="transition-all px-10"
          @click="handleDemoLogin"
        />
        <Button
          content="Documentación técnica"
          change=""
          bold="font-bold"
          w=""
          colors=""
          border="border-1 border-[#c7c5d3]"
          hover="hover:bg-[#c7c5d340]"
          class="px-10"
        />
      </div>
    </div>
  </section>
</template>
