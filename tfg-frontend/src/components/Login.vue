<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import Label from '@/components/Labels.vue'
import Button from '@/components/Button.vue'

const username = ref('')
const password = ref('')
const remember = ref(false)
const errorMessage = ref('')

const userStore = useUserStore()
const router = useRouter()

const handleLogin = async () => {
  try {
    await userStore.loginUser({
      username: username.value,
      password: password.value,
      remember: remember.value,
    })

    localStorage.setItem('isLoggedIn', 'true')
    router.push('/dashboard')
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Error al conectar con el servidor'
  }
}
defineProps({
  bar: {
    type: Boolean,
    default: true,
  },
})
</script>

<template>
  <div
    v-if="bar"
    class="top-0 absolute left-0 w-full h-1 bg-linear-to-r from-primary-too-dark to-primary"
  ></div>
  <div class="mb-10">
    <h2 class="font-headline text-3xl text-primary-too-dark">Acceso de Analista</h2>
    <p class="font-body text-sm text-neutral mt-2">
      Introduzca sus credenciales para inicializar la consola arquitectónica.
    </p>
  </div>
  <form @submit.prevent="handleLogin" class="space-y-6">
    <Label
      label="Identificador de estación"
      v-model="username"
      placeholder="analyst_002"
      type="text"
    />
    <Label label="Cifrado encriptado" v-model="password" type="password" placeholder="·······" />
    <p v-if="errorMessage" style="color: red">{{ errorMessage }}</p>
    <div class="py-2 flex justify-between items-center text-xs font-body">
      <label class="flex items-center cursor-pointer gap-2">
        <input
          type="checkbox"
          class="rounded-sm focus:ring-primary-too-dark accent-primary-too-dark w-4 h-4"
          v-model="remember"
        />
        <span class="">Sesión persistente</span>
      </label>
      <a href="#" class="text-secondary-light font-label font-semibold hover:underline"
        >¿Revocar acceso?</a
      >
    </div>

    <Button content="Inicializar motor" />

    <div class="flex items-center relative py-4 gap-4">
      <div class="border-[#c7c5d34d] grow border-t"></div>
      <p class="text-[10px] uppercase text-neutral-light font-label">autenticación de pares</p>
      <div class="border-[#c7c5d34d] grow border-t"></div>
    </div>
    <Button
      content="Conectar con Strava"
      colors="bg-white text-orange-400"
      hover="hover:bg-neutral-back"
      border="border-1 border-[#c7c5d34d]"
      :disabled="true"
      cursor="cursor-not-allowed"
    />
  </form>
</template>
