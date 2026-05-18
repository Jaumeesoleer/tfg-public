<script setup>
import { RouterView } from 'vue-router'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <body class="selection:bg-primary-light selection:text-primary-too-dark antialiased m-0">
    <Header v-if="!$route.meta.HideNavBar" />
    <div class="flex flex-col min-h-screen w-full">
      <RouterView />
      <Footer v-if="!$route.meta.HideNavBar" />
    </div>
  </body>
</template>
