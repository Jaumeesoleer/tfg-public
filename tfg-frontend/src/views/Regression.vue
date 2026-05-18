<script setup>
import TrendingUp from '@/assets/svg/TrendingUp.vue'
import Science from '@/assets/svg/Science.vue'
</script>

<template>
  <div
    class="md:col-span-8 bg-white p-8 rounded-xl whisper-border flex flex-col justify-between group overflow-hidden relative"
  >
    <div class="z-10">
      <Science class="stroke-secondary-light px-0" />
      <h3 class="font-serif text-3xl text-primary-too-dark mb-4">
        Random Forest & <br />
        Importancia de Variables
      </h3>
      <p class="text-sm text-on-surface-variant max-w-md">
        Cuantificación del impacto de 15 métricas de entrenamiento mediante el cálculo de pureza de
        nodos (Gini Importance) en árboles de decisión. Nuestro algoritmo evalúa la variabilidad
        fisiológica y ambiental de tus 97 actividades para aislar los factores críticos que dictan
        tu rendimiento real.
      </p>
    </div>
    <div class="mt-8 z-10">
      <div class="flex items-end gap-2 h-32">
        <div
          class="bg-primary/10 w-12 h-[30%] rounded-t-sm group-hover:bg-primary transition-all duration-700"
        ></div>
        <div
          class="bg-primary/10 w-12 h-[45%] rounded-t-sm group-hover:bg-primary transition-all duration-700 delay-75"
        ></div>
        <div
          class="bg-primary/10 w-12 h-[38%] rounded-t-sm group-hover:bg-primary transition-all duration-700 delay-150"
        ></div>
        <div
          class="bg-primary/10 w-12 h-[65%] rounded-t-sm group-hover:bg-primary transition-all duration-700 delay-200"
        ></div>
        <div
          class="bg-primary/10 w-12 h-[85%] rounded-t-sm group-hover:bg-primary transition-all duration-700 delay-300"
        ></div>
        <div
          class="bg-primary/10 w-12 h-[70%] rounded-t-sm group-hover:bg-primary transition-all duration-700 delay-500"
        ></div>
      </div>
      <div
        class="border-t border-outline-variant pt-4 flex justify-between font-label text-[10px] text-outline uppercase tracking-tighter"
      >
        <span>Input: Estabilidad de la Pendiente (stream_grade_std_mean)</span>
        <span>Coefficient: 0.0545</span>
        <span>RANK: #1 de 15 variables críticas</span>
      </div>
    </div>
    <div
      class="absolute right-0 bottom-0 opacity-5 pointer-events-none transform translate-x-1/4 translate-y-1/4"
    >
      <span class="material-symbols-outlined">
        <TrendingUp width="300" height="300" />
      </span>
    </div>
  </div>
</template>
