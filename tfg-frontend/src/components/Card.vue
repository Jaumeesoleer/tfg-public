<script setup>
import { onMounted, ref } from 'vue'
import { Green, Red, Yellow } from '@/assets/svg/light'

const props = defineProps({
  date: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  lasts: {
    type: Array,
    required: true,
  },
})

const barChar = () => {
  values.value = props.lasts.map((l) => l / 10)
  r.value = values.value.reduce((acc, val) => acc + val, 0) / values.value.length
  if (r.value < 5) rate.value = 0
  else if (r.value >= 5 && r.value < 6) rate.value = 1
  else rate.value = 2
}
const r = ref(0)
const rate = ref(0)
const values = ref([])

const rateDict = {
  0: ['Alerta', Red, 'text-light-red stroke-light-red', 'fill-light-red', 'bg-light-red'],
  1: [
    'Suficiente',
    Yellow,
    'text-light-yellow stroke-light-yellow',
    'fill-light-yellow',
    'bg-light-yellow',
  ],
  2: ['Bien', Green, 'text-light-green stroke-light-green', 'fill-light-green', 'bg-light-green'],
}
onMounted(() => {
  barChar()
})
</script>
<template>
  <div class="font-body tracking-wider text-xs flex justify-between">
    <p class="uppercase text-neutral-light font-semibold">{{ date }}</p>
    <div class="flex gap-1 font-bold" :class="rateDict[rate][2]">
      <component :is="rateDict[rate][1]" class="w-4 h-4" />
      <p>{{ rateDict[rate][0] }}</p>
    </div>
  </div>
  <h5 class="capitalize text-primary-dark font-headline text-2xl font-bold">{{ title }}</h5>
  <div class="flex justify-between items-center">
    <div class="flex items-end gap-1 h-12">
      <div
        v-for="(value, index) in values"
        :key="index"
        class="w-2"
        :class="rateDict[rate][4]"
        :style="{ height: value * 5 + 'px', opacity: value / 10 }"
      ></div>
    </div>
    <p class="text-2xl font-bold font-headline text-primary-dark">
      {{ Math.round(r * 10) }}<span class="font-normal font-label text-neutral text-xs">pts</span>
    </p>
  </div>
</template>
