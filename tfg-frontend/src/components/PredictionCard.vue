<script setup>
const props = defineProps({
  distance: [String, Number],
  time: Number,
  range: Array,
  version: String,
  previousTime: Number,
  avgPace: { type: Number, default: 370 }, // Ritmo de referencia para detectar ruido
})

const isReasonable = () => {
  const THRESHOLD = 1.5
  const predictedPace = props.time / parseFloat(props.distance)
  return predictedPace < props.avgPace * THRESHOLD
}

const formatTime = (s) => {
  if (!s) return '--:--'
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = Math.floor(s % 60)
  return h > 0
    ? `${h}:${m.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`
    : `${m}:${sec.toString().padStart(2, '0')}`
}

const isOptimized = () => props.time <= props.previousTime
</script>

<template>
  <div
    class="relative p-4 rounded-xl bg-neutral-back/60 border border-white/5 hover:border-secondary-light/40 transition-all mb-4 flex flex-col justify-between"
  >
    <div class="flex justify-between items-center mb-4">
      <span
        class="px-2 py-0.5 rounded bg-secondary-light/10 text-secondary-light text-[10px] font-bold uppercase tracking-widest"
      >
        {{ distance }} Forecast
      </span>
      <span class="text-[9px] text-neutral-500 font-label uppercase">
        {{ version?.split('_').pop() }}
      </span>
    </div>

    <div v-if="isReasonable()">
      <h3 class="text-3xl font-mono font-bold text-primary-too-dark tracking-tighter">
        {{ formatTime(time) }}
      </h3>
      <div class="mt-2">
        <span class="text-[9px] text-neutral uppercase font-bold block">Confidence Range</span>
        <span class="text-[11px] text-neutral-light/90 font-label -mt-2">
          {{ formatTime(range[0]) }} — {{ formatTime(range[1]) }}
        </span>
      </div>
    </div>

    <div v-else class="py-2">
      <h3 class="text-lg font-bold text-orange-500/80 italic">Inconsistent</h3>
      <p class="text-[9px] text-neutral-light/90 leading-tight">Out of logic bounds (p > 0.5).</p>
    </div>

    <!-- Footer -->
    <div class="mt-5 pt-3 border-t border-white/5 flex justify-between items-center w-full">
      <div class="flex flex-col">
        <span class="text-[9px] text-neutral-500 uppercase italic leading-none mb-1"
          >Model Trend</span
        >
        <span
          :class="isOptimized() ? 'text-emerald-400' : 'text-amber-400'"
          class="text-[10px] font-bold uppercase"
        >
          {{ isOptimized() ? 'Optimized' : 'Aerobic Gap' }}
        </span>
      </div>
      <div
        class="w-2 h-2 rounded-full"
        :class="
          isOptimized()
            ? 'bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.4)]'
            : 'bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.4)]'
        "
      ></div>
    </div>
  </div>
</template>
