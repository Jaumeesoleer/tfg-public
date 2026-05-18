<script setup>
import Sidebar from '@/components/Sidebar.vue'
import { computed, onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import defaultPhoto from '@/assets/Profile.webp'
import PasswordModal from '@/components/PasswordModal.vue'

const userStore = useUserStore()
const user = computed(() => userStore.user)
const API_URL = import.meta.env.VITE_API_URL

const levelFormatted = {
  begginer: () => 'Principiante',
  amateur: () => 'Intermedio',
  advanced: () => 'Avanzado',
  elite: () => 'Élite',
}

const displayPhoto = computed(() => {
  if (user.value.profile_photo && user.value.profile_photo !== '') {
    return `${API_URL}/${user.value.profile_photo}`
  }

  return defaultPhoto
})
const isModalOpen = ref(false)
onMounted(async () => {
  await userStore.fetchProfile()
})
</script>

<template>
  <main class="flex-1 bg-neutral-back-auth pt-5">
    <Sidebar class="hidden md:block" />
    <div class="md:ml-64 md:pl-13 lg:px-16 p-4 lg:pt-0 gap-10">
      <div class="flex gap-12">
        <img
          :src="displayPhoto"
          alt="Profile picture"
          class="max-w-60 max-h-60"
          v-if="user?.name"
        />
        <div class="flex items-end justify-between w-full">
          <div class="flex flex-col -gap-1">
            <h1 class="text-8xl text-primary-too-dark font-headline font-bold capitalize">
              {{ user?.name + ' ' + user?.surname }}
            </h1>
            <div class="flex gap-3 items-end -mt-4">
              <p class="text-secondary-light uppercase text-lg font-label traking-wider">
                @{{ user?.username }}
              </p>
              <div class="w-2 h-2 bg-secondary-light rounded-full self-center"></div>
              <p class="text-md font-headline lowercase text-neutral-light">
                {{ user?.nickname }}
              </p>
            </div>
          </div>
          <RouterLink
            to="/dashboard/edit-profile"
            class="text-sm font-bold bg-[#002F0A] text-white py-3 px-12 cursor-pointer hover:bg-primary/60"
            >Editar perfil</RouterLink
          >
        </div>
      </div>
      <div class="grid md:grid-cols-5 grid-cols-1 md:grid-rows-3 mt-15 gap-10">
        <div class="md:col-span-3 p-15 bg-neutral-back">
          <h1 class="capitalize text-3xl text-secondary-dark font-headline font-semibold">
            Información personal
          </h1>
          <div class="mt-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
            <div class="border-b py-2 border-neutral/40">
              <h4 class="text-sm uppercase text-neutral/60 font-label font-semibold tracking-wide">
                Username
              </h4>
              <p class="text-secondary-dark text-body">{{ user?.username }}</p>
            </div>
            <div class="border-b py-2 border-neutral/40">
              <h4 class="text-sm uppercase text-neutral/60 font-label font-semibold tracking-wide">
                Cumpleaños
              </h4>
              <p class="text-secondary-dark text-body">{{ user?.birthdate.formatted }}</p>
            </div>
            <div class="border-b py-2 border-neutral/40">
              <h4 class="text-sm uppercase text-neutral/60 font-label font-semibold tracking-wide">
                Email
              </h4>
              <p class="text-secondary-dark text-body">{{ user?.email }}</p>
            </div>
          </div>
        </div>
        <div class="md:col-span-2 md:row-span-3 bg-[#002F0A] p-15 flex flex-col justify-between">
          <div class="">
            <h3 class="text-3xl text-primary-light font-headline mb-10">
              Calibración <br />
              fisiológica
            </h3>
            <h4
              class="uppercase text-xs font-label text-primary-light/50 tracking-wider font-semibold"
            >
              Peso (kg)
            </h4>
            <p class="text-8xl font-headline font-bold mt-10 text-white">
              {{ user?.weight }}
              <span class="uppercase text-primary-light/50 text-3xl -ml-4">kg</span>
            </p>
            <h4
              class="uppercase text-xs font-label text-primary-light/50 tracking-wider font-semibold mt-10 flex gap-10"
            >
              Frecuencia cardíaca máxima (ppm)
            </h4>
            <p class="text-8xl font-headline font-bold mt-10 text-white">
              {{ user?.max_hr }}
              <span class="uppercase text-primary-light/50 text-3xl -ml-4">ppm</span>
            </p>
            <h4
              class="uppercase text-xs font-label text-primary-light/50 tracking-wider font-semibold mt-10"
            >
              Frecuencia cardíaca en reposo (ppm)
            </h4>
            <p class="text-8xl font-headline font-bold mt-10 text-white">
              {{ user?.rest_hr }}
              <span class="uppercase text-primary-light/50 text-3xl -ml-4">ppm</span>
            </p>
          </div>
          <p class="text-xs font-headline text-primary-light/50 mt-10">
            Actualizado: {{ user?.last_update.formatted }}
          </p>
        </div>
        <div class="md:col-span-3 p-15 bg-neutral-back">
          <h1 class="capitalize text-3xl text-secondary-dark font-headline font-semibold">
            Información del corredor
          </h1>
          <div class="mt-10 grid grid-cols-1 md:grid-cols-2 gap-10">
            <div class="border-b py-2 border-neutral/40">
              <h4 class="text-sm uppercase text-neutral/60 font-label font-semibold tracking-wide">
                Nivel
              </h4>
              <p class="text-secondary-dark text-body">
                {{ user?.level ? levelFormatted[user?.level]() : 'Actualiza tu nivel' }}
              </p>
            </div>
            <div class="border-b py-2 border-neutral/40">
              <h4 class="text-sm uppercase text-neutral/60 font-label font-semibold tracking-wide">
                Distancia objetivo
              </h4>
              <p class="text-secondary-dark text-body">
                {{ user?.obj_distance ? user?.obj_distance : 'Actualiza tu distancia objetivo' }}
              </p>
            </div>
          </div>
        </div>
        <div class="md:col-span-3 md:row-span-1 p-15 bg-neutral-back">
          <div class="">
            <h4 class="font-headline text-2xl text-secondary font-semibold">
              Registro del sistema
            </h4>
            <div class="mt-2 flex justify-between items-center">
              <div class="uppercase font-label text-neutral font-semibold">Alta</div>
              <p class="font-body text-secondary font-semibold">
                {{ user?.registration_date.formatted }}
              </p>
            </div>
            <div class="mt-4 flex justify-between items-center">
              <div class="uppercase font-label text-neutral font-semibold">Tipo de acceso</div>
              <p
                class="font-body text-secondary uppercase text-sm px-2 py-0.5 bg-secondary-light/20 font-semibold"
              >
                Premium
              </p>
            </div>
          </div>
          <div class="grid items-center grid-cols-4 mt-2">
            <div class="col-span-3">
              <h4 class="font-headline text-2xl text-secondary font-semibold">
                Seguridad & autenticación
              </h4>
              <p class="text-body text-neutral tracking-wide">
                Controla tus credenciales y el acceso de protocolos.
              </p>
            </div>

            <button
              @click="isModalOpen = true"
              class="p-2 cursor-pointer bg-secondary-light/20 text-secondary font-semibold hover:bg-secondary-light/50"
            >
              <h5 class="text-sm">Cambiar contraseña</h5>
            </button>
            <PasswordModal v-if="isModalOpen" @close="isModalOpen = false" />
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
