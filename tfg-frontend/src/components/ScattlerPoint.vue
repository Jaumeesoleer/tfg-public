<template>
  <div class="h-full w-full">
    <Scatter :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Scatter } from 'vue-chartjs'
import { Chart as ChartJS, LinearScale, PointElement, Tooltip } from 'chart.js'

ChartJS.register(LinearScale, PointElement, Tooltip)

const props = defineProps({
  data: { type: Array, default: () => [] },
})

const chartData = computed(() => ({
  datasets: [
    {
      label: 'Eficiencia',
      data: props.data,
      backgroundColor: 'rgba(59, 130, 246, 0.6)', 
      pointRadius: 4,
      pointHoverRadius: 6,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      title: { display: true, text: 'Pulsaciones (BPM)' },
      beginAtZero: false,
    },
    y: {
      title: { display: true, text: 'Velocidad' },
      ticks: { display: false },
      beginAtZero: false,
    },
  },
  plugins: {
    tooltip: {
      callbacks: {
        label: (context) => {
          const p = context.raw
          return ` FC: ${p.x} bpm | Vel: ${p.formattedSpeed}`
        },
      },
    },
  },
}
</script>
