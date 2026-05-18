<script setup>
import Settings from '@/assets/svg/Settings.vue'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const handleLogout = async () => {
  try {
    await userStore.logoutUser()
  } finally {
    localStorage.removeItem('isLoggedIn')
    router.push('/')
  }
}
</script>

<template>
  <Menu as="div" class="relative inline-block">
    <MenuButton
      class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white/10 px-3 py-2 text-sm font-semibold text-white inset-ring-1 inset-ring-white/5 hover:bg-white/20"
    >
      <Settings />
    </MenuButton>

    <transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <MenuItems
        class="absolute right-0 z-10 mb-2 w-56 origin-bottom-right bottom-full rounded-md bg-secondary-light outline-1 -outline-offset-1 outline-white/10"
      >
        <div class="py-1">
          <MenuItem v-slot="{ active }">
            <RouterLink
              to="/support"
              :class="[
                active ? 'bg-white/5 outline-hidden' : '',
                'block text-white px-4 py-2 text-sm',
              ]"
              >Soporte</RouterLink
            >
          </MenuItem>
          <MenuItem v-slot="{ active }">
            <RouterLink
              to="/license"
              :class="[
                active ? 'bg-white/5 outline-hidden' : '',
                'block text-white px-4 py-2 text-sm',
              ]"
              >Licencia</RouterLink
            >
          </MenuItem>
          <MenuItem v-slot="{ active }">
            <button
              type="button"
              @click="handleLogout"
              :class="[
                active ? 'bg-white/5 outline-hidden' : '',
                'w-full text-left cursor-pointer text-white px-4 py-2 text-sm',
              ]"
            >
              Sign out
            </button>
          </MenuItem>
        </div>
      </MenuItems>
    </transition>
  </Menu>
</template>
