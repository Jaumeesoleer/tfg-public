<script setup>
import AuthTitle from '@/components/AuthTitle.vue'
import Sidebar from '@/components/Sidebar.vue'
import Button from '@/components/Button.vue'
import Labels from '@/components/Labels.vue'
import RightArrow from '@/assets/svg/RightArrow.vue'
import Lock from '@/assets/svg/Lock.vue'
import { computed, onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import PasswordModal from '@/components/PasswordModal.vue'
import defaultPhoto from '@/assets/Profile.webp'

const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL

const errorMessage = ref('')
const emailError = ref('')
const usernameError = ref('')
const weightError = ref('')
const birthdateError = ref('')

const selectedFile = ref(null)
const imagePreview = ref(null)

const name = ref('')
const surname = ref('')
const username = ref('')
const email = ref('')
const birthdate = ref('')
const nickname = ref('')
const weight = ref('')
const maxHr = ref('')
const level = ref('')
const objRun = ref('')

const userStore = useUserStore()
const user = computed(() => userStore.user)

const isModalOpen = ref(false)

const onFileSelected = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    imagePreview.value = URL.createObjectURL(file)
  }
}
const displayPhoto = computed(() => {
  if (imagePreview.value && imagePreview.value.startsWith('blob:')) {
    return imagePreview.value
  }

  if (imagePreview.value && imagePreview.value !== '') {
    return `${API_URL}/${imagePreview.value}`
  }

  return defaultPhoto
})

const handleUpdate = async () => {
  try {
    const formData = new FormData()

    formData.append('name', name.value)
    formData.append('surname', surname.value)
    formData.append('username', username.value)
    formData.append('email', email.value)
    formData.append('birthdate', birthdate.value)
    formData.append('nickname', nickname.value)
    formData.append('weight', weight.value)
    formData.append('maxHr', maxHr.value)
    formData.append('level', level.value)
    formData.append('objRun', objRun.value)

    if (selectedFile.value) {
      formData.append('profile_photo', selectedFile.value)
    }
    await userStore.updateProfile(formData)

    router.push('/dashboard/profile')
  } catch (error) {
    errorMessage.value = error.response?.data?.error
    emailError.value = error.response?.data?.emailError
    usernameError.value = error.response?.data?.usernameError
    weightError.value = error.response?.data?.weightError
    birthdateError.value = error.response?.data?.birthdateError
  }
}

onMounted(async () => {
  await userStore.fetchProfile()

  if (user.value) {
    name.value = user.value.name
    surname.value = user.value.surname
    username.value = user.value.username
    email.value = user.value.email
    birthdate.value = user.value.birthdate.short
    nickname.value = user.value.nickname
    weight.value = user.value.weight
    maxHr.value = user.value.max_hr
    imagePreview.value = user.value.profile_photo
    level.value = user.value.level
    objRun.value = user.value.obj_distance
  }
})
</script>

