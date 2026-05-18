<script setup>
import { computed } from 'vue'
import { Chart } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  LinearScale,
  CategoryScale,
  ScatterController,
  LineController,
  Filler,
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  LinearScale,
  CategoryScale,
  ScatterController,
  LineController,
  Filler,
)

const props = defineProps({
  user_bests: Array,
  ml_points: Array,
  pred: Object,
})

// Normalizar datos
const normalizedPoints = computed(() => {
  if (!props.ml_points) return []

  return [...props.ml_points]
    .filter((p) => p?.confidence_range?.length === 2)
    .sort((a, b) => a.distance - b.distance)
    .map((p) => {
      const low = Math.min(p.confidence_range[0], p.confidence_range[1])
      const high = Math.max(p.confidence_range[0], p.confidence_range[1])

      return {
        x: p.distance,
        y: p.time,
        low,
        high,
      }
    })
})

const chartData = computed(() => {
  if (!props.user_bests || !normalizedPoints.value.length || !props.pred?.['5k']) {
    return { datasets: [] }
  }

  return {
    datasets: [
      // LÍMITE SUPERIOR
      {
        label: 'Límite superior',
        data: normalizedPoints.value.map((p) => ({
          x: p.x,
          y: p.high,
        })),
        borderColor: 'rgba(99, 102, 241, 0.3)',
        borderWidth: 1,
        pointRadius: 0,
        tension: 0.3,
        fill: false,
        type: 'line',
      },

      // LÍMITE INFERIOR + RELLENO
      {
        label: 'Margen de Error (95% CI)',
        data: normalizedPoints.value.map((p) => ({
          x: p.x,
          y: p.low,
        })),
        backgroundColor: 'rgba(99, 102, 241, 0.15)',
        borderColor: 'rgba(99, 102, 241, 0.3)',
        borderWidth: 1,
        pointRadius: 0,
        tension: 0.3,
        fill: '-1',
        type: 'line',
      },

      // PB
      {
        label: 'Récords Reales (PB)',
        data: props.user_bests.map((b) => ({
          x: b.distance,
          y: b.time,
        })),
        backgroundColor: '#34d399',
        pointRadius: 8,
        pointHoverRadius: 10,
        type: 'scatter',
      },

      // ML
      {
        label: 'Predicción ML Actual',
        data: normalizedPoints.value.map((p) => ({
          x: p.x,
          y: p.y,
        })),
        backgroundColor: '#6366f1',
        pointStyle: 'rectRot',
        pointRadius: 7,
        type: 'scatter',
      },

      // HISTÓRICO
      {
        label: 'Último Log Guardado',
        data: [
          { x: 5, y: props.pred['5k'] },
          { x: 10, y: props.pred['10k'] },
          { x: 21.1, y: props.pred['21k'] },
          { x: 42.2, y: props.pred['42k'] },
        ],
        borderColor: 'rgba(255, 255, 255, 0.2)', 
        borderWidth: 2,
        borderDash: [6, 4],
        showLine: true,
        fill: false,
        pointRadius: 0,
        tension: 0.1,
        type: 'line',
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    filler: {
      propagate: false,
    },
    legend: {
      position: 'bottom',
      labels: {
        color: '#9ca3af',
        usePointStyle: true,
        padding: 15,
        filter: (item) => item.text !== 'Límite superior',
      },
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const val = context.parsed.y
          if (val == null) return ''

          const m = Math.floor(val / 60)
          const s = Math.floor(val % 60)
          return `${context.dataset.label}: ${m}:${s.toString().padStart(2, '0')}`
        },
      },
    },
  },
  scales: {
    x: {
      type: 'linear',
      title: {
        display: true,
        text: 'Distancia (km)',
        color: '#6b7280',
      },
      grid: { color: 'rgba(255,255,255,0.05)' },
      ticks: { color: '#9ca3af' },
    },
    y: {
      beginAtZero: false,
      title: {
        display: true,
        text: 'Tiempo Estimado',
        color: '#6b7280',
      },
      grid: { color: 'rgba(255,255,255,0.05)' },
      ticks: {
        color: '#9ca3af',
        callback: (value) => Math.floor(value / 60) + ' min',
      },
    },
  },
}
</script>

<template>
  <div class="w-full h-120 p-4 bg-neutral-back/60 rounded-2xl border border-white/5">
    <Chart v-if="chartData.datasets.length" type="line" :data="chartData" :options="chartOptions" />
  </div>
</template>
