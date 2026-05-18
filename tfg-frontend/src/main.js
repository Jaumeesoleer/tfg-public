// ==============================================================================
// PUNTO DE ENTRADA UNIFICADO, ORQUESTADOR Y ARRANQUE DE LA SPA (ENTRY POINT)
// TFG: Análisis y predicción del rendimiento en corredores
// Autor: Jaume Antoni Soler Sánchez
// ==============================================================================

import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Tooltip from 'primevue/tooltip'

import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue)
app.directive('tooltip', Tooltip)

app.mount('#app')
