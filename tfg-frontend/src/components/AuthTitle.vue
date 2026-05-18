<script setup>
defineProps({
  color: {
    type: String,
    default: 'text-primary-too-dark',
  },
  title: {
    type: String,
    required: true,
  },
  titleClass: {
    type: String,
    default: 'font-headline text-5xl font-bold capitalize',
  },
  subtitle: {
    type: String,
    required: true,
  },
  subtitleClass: {
    type: String,
    default: 'font-label text-neutral-light mt-2 tracking-wide',
  },
})
</script>

<template>
  <div class="max-w-2xl">
    <h1 :class="[color, titleClass]">{{ title }}</h1>
    <p :class="[subtitleClass]">{{ subtitle }}</p>
  </div>
</template>
