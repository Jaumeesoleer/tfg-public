<template>
  <div class="w-full h-150 relative">
    <Line v-if="isDataReady" :data="chartData" :options="chartOptions" />
    <div v-else class="placeholder">Esperando datos de actividad...</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale,
  Filler,
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale,
  Filler,
)

// 1. DEFINICIÓN DE PROPS
const props = defineProps({
  timestamps: { type: Array, required: true }, 
  speedsRaw: { type: Array, required: true }, 
  distancesRaw: { type: Array, required: true }, 
  heartrates: { type: Array, default: () => [] }, 
})

// 2. UTILIDADES DE CONVERSIÓN
const toPaceDecimal = (ms) => {
  if (!ms || ms <= 0.8) return null // Filtro para paradas (menos de 3km/h)
  const pace = 16.6667 / ms
  return pace > 12 ? null : pace // Filtro: ritmos más lentos de 12:00 min/km son ruido
}

const formatPace = (decimal) => {
  if (!decimal) return '00:00'
  const mins = Math.floor(decimal)
  const secs = Math.round((decimal - mins) * 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 3. PROPIEDAD COMPUTADA PARA EL GRÁFICO
const isDataReady = computed(() => props.distancesRaw.length > 0)

const chartData = computed(() => ({
  // Eje X: Convertimos metros a Kilómetros con 2 decimales
  labels: props.distancesRaw.map((d) => (d / 1000).toFixed(2)),
  datasets: [
    {
      label: 'Ritmo',
      data: props.speedsRaw.map((s) => toPaceDecimal(s)),
      borderColor: '#5355aa',
      borderWidth: 1.5,
      backgroundColor: 'transparent',
      yAxisID: 'yPace',
      tension: 0.1,
      pointRadius: 0,
      spanGaps: true,
    },
    {
      label: 'Pulso',
      data: props.heartrates,
      borderColor: '#852221',
      borderWidth: 1.5,
      backgroundColor: '#85222120',
      fill: true,
      yAxisID: 'yHR',
      tension: 0.1,
      pointRadius: 0,
    },
  ],
}))

// 4. CONFIGURACIÓN DEL GRÁFICO
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  resizeDelay: 50,
  interaction: { mode: 'index', intersect: false },
  scales: {
    x: {
      title: { display: true, text: 'Distancia (km)' },
      ticks: { maxTicksLimit: 8 },
    },
    yHR: {
      type: 'linear',
      position: 'left',
      title: { display: true, text: 'BPM' },
      suggestedMin: 120,
    },
    yPace: {
      type: 'linear',
      position: 'right',
      reverse: true, // Rápido arriba, lento abajo
      title: { display: true, text: 'Ritmo (min/km)' },
      grid: { drawOnChartArea: false },
      ticks: {
        callback: (value) => formatPace(value),
      },
    },
  },
  plugins: {
    tooltip: {
      callbacks: {
        label: (context) => {
          const val = context.parsed.y
          return context.dataset.yAxisID === 'yPace'
            ? `Ritmo: ${formatPace(val)} min/km`
            : `Pulso: ${val} bpm`
        },
      },
    },
  },
}
</script>
