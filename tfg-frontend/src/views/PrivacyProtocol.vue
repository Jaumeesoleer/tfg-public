<template>
  <main class="pt-24 min-h-[calc(100vh-130px)] bg-neutral-back">
    <div class="border-b border-white/5 pb-6 max-w-7xl w-auto mx-auto mt-10">
      <div class="mx-10">
        <h4 class="font-headline font-semibold text-4xl text-primary-too-dark">
          Control de Privacidad y Nodo GDPR
        </h4>
        <p class="text-sm text-neutral/70 mt-1">
          Gestión de derechos de información, anonimización biométrica y revocación de tokens.
        </p>
      </div>

      <div class="flex items-center gap-6 px-4 py-2 rounded-md h-fit text-xs font-label mx-10">
        <div class="flex items-center gap-2 bg-primary-light px-3 py-1">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-emerald-400 font-bold uppercase tracking-wider text-[10px]"
            >Cifrado Activo</span
          >
        </div>
        <div class="text-neutral bg-neutral-light/60 ml-6 px-3 py-1 font-label rounded-md">
          Última auditoría: <span class="text-white">15 de Mayo, 2026</span>
        </div>
      </div>
    </div>

    <div class="mt-8 max-w-7xl w-auto mx-auto">
      <div class="flex flex-wrap items-baseline justify-between pb-2 mb-4 mx-10">
        <h5
          class="font-headline font-semibold text-primary-too-dark text-xl flex items-center gap-2"
        >
          <span class="font-label text-secondary-semi-light/50 text-sm">01.</span> Estándares de
          Cifrado de Datos
        </h5>
        <span class="font-label text-[11px] text-neutral uppercase tracking-widest">
          Protocolo: <span class="text-secondary-semi-light/50 font-bold">AES-256-GCM</span>
        </span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 text-sm mx-10">
        <div class="space-y-1.5">
          <div class="flex items-center gap-2 font-label text-neutral uppercase font-semibold">
            <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
            Seguridad en Reposo (At-Rest)
          </div>
          <p class="text-neutral leading-relaxed font-body">
            Todos los vectores de características generados para el modelo de Machine Learning se
            almacenan encriptados en la base de datos. Los identificadores críticos de Strava y
            datos biométricos sensibles del perfil están aislados criptográficamente para evitar
            filtraciones en el almacenamiento persistente.
          </p>
        </div>

        <div class="space-y-1.5">
          <div class="flex items-center gap-2 font-label text-neutral uppercase font-semibold">
            <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
            Seguridad en Tránsito (In-Transit)
          </div>
          <p class="text-neutral leading-relaxed font-body">
            El flujo de streams y telemetría de carrera desde los servidores de Strava hacia la API
            de Flask se ejecuta bajo túneles TLS 1.3 estrictos. El intercambio de tokens OAuth 2.0 y
            credenciales JWT viaja firmado digitalmente, garantizando que ninguna entidad externa
            intercepte el rendimiento del atleta.
          </p>
        </div>
      </div>
    </div>
    <div class="mt-8 pt-6 max-w-7xl w-auto mx-auto">
      <div class="flex flex-wrap items-baseline justify-between pb-2 mb-4 mx-10">
        <h5
          class="font-headline font-semibold text-xl text-primary-too-dark flex items-center gap-2"
        >
          <span class="font-label text-secondary-semi-light/50 text-sm">02.</span> Tratamiento
          Algorítmico y Anonimización
        </h5>
        <span class="font-label text-[11px] text-neutral uppercase tracking-widest">
          Cumplimiento:
          <span class="text-secondary-semi-light/50 font-bold">RGPD / UE 2016/679</span>
        </span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 text-sm mx-10">
        <div class="space-y-1.5">
          <div class="flex items-center gap-2 font-label text-neutral uppercase font-semibold">
            <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
            Desacoplamiento Biométrico
          </div>
          <p class="text-neutral leading-relaxed font-body">
            Las variables fisiológicas del perfil del usuario (peso, edad y zonas de frecuencia
            cardíaca máxima) se transforman en coeficientes relativos normalizados antes de
            alimentar al optimizador del modelo. Este proceso disocia de forma irreversible tu
            identidad física del vector analítico de entrenamiento, garantizando que el motor de
            regresión solo procese patrones matemáticos abstractos.
          </p>
        </div>

        <div class="space-y-1.5">
          <div class="flex items-center gap-2 font-label text-neutral uppercase font-semibold">
            <span class="w-1.5 h-1.5 bg-neutral rounded-full"></span>
            Ofuscación de Telemetría GPS
          </div>
          <p class="text-neutral leading-relaxed font-body">
            El pipeline de ingesta de datos aplica un filtro de exclusión espacial sobre los flujos
            de coordenadas geográficas extraídos de las actividades. Se omiten de forma automática
            los perímetros iniciales y finales de los recorridos de carrera. Esto impide que el
            software almacene o reconstruya patrones cartográficos vinculados a ubicaciones
            residenciales o lugares de trabajo frecuentes.
          </p>
        </div>
      </div>
    </div>
  </main>
</template>
