<script setup>
import { ref } from 'vue'

const props = defineProps({
  label: String,
  id: String,
  modelValue: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  required: { type: Boolean, default: true },
  inputClasses: {
    type: String,
    default:
      'w-full text-primary-too-dark placeholder:text-neutral/50 focus:ring-0 font-body focus-visible:outline-none',
  },
  divClasses: {
    type: String,
    default:
      'bg-[#dfe3e6] rounded-t-lg flex flex-col p-4 border-b-2 border-[#c7c5d3] transition-all focus-within:bg-white focus-within:border-secondary-light',
  },
  error:{
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const currentType = ref(props.type === 'date' ? 'text' : props.type)
const handleFocus = () => {
  if (props.type === 'date') currentType.value = 'date'
}

const handleBlur = (e) => {
  if (props.type === 'date' && !e.target.value) currentType.value = 'text'
}
</script>

<template>
  <div :class="divClasses">
    <label
      class="text-[10px] bloc font-label tracking-widest text-outline mb-1 uppercase text-neutral"
      :for="id"
      >{{ label }}</label
    >
    <input
      :value="modelValue"
      :id="id"
      @input="emit('update:modelValue', $event.target.value)"
      :type="currentType"
      :placeholder="placeholder"
      @focus="handleFocus"
      @blur="handleBlur"
      :required="required"
      :class="inputClasses"
    />
  </div>
</template>