<template>
  <main class="flex-1 bg-neutral-back-auth pt-5">
    <Sidebar />
    <div class="md:ml-64 md:pl-13 lg:px-16 p-4 lg:pt-0 gap-10">
      <AuthTitle
        title="Editar perfil profesional"
        subtitle="Modifique sus credenciales clínicas, los parámetros fisiológicos de línea base y los protocolos de autenticación dentro del ecosistema de The Architect."
        class="pt-8"
      />
      <div class="mt-10 grid grid-cols-1 md:grid-cols-12 gap-5 border-b border-neutral/40 pb-10">
        <div class="md:col-span-3 bg-neutral-back p-10 h-fit">
          <img :src="displayPhoto" alt="Profile photo" class="border-xl p-4" />
          <h4 class="text-center text-2xl font-headline font-bold">Foto de perfil</h4>
          <p class="text-xs text-neutral text-center font-body tracking-wide -mt-1">
            JPG o PNG. Max 5MB
          </p>
          <input
            type="file"
            ref="fileInput"
            class="hidden"
            accept="image/png, image/jpeg, image/webp, image/jpg"
            @change="onFileSelected"
          />
          <Button
            content="Cambiar imagen"
            colors="text-secondary-light"
            border="border-1 border-secondary-light/30"
            hover="hover:bg-secondary-light/10"
            bold="font-bold"
            classes="p-3 uppercase tracking-wider text-[10px] mt-4"
            w="w-full"
            @click="$refs.fileInput.click()"
          />
        </div>
        <div class="md:col-span-9 bg-neutral-back p-8">
          <h4 class="w-full border-b border-neutral/30 mb-8 text-3xl font-headline capitalize pb-3">
            Credenciales personales
          </h4>
          <form
            @submit.prevent="handleUpdate"
            class="grid grid-cols-1 md:grid-cols-3 gap-10"
            id="profileForm"
          >
            <Labels
              label="Nombre"
              id="name"
              div-classes="rounded-sm p-4 border-b-2 border-[#c7c5d3] focus-within:border-secondary-light"
              v-model="name"
            />
            <Labels
              label="Apellido"
              id="surname"
              div-classes="rounded-sm p-4  border-b-2 border-[#c7c5d3] focus-within:border-secondary-light"
              v-model="surname"
            />
            <Labels
              label="Username"
              id="username"
              div-classes="rounded-sm p-4 border-b-2 border-[#c7c5d3] focus-within:border-secondary-light"
              v-model="username"
            />
            <Labels
              label="Nickname"
              id="email"
              div-classes="rounded-sm p-4 border-b-2 border-[#c7c5d3] focus-within:border-secondary-light"
              v-model="nickname"
            />
            <Labels
              label="Email"
              :model-value="user?.email"
              id="email"
              div-classes="rounded-sm p-4 border-b-2 border-[#c7c5d3] focus-within:border-secondary-light"
              v-model="email"
            />
            <Labels
              label="Cumpleaños"
              type="date"
              id="birthdate"
              div-classes="rounded-sm p-4 border-b-2 border-[#c7c5d3] focus-within:border-secondary-light"
              v-model="birthdate"
            />
            <div
              class="rounded-sm flex flex-col p-4 border-b-2 border-[#c7c5d3] transition-all focus-within:border-secondary-light"
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
            <div
              class="rounded-sm flex flex-col p-4 border-b-2 border-[#c7c5d3] transition-all focus-within:border-secondary-light"
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
            <div class="grid md:grid-cols-2 text-center">
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
          </form>
        </div>
        <div class="md:col-span-8 bg-neutral-back p-8">
          <h4 class="w-full text-3xl font-headline border-b border-neutral/30 pb-3">
            Base fisiológica
          </h4>
          <div class="flex gap-4">
            <div class="flex items-end">
              <Labels
                label="body mass (kg)"
                id="kg"
                type="numeric"
                div-classes="rounded-b-sm py-4  border-b-2 border-[#c7c5d3] focus-within:border-secondary-light text-2xl font-bold"
                v-model="weight"
              />
              <p class="p-4 font-headline text-neutral text-xl">kg</p>
            </div>
            <div class="flex items-end">
              <Labels
                label="Frecuencia cardíaca máxima (ppm)"
                id="max-hr"
                type="numeric"
                div-classes="rounded-b-sm py-4  border-b-2 border-[#c7c5d3] focus-within:border-secondary-light text-2xl font-bold"
                v-model="maxHr"
              />
              <p class="p-4 font-headline text-neutral text-xl">ppm</p>
            </div>
          </div>
          <p class="text-xs text-neutral/50 mt-4">
            Nota: Modificar estos valores llevaran a una recalibración de su informe de métricas
            avanzadas
          </p>
        </div>
        <div class="md:col-span-4 bg-[#0F172A] p-8 text-white">
          <div class="flex items-center gap-3">
            <Lock class="stroke-secondary-light" />
            <h4 class="text-xl font-headline">Protocolo de seguridad</h4>
          </div>
          <p class="text-white/50 text-xs mt-4 font-label mb-8">
            Asegúrese de que sus credenciales mantengan el nivel más alto de cifrado actualizando su
            token de autenticación periódicamente.
          </p>

          <button
            @click="isModalOpen = true"
            class="bg-white/10 text-white flex items-center justify-between p-2 rounded-md uppercase font-label hover:bg-white/30 text-xs border border-white/50 w-full cursor-pointer"
          >
            <h5>Cambiar contraseña</h5>
            <RightArrow />
          </button>
          <PasswordModal v-if="isModalOpen" @close="isModalOpen = false" />
        </div>
      </div>
      <div class="flex items-center justify-between mt-10 text-neutral">
        <p class="text-xs font-label">Última actualización: {{ user?.last_update.formatted }}</p>
        <div class="flex gap-10 items-center">
          <RouterLink
            to="dashboard/profile"
            class="uppercase text-xs tracking-wide font-label cursor-pointer hover:underline"
            >Cancelar</RouterLink
          >
          <Button
            content="Guardar cambios"
            classes="px-7 py-3 font-label tracking-widest uppercase text-xs"
            @click="handleUpdate"
          />
        </div>
      </div>
    </div>
  </main>
</template>
