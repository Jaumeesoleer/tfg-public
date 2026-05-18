<script setup>
import Neural from '@/assets/svg/Neural.vue'
import History from '@/assets/svg/History.vue'
import Cloud from '@/assets/svg/Cloud.vue'
import Light from '@/assets/svg/Light.vue'

const props = defineProps({
  svg: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    required: true,
  },
  text: {
    type: String,
    required: true,
  },
  bgColor: {
    type: String,
    default: 'bg-primary-ultra',
  },
  titleColor: {
    type: String,
    default: 'text-white',
  },
  textColor: {
    type: String,
    default: 'text-primary-light/60',
  },
  tips: {
    type: Boolean,
    default: false,
  },
  padding: {
    type: String,
    default: 'p-8',
  },
  html: {
    type: Boolean,
    default: false,
  },
  titleClass: {
    type: String,
    default: 'font-serif text-2xl mt-4 mb-2',
  },
  hr: {
    type: Number
  },
  eff:{
    type:Number
  }
})

const svgs = {
  Neural,
  History,
  Cloud,
  Light,
}
</script>

<template>
  <div
    :class="[bgColor, textColor, padding, svg === 'Light' ? 'flex  gap-2' : '']"
    class="flex-1 rounded-xl relative overflow-hidden group"
  >
    <component v-if="svg" :is="svgs[svg]" :class="svg === 'Light' ? '' : 'mb-4'" />
    <div class="">
      <h4 :class="[titleColor, titleClass]" class="">{{ title }}</h4>
      <p class="text-xs leading-relaxed" v-if="!html">
        {{ text }}
      </p>
      <div class="text-xs leading-relaxed" v-if="html" v-html="text"></div>
    </div>
    <img
      v-if="svg == 'Neural'"
      src="@/assets/Neural.png"
      class="absolute bottom-0 right-0 w-24 h-24 opacity-20 grayscale group-hover:grayscale-0 transition-all duration-500"
      alt=""
    />

    <div class="flex gap-10 mt-6" v-if="tips === true">
      <div class="">
        <p class="text-[10px] uppercase text-neutral-light font-bold font-label tracking-wide">
          Tendencia de frecuencia cardíaca media
        </p>
        <p class="text-xl font-headline font-bold text-secondary-light">
          {{ props.hr }} <span class="uppercase">bpm</span>
        </p>
      </div>
      <div class="text-[10px] uppercase text-neutral-light font-bold font-label tracking-wide">
        <p class="">Índice de eficiencia</p>
        <p class="text-xl font-headline font-bold text-secondary-light">{{props.eff *100}}%</p>
      </div>
    </div>
  </div>
</template>
