<template>
  <main class="pt-24 min-h-[calc(100vh-130px)] bg-neutral-back">
    <div class="border-b border-white/5 pb-6 max-w-7xl w-auto mx-auto mt-10">
      <div class="mx-10">
        <h4 class="font-headline font-semibold text-4xl text-primary-too-dark">
          Licencia del Modelo y Cuotas de Cómputo
        </h4>
        <p class="text-sm text-neutral/70 mt-1">
          Términos de uso del motor algorítmico, límites de peticiones a la API de Machine Learning
          y descargo de responsabilidad.
        </p>
      </div>

      <div class="flex items-center gap-6 px-4 py-2 rounded-md h-fit text-xs font-label mx-10">
        <div class="flex items-center gap-2 bg-primary-light px-3 py-1">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-emerald-400 font-bold uppercase tracking-wider text-[10px]"
            >Licencia Académica Active</span
          >
        </div>
        <div class="text-neutral bg-neutral-light/60 ml-6 px-3 py-1 font-label rounded-md">
          Núcleo del motor: <span class="text-white">Open-Source (MIT)</span>
        </div>
      </div>
    </div>

    <div class="mt-8 max-w-7xl w-auto mx-auto">
      <div class="flex flex-wrap items-baseline justify-between pb-2 mb-4 mx-10">
        <h5
          class="font-headline font-semibold text-primary-too-dark text-xl flex items-center gap-2"
        >
          <span class="font-label text-secondary-semi-light/50 text-sm">01.</span> Régimen de
          Licencia Core
        </h5>
        <span class="font-label text-[11px] text-neutral uppercase tracking-widest">
          Distribución: <span class="text-secondary-semi-light/50 font-bold">Uso No Comercial</span>
        </span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 text-sm mx-10">
        <div class="space-y-1.5">
          <div class="flex items-center gap-2 font-label text-neutral uppercase font-semibold">
            <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
            Código Abierto e Integridad
          </div>
          <p class="text-neutral leading-relaxed font-body">
            El pipeline matemático y los optimizadores basados en modelos matemáticos lineales se
            distribuyen bajo la licencia estándar MIT. Los desarrolladores e investigadores pueden
            auditar, clonar y proponer modificaciones al pipeline de ingeniería, manteniendo el
            carácter transparente del algoritmo predictivo.
          </p>
        </div>

        <div class="space-y-1.5">
          <div class="flex items-center gap-2 font-label text-neutral uppercase font-semibold">
            <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
            Restricciones de Explotación
          </div>
          <p class="text-neutral leading-relaxed font-body">
            Queda estrictamente prohibida la explotación comercial directa de los pesos entrenados
            de este modelo o de su API sin consentimiento explícito. Los datos generados se reservan
            para fines de evaluación del rendimiento deportivo en el ámbito privado o de
            investigación académica universitaria.
          </p>
        </div>
      </div>
    </div>

    <div class="mt-8 pt-6 max-w-7xl w-auto mx-auto">
      <div class="flex flex-wrap items-baseline justify-between pb-2 mb-4 mx-10">
        <h5
          class="font-headline font-semibold text-xl text-primary-too-dark flex items-center gap-2"
        >
          <span class="font-label text-secondary-semi-light/50 text-sm">02.</span> Cuotas e
          Infraestructura del Servidor
        </h5>
        <span class="font-label text-[11px] text-neutral uppercase tracking-widest">
          Cuota mensual:
          <span class="text-secondary-semi-light/50 font-bold">14 / 100 Consultas</span>
        </span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 text-sm mx-10">
        <div class="space-y-1.5">
          <div class="flex items-center gap-2 font-label text-neutral uppercase font-semibold">
            <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
            Restricción de Rate-Limiting Local
          </div>
          <p class="text-neutral leading-relaxed font-body">
            Para salvaguardar la disponibilidad del backend local desarrollado en Flask y evitar
            desbordamientos de memoria, cada perfil dispone de una cuota máxima de 100 operaciones
            de simulación dinámica al mes. Las peticiones excedentes se mitigan en el controlador
            devolviendo un código HTTP 429.
          </p>
        </div>

        <div class="space-y-1.5">
          <div class="flex items-center gap-2 font-label text-neutral uppercase font-semibold">
            <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
            Costes de Entrenamiento en Memoria
          </div>
          <p class="text-neutral leading-relaxed font-body">
            La agregación de actividades de los dataframes y la imputación de valores nulos mediante
            Scikit-Learn suponen un coste de CPU crítico para el microservicio. El sistema optimiza
            estos recursos almacenando en caché el último estado calculado en la tabla
            `PredictionLog` hasta que el usuario solicite un nuevo recalculo explícito.
          </p>
        </div>
      </div>
    </div>

    <div class="mt-8 pt-6 max-w-7xl w-auto mx-auto border-t border-white/5">
      <div class="flex flex-wrap items-baseline justify-between pb-2 mb-4 mx-10">
        <h5
          class="font-headline font-semibold text-xl text-primary-too-dark flex items-center gap-2"
        >
          <span class="font-label text-secondary-semi-light/50 text-sm">03.</span> Exención de
          Responsabilidad Fisiológica
        </h5>
        <span class="font-label text-[11px] text-amber-500 uppercase tracking-widest font-bold">
          Atención / Disclaimer
        </span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 text-sm mx-10">
        <div class="space-y-1.5">
          <div class="flex items-center gap-2 font-label text-neutral uppercase font-semibold">
            <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
            Naturaleza Estadística Algorítmica
          </div>
          <p class="text-neutral leading-relaxed font-body">
            Los umbrales temporales estimados para distancias de fondo (5k, 10k, media y maratón)
            son aproximaciones puramente estadísticas basadas en tendencias históricas del atleta.
            El modelo asume condiciones ambientales ideales y una mecánica de carrera eficiente; no
            contempla bajones imprevistos de rendimiento.
          </p>
        </div>

        <div class="space-y-1.5">
          <div class="flex items-center gap-2 font-label text-neutral uppercase font-semibold">
            <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
            Supervisión Facultativa Obligatoria
          </div>
          <p class="text-neutral leading-relaxed font-body">
            Esta plataforma web es una herramienta de software analítico para simulación y no
            constituye un plan de entrenamiento médico ni un sustituto de una prueba de esfuerzo
            cardiovascular realizada en un entorno clínico. Cualquier incremento drástico en las
            cargas simuladas debe ser supervisado por profesionales certificados.
          </p>
        </div>
      </div>
    </div>
  </main>
</template>
