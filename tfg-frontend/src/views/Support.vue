<script setup>
import { useSupportStore } from '@/stores/support'
import { ref, computed } from 'vue'

const name = ref('')
const email = ref('')
const subject = ref('')
const content = ref('')

const supportStore = useSupportStore()

const handleSubmitTicket = async () => {
  try{
    
    await supportStore.ticket({
      name: name.value,
      email: email.value,
      subject: subject.value,
      content: content.value,
    })
    // Aquí irá la lógica para enviar el JSON a la API pública de Flask
    alert('¡Ticket transmitido con éxito al nodo de soporte!')
  }catch (error){
    console.log(error)
  }
}
</script>
<template>
  <main class="pt-24 min-h-[calc(100vh-130px)] bg-neutral-back">
    <div class="pb-6 max-w-7xl w-auto mx-auto my-10">
      <div class="mx-10">
        <h4 class="font-headline font-semibold text-4xl text-primary-too-dark">Support Terminal</h4>
        <p class="text-sm text-neutral/70 mt-1">
          ¿Tienes dudas con el motor predictivo o has detectado una anomalía? Despacha un ticket
          directo a nuestro equipo de desarrollo.
        </p>
      </div>

      <div class="flex items-center gap-6 px-4 py-2 rounded-md h-fit text-xs font-label mx-10">
        <div class="flex items-center gap-2 bg-primary-light px-3 py-1">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-emerald-400 font-bold uppercase tracking-wider text-[10px]"
            >Terminal de Guardia Online</span
          >
        </div>
        <div class="text-neutral bg-neutral-light/60 ml-6 px-3 py-1 font-label rounded-md">
          Tiempo medio de respuesta <span class="text-white font-mono"> &lt; 24 Horas</span>
        </div>
      </div>
    </div>

    <div class="mt-8 max-w-7xl w-auto mx-auto mb-16">
      <div class="flex flex-wrap items-baseline justify-between pb-2 mb-6 mx-10">
        <h5
          class="font-headline font-semibold text-primary-too-dark text-xl flex items-center gap-2"
        >
          <span class="font-label text-secondary-semi-light/50 text-sm">01.</span> Apertura de
          Incidencia Global
        </h5>
        <span class="font-label text-[11px] text-neutral uppercase tracking-widest">
          Acceso: <span class="text-secondary-semi-light/50 font-bold">Público / Abierto</span>
        </span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 text-sm mx-10">
        <div class="lg:col-span-5 space-y-6">
          <div class="space-y-2">
            <div
              class="flex items-center gap-2 font-label text-neutral uppercase font-semibold text-xs tracking-wider"
            >
              <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
              Soporte Técnico de Extremo a Extremo
            </div>
            <p class="text-neutral leading-relaxed font-body">
              No necesitas disponer de una cuenta activa en la plataforma para reportar un problema.
              Si estás experimentando dificultades para sincronizar tus actividades, anomalías en
              las gráficas de dispersión o errores de respuesta en las peticiones locales, detalla
              los pasos para que podamos reproducir el comportamiento en nuestro entorno de
              desarrollo.
            </p>
          </div>

          <div class="space-y-2">
            <div
              class="flex items-center gap-2 font-label text-neutral uppercase font-semibold text-xs tracking-wider"
            >
              <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
              Buenas Prácticas para el Reporte
            </div>
            <p class="text-neutral leading-relaxed font-body text-xs">
              Para acelerar el diagnóstico, si eres desarrollador o estás auditando el TFG en local,
              se recomienda especificar en el cuerpo del mensaje la versión del navegador utilizado
              y el código de estado HTTP devuelto por la consola de desarrollador (F12) al disparar
              la petición.
            </p>
          </div>
        </div>

        <!-- Columna Derecha (Ancho: 7 de 12): El Formulario Interactivo -->
        <div class="lg:col-span-7 bg-neutral-light/20 p-8 rounded-md border border-white/5">
          <form @submit.prevent="handleSubmitTicket" class="space-y-5">
            <!-- Fila doble: Nombre y Email -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-1.5">
                <label
                  for="ticket-name"
                  class="font-label text-xs uppercase text-neutral/80 font-semibold"
                  >Tu Nombre</label
                >
                <input
                  id="ticket-name"
                  type="text"
                  v-model="name"
                  required
                  placeholder="Ej. Joan Doe"
                  class="w-full bg-neutral-back border border-white/10 rounded px-4 py-2 text-primary-too-dark placeholder-neutral/30 outline-none focus:border-indigo-500 text-sm transition-all"
                />
              </div>
              <div class="space-y-1.5">
                <label
                  for="ticket-email"
                  class="font-label text-xs uppercase text-neutral/80 font-semibold"
                  >Correo Electrónico</label
                >
                <input
                  id="ticket-email"
                  type="email"
                  v-model="email"
                  required
                  placeholder="tu@email.com"
                  class="w-full bg-neutral-back border border-white/10 rounded px-4 py-2 text-primary-too-dark placeholder-neutral/30 outline-none focus:border-indigo-500 text-sm transition-all"
                />
              </div>
            </div>

            <!-- Campo: Asunto del Ticket -->
            <div class="space-y-1.5">
              <label
                for="ticket-subject"
                class="font-label text-xs uppercase text-neutral/80 font-semibold"
                >Asunto de la Consulta</label
              >
              <input
                id="ticket-subject"
                type="text"
                v-model="subject"
                required
                placeholder="Breve título de la incidencia"
                class="w-full bg-neutral-back border border-white/10 rounded px-4 py-2 text-primary-too-dark placeholder-neutral/30 outline-none focus:border-indigo-500 text-sm transition-all"
              />
            </div>

            <!-- Campo: Mensaje / Detalles técnicos -->
            <div class="space-y-1.5">
              <label
                for="ticket-message"
                class="font-label text-xs uppercase text-neutral/80 font-semibold"
                >Descripción del Problema</label
              >
              <textarea
                id="ticket-message"
                rows="5"
                required
                v-model="content"
                placeholder="Describe con el mayor detalle posible qué ha ocurrido..."
                class="w-full bg-neutral-back border border-white/10 rounded px-4 py-3 text-primary-too-dark placeholder-neutral/30 outline-none focus:border-indigo-500 text-sm transition-all resize-none"
              ></textarea>
            </div>

            <!-- Botón Despachador -->
            <div class="pt-2">
              <button
                type="submit"
                class="w-full bg-secondary-light hover:bg-secondary-light/70 text-white font-label py-2.5 rounded font-semibold text-sm transition-all tracking-wide uppercase shadow-lg shadow-secondary-light/10 cursor-pointer"
              >
                Transmitir Ticket de Soporte
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>
