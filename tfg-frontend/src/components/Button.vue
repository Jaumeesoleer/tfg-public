<script setup>
import Lock from '@/assets/svg/Lock.vue'
import RightArrow from '@/assets/svg/RightArrow.vue'
import LeftArrow from '@/assets/svg/LeftArrow.vue'
const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  type: {
    type: String,
    default: 'submit',
  },
  content: {
    type: String,
    required: true,
  },
  change: {
    type: String,
    default: 'Entrando...',
  },
  colors: {
    type: String,
    default: 'bg-primary-ultra text-white',
  },
  hover: {
    type: String,
    default: 'hover:bg-primary-ultra/80',
  },
  border: {
    type: String,
    default: 'border-1',
  },
  bold: {
    type: String,
    default: 'font-semibold',
  },
  w: {
    type: String,
    default: 'w-full',
  },
  isLock: {
    type: Boolean,
    default: false,
  },
  classes: {
    type: String,
    default: 'text-sm tracking-widest uppercase py-4',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  click: { type: Function, default: null },
  cursor: { type: String, default: 'cursor-pointer' },
})
</script>

<template>
  <button
    v-bind="$attrs"
    v-on="props.click ? { click: props.click } : {}"
    :disabled="disabled"
    :type="type"
    class="font-label rounded-sm transition-all active:scale-[0.98]"
    :class="[
      isLock
        ? [colors, hover, border, bold, w, classes, ['flex items-center justify-center gap-2']]
        : [colors, hover, border, bold, w, classes],
      cursor,
    ]"
  >
    <RightArrow v-if="content === 'RightArrow'" class="w-full mx-auto" />
    <LeftArrow v-else-if="content === 'LeftArrow'" class="w-full mx-auto" />
    <template v-else>
      <component v-if="isLock" :is="Lock" />
      <p>{{ loading ? change : content }}</p>
    </template>
  </button>
</template>
