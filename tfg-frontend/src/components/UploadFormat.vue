<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  text: {
    type: String,
    required: true,
  },
  atr: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    required: true,
  },
})
const type = {
  primary: ['bg-primary-dark', 'text-primary'],
  secondary: ['bg-secondary-dark', 'text-secondary'],
}
</script>

<template>
  <div class="mt-4 flex items-center gap-2">
    <div class="w-2 h-2 rounded-full hidden md:block" :class="type[color][0]"></div>
    <h4 class="text-primary-too-dark text-xl md:text-2xl font-headline font-bold">
      {{ title }}
    </h4>
  </div>
  <p class="mt-2 font-body text-sm text-neutral/80">
    {{ text }}
  </p>
  <div class="bg-neutral-back-auth p-3 mt-2">
    <p class="font-mono text-[10px] md:text-xs" :class="type[color][1]">
      {{ atr }}
    </p>
  </div>
</template>
