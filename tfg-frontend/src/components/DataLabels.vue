<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  id: {
    type: String,
    default: '',
  },
  text: {
    type: String,
    required: true,
  },
  placeholder: {
    type: String,
    required: true,
  },
  modelValue: {
    type: [String, Number],
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div :class="id">
    <label for="" class="uppercase font-semibold font-xs text-secondary-light">{{ title }}</label>
    <div
      class="mt-4 bg-neutral-back-auth flex justify-between outline outline-neutral/40 border-b border-neutral/40 rounded-t-md p-2 items-end placeholder-neutral-light"
    >
      <input
        :id="id"
        type="numeric"
        :placeholder="placeholder"
        class="apearance-none w-full"
        :value="modelValue"
        @input="emit('update:modelValue', $event.target.value)"
      />
      <p class="uppercase font-semibold font-label text-[10px] text-neutral-light">ppm</p>
    </div>
    <p class="text-xs font-body mt-1 text-neutral-light tracking-wide">{{ text }}</p>
  </div>
</template>
