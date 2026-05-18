<template>
  <div class="h-full w-full">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

const props = defineProps({
  data: { type: Array, default: () => [] }, 
  middleValue: { type: Number, default: 0 },
})

console.log(props.data)
const chartData = computed(() => ({
  labels: props.data.map((_, i) => i),
  datasets: [
    {
      label: 'Velocidad',
      data: props.data.map((d) => d[0]),
      borderColor: '#3B82F6',
      borderWidth: 2,
      pointRadius: 0,
      tension: 0.3,
      zIndex: 2, 
    },
    {
      label: 'Referencia',
      // Creamos una línea recta con el valor medio
      data: props.data.map(() => props.middleValue),
      borderColor: 'rgba(156, 163, 175, 0.5)',
      borderWidth: 1,
      borderDash: [5, 5], 
      pointRadius: 0,
      fill: false,
      zIndex: 1,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        // Solo mostramos el tooltip para el primer dataset (la velocidad real)
        label: (context) => {
          if (context.datasetIndex !== 0) return null
          const index = context.dataIndex
          const item = props.data[index]
          return ` Velocidad: ${item[1]}`
        },
      },
    },
  },
  scales: {
    x: { display: false },
    y: {
      beginAtZero: false,
      grid: {
        drawTicks: false,
      },
    },
  },
  // Evita que el tooltip aparezca para la línea de referencia
  interaction: {
    mode: 'index',
    intersect: false,
  },
}
</script>
