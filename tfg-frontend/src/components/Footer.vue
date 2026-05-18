<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <footer
    class="border-t border-[#c7c5d31a] bg-neutral-back"
    :class="[$route.meta.HideNavBar ? 'pb-12' : 'py-12']"
  >
    <div
      class="flex flex-col max-w-7xl px-8 mx-auto md:flex-row gap-8 items-center justify-between"
    >
      <h3
        class="text-2xl font-headline text-black italic justify-self-center md:justify-self-start"
      >
        The Analitycal Architect
      </h3>
      <nav
        class="flex gap-8 font-label justify-center text-[10px] tracking-widest text-outline text-neutral-light"
      >
        <RouterLink to="/privacy" class="uppercase hover:text-secondary-light"
          >Privacy protocol</RouterLink
        >
        <RouterLink to="/license" class="uppercase hover:text-secondary-light"
          >Analytical license</RouterLink
        >
        <RouterLink to="/support" class="uppercase hover:text-secondary-light"
          >Support terminal</RouterLink
        >
      </nav>
      <p class="md:justify-self-end justify-self-center uppercase text-[10px] text-neutral-light">
        Jaume Soler Dev
      </p>
    </div>
  </footer>
</template>
