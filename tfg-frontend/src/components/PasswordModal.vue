<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'

defineEmits(['close'])
const userStore = useUserStore()
const router = useRouter()

const password = ref('')
const newPassword = ref('')
const repeatNewPassword = ref('')

const errorMessage = ref('')

const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/

const isPasswordStrong = computed(() => {
  return passwordRegex.test(newPassword.value)
})

const checkPassword = computed(() => {
  if (newPassword.value.length === 0) return 0
  if (!isPasswordStrong.value) return 1
  if (newPassword.value !== repeatNewPassword.value) return 2
  return 3
})

const handleNewPassword = async () => {
  try {
    await userStore.newPassword({
      password: password.value,
      newPassword: newPassword.value,
    })
    router.push('/dashboard/profile')
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Error al conectar con el servidor'
    console.log(errorMessage.value)
  }
}
</script>

<template>
  <div
    class="fixed inset-0 z-100 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm transition-opacity"
    @click.self="$emit('close')"
  >
    <div
      class="bg-white w-full max-w-md p-8 rounded-none border border-outline-variant/30 shadow-2xl space-y-8"
    >
      <div class="space-y-2">
        <h2 class="text-2xl font-serif text-on-surface text-secondary-too-dark">
          Security Protocol: Update Credentials
        </h2>
        <div class="h-px w-12 bg-secondary"></div>
      </div>

      <form @submit.prevent="handleNewPassword">
        <div class="space-y-6">
          <div class="space-y-2">
            <label class="text-[11px] font-bold uppercase tracking-widest text-slate-500 label-font"
              >Current Password</label
            >
            <input
              class="w-full scientific-input px-4 py-3 rounded-none text-primary-too-dark border border-slate-200 focus:outline-none focus:border-slate-400"
              placeholder="••••••••••••"
              type="password"
              v-model="password"
            />
          </div>
          <div class="space-y-2">
            <label
              class="text-[11px] font-bold uppercase tracking-widest text-slate-500 label-font"
              >{{
                checkPassword == 1
                  ? 'La contraseña debe contener un número y tener 8 carácteres'
                  : 'New password'
              }}</label
            >
            <input
              class="w-full scientific-input px-4 py-3 rounded-none text-primary-too-dark border focus:outline-none"
              :class="[
                checkPassword == 1
                  ? 'border-light-red focus:border-light-red'
                  : 'border-slate-200 focus:border-slate-400',
              ]"
              placeholder="••••••••••••"
              type="password"
              v-model="newPassword"
            />
          </div>
          <div class="space-y-2">
            <label
              class="text-[11px] font-bold uppercase tracking-widest text-slate-500 label-font"
            >
              {{
                checkPassword == 2 ? 'Las constraseñas no coinciden' : 'Confirm new password'
              }}</label
            >
            <input
              class="w-full scientific-input px-4 py-3 rounded-none text-primary-too-dark border focus:outline-none"
              :class="[
                checkPassword == 2 ? 'border-light-red' : 'border-slate-200 focus:border-slate-400',
              ]"
              placeholder="••••••••••••"
              type="password"
              v-model="repeatNewPassword"
            />
          </div>
        </div>

        <div class="p-4 bg-surface-container-low border-l-2 border-secondary bg-slate-50 my-4">
          <p class="text-xs text-slate-600 leading-relaxed italic label-font">
            Passwords must be at least 8 characters and include clinical-grade complexity
            (alphanumeric with symbols).
          </p>
        </div>

        <div class="my-2 bg-light-red/40" v-if="errorMessage">
          <p class="text-light-red uppercase font-bold tracking-widest text-xs text-center py-2">
            {{ errorMessage }}
          </p>
        </div>

        <div class="flex items-center justify-end gap-4">
          <button
            @click="$emit('close')"
            type="button"
            class="px-6 py-3 text-slate-500 font-bold text-xs uppercase tracking-widest hover:text-slate-900 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="checkPassword !== 3 || !password"
            class="px-8 py-3 bg-[#14411A] text-white font-bold text-xs uppercase tracking-widest shadow-lg hover:brightness-110 transition-all z-9999999 cursor-pointer"
          >
            Confirm Update
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
