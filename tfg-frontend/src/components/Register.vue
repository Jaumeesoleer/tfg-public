<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import Label from '@/components/Labels.vue'
import Button from '@/components/Button.vue'

const username = ref('')
const name = ref('')
const surname = ref('')
const birthDate = ref('')
const email = ref('')
const password = ref('')
const passwordCheck = ref('')
const weight = ref('')
const fc_max = ref('')
const errorMessage = ref('')
const usernameError = ref('')
const nameError = ref('')
const surnameError = ref('')
const nicknameError = ref('')
const dateError = ref('')
const emailError = ref('')
const gender = ref('')
const nickname = ref('')
const level = ref('')
const objRun = ref('')
const userStore = useUserStore()
const router = useRouter()

const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/

const isPasswordStrong = computed(() => {
  return passwordRegex.test(password.value)
})

const checkPassword = computed(() => {
  if (password.value.length === 0) return 0
  if (!isPasswordStrong.value) return 1
  if (password.value !== passwordCheck.value) return 2
  return 3
})

const handleRegister = async () => {
  try {
    await userStore.registerUser({
      username: username.value,
      nickname: nickname.value,
      name: name.value,
      surname: surname.value,
      birthDate: birthDate.value,
      email: email.value,
      password: password.value,
      passwordCheck: passwordCheck.value,
      gender: gender.value,
      weight: weight.value,
      fc_max: fc_max.value,
      level: level.value,
      objRun: objRun.value,
    })
    router.push('/')
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Error al conectar con el servidor'
    usernameError.value = error.response?.data?.errorUsername || false
    nameError.value = error.response?.data?.errorName || false
    emailError.value = error.response?.data?.errorEmail || false
    dateError.value = error.response?.data?.errorDate || false
    surnameError.value = error.response?.data?.errorSurname || false
    nicknameError.value = error.response?.data?.errorNickname || false
    nameError.value = error.response?.data?.nameError || false
    console.log(usernameError)
  }
}

const page = ref(1)
</script>

