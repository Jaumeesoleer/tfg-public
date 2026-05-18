<script setup>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  values: { type: Array },
  zones: { type: Array },
})

const graph = ref(null)
// Extracción local de los vectores informacionales recibidos en el payload
const value = props?.values
const yellow = props.zones[4]['min']
const green = props.zones[1]['max']

onMounted(() => {
  new Chart(graph.value, {
    type: 'bar',
    data: {
      labels: value.map(() => ''),
      datasets: [
        {
          data: value,
          // --- PIPELINE DE MAPEO CROMÁTICO SEMAFÓRICO ADAPTATIVO (COLORIMETRÍA BIOMÉTRICA) ---
          backgroundColor: value.map((v) => {
            if (v <= green) return '#2ecc71'
            if (v >= green && v < yellow) return '#f1c40f'
            return '#e74c3c' // Rojo
          }),
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true },
      },
      scales: {
        x: { display: false },
        y: {
          display: false,
          beginAtZero: true,
        },
      },
    },
  })
})
</script>

<template>
  <div class="w-full">
    <canvas ref="graph"></canvas>
  </div>
</template>

