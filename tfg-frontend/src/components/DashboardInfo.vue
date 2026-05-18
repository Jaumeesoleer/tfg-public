<script setup>
import Chrono from '@/assets/svg/Chrono.vue'
import Speed from '@/assets/svg/Speed.vue'
import Bolt from '@/assets/svg/Bolt.vue'
import Heart from '@/assets/svg/Heart.vue'
import { computed } from 'vue'

const svgs = {
  Chrono,
  Speed,
  Bolt,
  Heart,
}

const props = defineProps({
  value: {
    type: [String, Number],
    required: true,
  },
  svg: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    required: true,
  },
  diff: {
    type: String,
    default: '',
  },
  comp: {
    type: String,
    default: '',
  },
  bg: {
    type: String,
    default: 'bg-white',
  },
  v: {
    type: String,
    default: '',
  },
})
const classStyle = computed(() => {
  const baseClasses = 'px-2 py-0.5 font-extrabold text-xs uppercase'
  const numDiff = parseFloat(props.diff)

  if (numDiff > 0) {
    return `${baseClasses} text-primary-dark bg-primary-light`
  } else if (numDiff == 0) {
    return `${baseClasses} text-secondary-dark bg-secondary-light/60 uppercase`
  }
  return `${baseClasses} bg-red-200 text-light-red`
})

const symbol = computed(() => {
  const numDiff = parseFloat(props.diff)
  if (isNaN(numDiff) || numDiff === 0) return ''
  return numDiff > 0 ? '+' : ''
})
</script>

<template>
  <div :class="bg" class="p-5 flex flex-col gap-2">
    <component
      v-if="svg"
      :is="svgs[svg]"
      class="w-7 h-7 stroke-secondary-light"
      :class="[svg === 'Heart' || svg === 'Bolt' ? 'fill-secondary-light' : '']"
    />
    <h4 class="text-xs uppercase text-neutral/80 font-semibold">{{ title }}</h4>
    <div :class="[!diff ? 'flex items-end gap-1' : '']">
      <p class="-mt-1 text-3xl font-headline font-bold">{{ value + v }}</p>
      <p v-if="!diff" class="text-[10px] text-neutral/60 mb-1">
        {{ comp }}
      </p>
      <div v-if="diff" class="flex gap-2 items-center">
        <div class="" v-if="comp === 'Model Health'">
          <p v-if="parseFloat(diff) < 0" class="" :class="classStyle">Low</p>
          <p v-if="parseFloat(diff) > 0" class="" :class="classStyle">High</p>
          <p v-if="parseFloat(diff) === 0" class="" :class="classStyle">Stable</p>
        </div>
        <div v-else>
          <p v-if="parseFloat(diff) === 0" :class="classStyle">Stable</p>
          <p v-else :class="classStyle">{{ symbol }}{{ diff }}%</p>
        </div>
        <p class="text-[10px] text-neutral/60">{{ comp }}</p>
      </div>
    </div>
  </div>
</template>
