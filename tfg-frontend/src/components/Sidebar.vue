<script setup>
import Science from '@/assets/svg/Science.vue'
import Mapping from '@/assets/svg/Mapping.vue'
import Overview from '@/assets/svg/Overview.vue'
import History from '@/assets/svg/History.vue'
import defaultPhoto from '@/assets/Profile.webp'
import { useUserStore } from '@/stores/user'
import { computed, onMounted } from 'vue'
import Neural from '@/assets/svg/Neural.vue'
import Dropdown from './Dropdown.vue'

const userStore = useUserStore()
const user = computed(() => userStore.user)
const API_URL = import.meta.env.VITE_API_URL

const displayPhoto = computed(() => {
  if (user.value.profile_photo && user.value.profile_photo !== '') {
    return `${API_URL}/${user.value.profile_photo}`
  }

  return defaultPhoto
})

onMounted(async () => {
  userStore.fetchProfile()
})
</script>
<template>
  <aside class="p-3 bg-neutral-back2 fixed h-full">
    <div class="flex gap-3 text-primary-dark items-baseline">
      <div class="w-3 h-3 bg-primary-dark rounded-full"></div>
      <h2 class="font-headline text-2xl">The Architect</h2>
    </div>
    <p class="text-neutral/70 font-sem text-sm tracking-wide font-body mt-1">Scikit-learn v1.5.2</p>

    <div class="flex flex-col justify-between h-8/10">
      <div
        class="mt-10 flex flex-col font-body tracking-wide text-sm font-semibold stroke-neutral text-neutral"
      >
        <RouterLink
          to="/dashboard"
          class="p-2 hover:bg-neutral/10 pr-30 flex gap-2 items-center"
          exact-active-class="bg-white pr-30 text-secondary-light"
        >
          <Overview />
          <p>Panel de Control</p>
        </RouterLink>
        <RouterLink
          to="/dashboard/data"
          class="p-2 hover:bg-neutral/10 flex gap-2 items-center"
          exact-active-class="bg-white pr-30 text-secondary-light"
        >
          <Mapping />
          <p>Mapeo de Datos</p>
        </RouterLink>
        <RouterLink
          to="/dashboard/predictor"
          class="p-2 hover:bg-neutral/10 flex gap-2 items-center"
          exact-active-class="bg-white  text-secondary-light"
        >
          <Science />
          <p>Perspectivas del Modelo</p>
        </RouterLink>
        <RouterLink
          to="/dashboard/activities"
          class="p-2 hover:bg-neutral/10 pr-30 flex gap-2 items-center"
          exact-active-class="bg-white pr-30 text-secondary-light"
        >
          <History />
          <p>Archivo Histórico</p>
        </RouterLink>
        <RouterLink
          to="/dashboard/upload"
          class="p-2 hover:bg-neutral/10 pr-30 flex gap-2 items-center"
          exact-active-class="bg-white pr-30 text-secondary-light"
        >
          <Neural class="stroke-current" />
          <p>Cargar Datos</p>
        </RouterLink>
      </div>
      <div class="flex justify-between gap-2 items-center" v-if="user">
        <RouterLink
          to="/dashboard/profile"
          class="hover:text-secondary-light text-secondary-dark cursor-pointer flex items-center gap-2"
          exact-active-class=""
        >
          <img :src="displayPhoto" alt="Profile photo" class="h-10 w-10 rounded-md" />
          <div class="text-label">
            <p class="font-bold text-xs">{{ user.name + ' ' + user.surname }}</p>
            <p class="text-[10px] text-neutral">{{ user.nickname }}</p>
          </div>
        </RouterLink>
        <Dropdown />
      </div>
    </div>
  </aside>
</template>
