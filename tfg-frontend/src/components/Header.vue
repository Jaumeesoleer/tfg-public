<script setup>
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>

<template>
  <header
    class="shadow-sm backdrop-blur-md/80 items-center top-0 bg-neutral-back fixed w-full z-9999"
  >
    <div class="mx-auto w-auto max-w-7xl">
      <nav class="flex justify-between items-center w-full md:px-8 p-4 max-w-full mx-auto">
        <RouterLink
          class="font-semibold text-2xl font-headline text-primary-too-dark cursor-pointer"
          exact-active-class=""
          :to="userStore.isAuthenticated ? '/dashboard' : '/'"
        >
          The Architect: Arquitectura del Rendimiento
        </RouterLink>

        <RouterLink
          class="p-2 sm:py-4 text-white bg-secondary-light hover:bg-secondary-light/80 font-label text-[10px] sm:text-xs tracking-widest uppercase rounded-sm transition-all active:scale-[0.98] cursor-pointer font-semibold"
          to="/signup"
        >
          Alta de Analista
        </RouterLink>
      </nav>
    </div>
  </header>
</template>