<template>
  <div class="flex flex-col justify-between h-full mx-auto pb-20">
    <div class="">
      <h1 class="mb-10 font-headline text-3xl text-primary-too-dark">Registrate</h1>
      <form @submit.prevent="handleRegister">
        <div class="flex flex-col gap-6" v-show="page === 1">
          <Label
            id="username"
            :label="usernameError ? 'Username ya registrado, utilice otro' : 'Username'"
            v-model="username"
            placeholder="analyticMan2"
            :class="[usernameError ? 'border-light-red' : '']"
          />
          <Label
            id="nickname"
            :label="nicknameError ? 'Error en el nickname' : 'Nickname'"
            v-model="nickname"
            placeholder="Hyrox Runner"
            :class="[nicknameError ? 'border-light-red' : '']"
          />
          <div class="flex gap-2 justify-between">
            <Label
              id="name"
              :label="nameError ? 'Error en el nombre' : 'Nombre'"
              v-model="name"
              placeholder="Julen"
              class="w-full"
              :class="[nameError ? 'border-light-red' : '']"
            />
            <Label
              id="surname"
              :label="surnameError ? 'Error en el apellido' : 'Apellido'"
              v-model="surname"
              placeholder="Cardo"
              class="w-full"
              :class="[surnameError ? 'border-light-red' : '']"
            />
          </div>
        </div>

        <div class="flex flex-col gap-6" v-show="page === 2">
          <Label
            id="birthdate"
            :label="dateError ? 'Error en la fecha' : 'Cumpleaños'"
            v-model="birthDate"
            type="date"
            placeholder="29/07/2003"
            :class="[dateError ? 'border-light-red' : '']"
          />
          <Label
            id="email"
            :label="dateError ? 'Correo ya registrado' : 'Email'"
            v-model="email"
            type="email"
            placeholder="analytical@architect.com"
            :class="[emailError ? 'border-light-red' : '']"
          />
        </div>

        <div class="flex flex-col gap-6" v-show="page === 3">
          <div
            class="bg-[#dfe3e6] rounded-t-lg flex flex-col p-4 border-b-2 border-[#c7c5d3] transition-all focus-within:bg-white focus-within:border-secondary-light"
          >
            <label
              class="text-[10px] bloc font-label tracking-widest text-outline mb-1 uppercase text-neutral"
              for="level"
            >
              Nivel
            </label>
            <select
              v-model="level"
              id="level"
              class="w-full text-primary-too-dark placeholder:text-neutral/50 focus:ring-0 font-body focus-visible:outline-none"
            >
              <option value="" disabled selected>Selecciona uno</option>
              <option value="begginer">Principiante</option>
              <option value="amateur">Intermedio</option>
              <option value="advanced">Avanzado</option>
              <option value="elite">Élite</option>
            </select>
          </div>
          <div class="grid grid-cols-4 text-center">
            <p
              class="bg-primary-light rounded-md text-primary-too-dark w-fit m-auto px-2 cursor-default"
              v-tooltip.bottom="{
                value: 'Ideal si estás empezando',
              }"
            >
              Princpiante
            </p>
            <p
              class="bg-secondary-light/60 rounded-md text-secondary w-fit m-auto px-2 cursor-default"
              v-tooltip.bottom="{
                value: 'Ideal si entrenas con regularidad',
              }"
            >
              Intermedio
            </p>
            <p
              class="bg-light-red/50 rounded-md text-light-red w-fit m-auto px-2 cursor-default"
              v-tooltip.bottom="{
                value: 'Ideal si sigues planes para mejorar tiempos',
              }"
            >
              Avanzado
            </p>
            <p
              class="bg-[#673AB74D] rounded-md text-[#673AB7] w-fit m-auto px-2 cursor-default"
              v-tooltip.bottom="{
                value: 'Ideal si compites por puestos en la clasificación general',
              }"
            >
              Elite
            </p>
          </div>
          <div
            class="bg-[#dfe3e6] rounded-t-lg flex flex-col p-4 border-b-2 border-[#c7c5d3] transition-all focus-within:bg-white focus-within:border-secondary-light"
          >
            <label
              class="text-[10px] bloc font-label tracking-widest text-outline mb-1 uppercase text-neutral"
              for="objRun"
            >
              Tu distancia objetivo
            </label>
            <select
              v-model="objRun"
              id="objRun"
              class="w-full text-primary-too-dark placeholder:text-neutral/50 focus:ring-0 font-body focus-visible:outline-none"
            >
              <option value="" disabled selected>Selecciona uno</option>
              <option value="5">5k</option>
              <option value="10">10k</option>
              <option value="21">21k</option>
              <option value="42">42k</option>
            </select>
          </div>
        </div>
        <div class="flex flex-col gap-6" v-show="page === 4">
          <Label
            id="password"
            :label="
              checkPassword == 1
                ? 'La contraseña debe contener un número y tener 8 carácteres'
                : 'Contraseña'
            "
            v-model="password"
            type="password"
            placeholder="••••••••••••"
            :class="[checkPassword == 1 ? 'border-light-red' : '']"
          />
          <Label
            id="passwordCheck"
            :label="checkPassword == 2 ? 'las Contraseñas no coinciden' : 'Repite la contraseña'"
            v-model="passwordCheck"
            type="password"
            placeholder="••••••••••••"
            :class="[checkPassword == 2 ? 'border-light-red' : '']"
          />
        </div>
        <div class="flex flex-col gap-6 mb-6" v-show="page === 5">
          <Label
            label="Tu peso en kg"
            id="weight"
            v-model="weight"
            placeholder="60 kg"
            type="numeral"
          />
          <Label
            id="fc_max"
            label="Tu FC máxima, solo sí la conoces"
            v-model="fc_max"
            type="numeral"
            placeholder="198 bpm"
            :required="false"
          />
          <Label
            label="Tu FC máxima, solo sí la conoces"
            type="numeral"
            placeholder="198 bpm"
            :required="false"
            class="hidden"
          />
          <div
            class="bg-[#dfe3e6] rounded-t-lg flex flex-col p-4 border-b-2 border-[#c7c5d3] transition-all focus-within:bg-white focus-within:border-secondary-light"
          >
            <label
              class="text-[10px] bloc font-label tracking-widest text-outline mb-1 uppercase text-neutral"
              for="gender"
            >
              Sexo
            </label>
            <select
              v-model="gender"
              id="gender"
              class="w-full text-primary-too-dark placeholder:text-neutral/50 focus:ring-0 font-body focus-visible:outline-none"
            >
              <option value="" disabled selected>Selecciona uno</option>
              <option value="male">Hombre</option>
              <option value="female">Mujer</option>
              <option value="other">Otro / Prefiero no decirlo</option>
            </select>
          </div>
        </div>
        <p
          v-if="errorMessage"
          class="text-light-red text-center mb-4 uppercase font-body"
          v-show="page === 5"
        >
          {{ errorMessage }}
        </p>
        <Button
          content="Registrarse"
          v-show="page === 5"
          :disabled="checkPassword !== 3"
          :cursor="checkPassword !== 3 ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'"
        />
      </form>
    </div>
    <div class="flex justify-end">
      <Button type="button" content="LeftArrow" @click="page--" v-if="page > 1" w="w-20" />
      <Button type="button" content="RightArrow" @click="page++" v-if="page < 5" w="w-20" />
      <div class="w-20" v-if="page === 5"></div>
    </div>
  </div>
</template>
