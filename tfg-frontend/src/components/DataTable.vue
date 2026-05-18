<script setup>
const props = defineProps({
  zones: { type: Array, required: true },
})
const emit = defineEmits(['update:zones'])

const updateZone = (index, newValue) => {
  const newMin = parseInt(newValue) || 0
  const newZones = [...props.zones]

  // Actualizamos el mínimo de la zona actual
  newZones[index] = { ...newZones[index], min: newMin }

  // Si no es la primera zona, el máximo de la anterior debe ser el mínimo de esta
  if (index > 0) {
    newZones[index - 1] = { ...newZones[index - 1], max: newMin }
  }

  // Si no es la última zona, el máximo de esta debe ser el mínimo de la siguiente
  if (index < newZones.length - 1) {
    newZones[index] = { ...newZones[index], max: newZones[index + 1].min }
  }

  emit('update:zones', newZones)
}

const values = {
  1: [
    'text-sky-600',
    'bg-sky-100',
    'Recuperación (Z1)',
    'Restauración activa',
    '50-60%',
    'bg-sky-600',
  ],
  2: [
    'text-green-600',
    'bg-green-100',
    'Aeróbica (Z2)',
    'Base de resistencia',
    '60-70%',
    'bg-green-600',
  ],
  3: [
    'text-yellow-600',
    'bg-yellow-100',
    'Tempo (Z3)',
    'Eficiencia de lactato',
    '70-80%',
    'bg-yellow-600',
  ],
  4: [
    'text-orange-600',
    'bg-orange-100',
    'Umbral (Z4)',
    'Esfuerzo sub-máximo',
    '80-90%',
    'bg-orange-600',
  ],
  5: ['text-red-600', 'bg-red-100', 'Anaeróbica (Z5)', 'Esfuerzo máximo', '90-100%', 'bg-red-600'],
}
</script>

<template>
  <tr
    v-for="(value, key) in zones"
    :key="key"
    class="grid grid-cols-4 bg-neutral-back/60 font-body items-center px-10 py-7 text-center"
  >
    <td class="flex gap-2">
      <div class="w-2 my-2 rounded-full" :class="values[key + 1][5]"></div>
      <div class="text-left">
        <p class="font-sembold">{{ values[key + 1][2] }}</p>
        <p class="text-xs mt-1 text-neutral">{{ values[key + 1][3] }}</p>
      </div>
    </td>
    <td
      class="text-xs w-fit m-auto rounded-md font-semibold p-1"
      :class="[values[key + 1][0], values[key + 1][1]]"
    >
      {{ values[key + 1][4] }}
    </td>
    <!-- Mostramos el rango actualizado -->
    <td class="text-lg tracking-wide">{{ value.min }} - {{ value.max }}</td>
    <td class="flex">
      <div class="w-2/5 lg:w-3/5"></div>
      <input
        type="number"
        class="text-right w-3/5 lg:w-2/5 bg-neutral-light/20 font-label px-1"
        placeholder="Min"
        :value="value.min"
        @input="updateZone(key, $event.target.value)"
      />
    </td>
  </tr>
</template>
