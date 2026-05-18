<script setup>
import { computed } from 'vue'
const props = defineProps({
  value: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
})
const formattedValue = computed(() => {
  const match = String(props.value).match(/^([\d.]+)(.*)$/)
  if (!match) return { nums: props.value, unit: '' }
  return {
    num: match[1],
    unit: match[2],
  }
})
</script>

<template>
  <div>
    <div class="font-headline text-2xl sm:text-4xl text-primary-too-dark font-bold">
      {{ formattedValue.num }}
      <span class="text-xl">{{ formattedValue.unit }}</span>
    </div>
    <p class="text-[10px] text-neutral-light font-label uppercase text-outline tracking-wider">
      {{ name }}
    </p>
  </div>
</template>
