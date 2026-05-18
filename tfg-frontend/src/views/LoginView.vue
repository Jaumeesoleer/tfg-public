<script setup>
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import Arc from '@/assets/svg/Arc.vue'
import { RouterLink } from 'vue-router'

const selected = 'font-bold border-b'
</script>
<template>
  <main class="bg-neutral-back flex-1 flex">
    <div class="grid grid-cols-1 lg:grid-cols-12 p-8 mx-auto max-w-7xl w-full">
      <div
        class="hidden lg:flex lg:flex-col lg:col-span-5 bg-primary-ultra rounded-l-2xl px-10 py-15 justify-between"
      >
        <div class="">
          <div class="flex gap-5">
            <Arc class="w-8 h-8 stroke-primary-light/60" />
            <h2 class="capitalize font-headline text-3xl text-white font-semibold">
              The Architect: Arquitectura del Rendimiento
            </h2>
          </div>
          <h1 class="text-6xl text-white font-headline mt-10">
            El manuscrito <br />
            clínico.
          </h1>
          <p class="mt-10 font-body text-xl text-primary-light/60">
            Acceda al ecosistema seguro de análisis deportivo avanzado. Nuestra metodología cierra
            la brecha entre los datos brutos y los hallazgos científicos.
          </p>
        </div>
        <div class="bg-primary-semi-light p-4 border-l-2 border-primary-light">
          <h4 class="font-label uppercase tracking-wide text-primary-light/60">
            Estado actual del sistema
          </h4>
          <div class="flex items-center gap-2">
            <div class="rounded-full w-3 h-3 bg-primary-light/60 animate-pulse"></div>
            <p class="text-white">Núcleo de la arquitectura: Operativo</p>
          </div>
        </div>
      </div>
      <div class="lg:col-span-7 bg-white lg:px-10 lg:py-15 rounded-2xl h-full lg:rounded-r-2xl">
        <div class="border-b border-neutral-light flex gap-4 mb-10">
          <RouterLink to="/login" :class="{ [selected]: $route.meta.Login }" class=""
            >Login</RouterLink
          >
          <RouterLink to="/signup" :class="{ [selected]: !$route.meta.Login }">Register</RouterLink>
        </div>
        <Register v-if="$route.name === 'signup'" />
        <Login v-if="$route.name === 'login'" />
      </div>
    </div>
  </main>
</template>
