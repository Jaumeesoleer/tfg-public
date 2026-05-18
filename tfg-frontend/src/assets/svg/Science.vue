<template>
  <svg
    :width="width"
    :height="height"
    viewBox="3 0 24 24"
    fill="none"
    preserveAspectRatio="xMinYMid meet"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M10 4V10L5.20285 16.8531C4.27496 18.1786 5.22327 20 6.84131 20H17.1587C18.7767 20 19.725 18.1786 18.7972 16.8531L14 10V4M10 4H14M10 4H8M14 4H16"
      stroke-width="1.6799999999999997"
      stroke-linecap="round"
      stroke-linejoin="round"
    ></path>
  </svg>
</template>

<script setup>
defineProps({
  width: {
    type: String,
    default: '24',
  },
  height: {
    type: String,
    default: '24',
  },
})
</script>
