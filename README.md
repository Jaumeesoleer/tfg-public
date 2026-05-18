# The Architect: Arquitectura del Rendimiento

Plataforma web integral diseñada para la optimización, análisis exploratorio y modelado predictivo del rendimiento de corredores de fondo. La herramienta centraliza la ingesta de telemetría deportiva de sensores GPS para transformar datos históricos en ventajas estratégicas de planificación.

## 🚀 Características Clave

- **Ingesta Dinámica de Datos**: Mecanismos de carga masiva drag & drop para archivos estructurados de entrenamiento (formatos CSV con esquemas compatibles con Strava), incluyendo validación automática de esquemas algebraicos.
- **Procesamiento y Pipeline de Limpieza**: Filtrado analítico y tratamiento automático de outliers fisiológicos y anomalías de GPS mediante Pandas (ej. descarte de velocidades irreales o paradas).
- **Panel de Control Analítico (Dashboard)**: Interfaz responsiva enfocada en la telemetría del atleta. Incluye gráficas avanzadas de líneas duales con doble eje Y invertido para superponer ritmo y frecuencia cardíaca sobre la distancia.
- **Distribución de Carga Fisiológica**: Segmentación automática del tiempo de entrenamiento en zonas de intensidad cardíaca (Z1-Z5) calculadas de forma personalizada o mediante el método de Karvonen (frecuencia cardíaca de reserva).
- **Motor de Machine Learning Personalizado**: Arquitectura basada en un modelo supervisado `MultiOutputRegressor` que encapsula un `Random Forest Regressor` de Scikit-learn para estimar marcas simultáneas en distancias estándar (5K, 10K, Media Maratón y Maratón).
- **Simulador Interactivos "What-If"**: Módulo predictivo reactivo que permite ajustar factores de fatiga acumulada y simular penalizaciones de ritmo por temperatura ambiente (ej. penalización progresiva del 0.8% por grado adicional a partir de los 20°C).
- **Seguridad de Nivel Profesional**: Autenticación e inicio de sesión seguros mediante el uso de cookies JWT con la propiedad `HttpOnly` (inmunes a ataques XSS) y validación cruzada de headers contra ataques CSRF.

## 🛠️ Stack Tecnológico

### Capa de Presentación (Frontend)

- **Framework**: Vue 3 (Composition API) & Vite.
- **Estilos**: Tailwind CSS (Estructura de diseño modular _utility-first_).
- **Estado Global**: Pinia (Stores reactivos y persistencia en caché local).
- **Gráficas**: Chart.js + wrappers reactivos `vue-chartjs`.
- **Cliente HTTP**: Axios (Interceptor automatizado para renovación silenciosa de tokens expirados en flujo _Retry_).

### Capa de Negocio (Backend)

- **Framework**: Python 3.11 & Flask (Organizado mediante Blueprints bajo el patrón _Application Factory_).
- **Manipulación de Datos**: Pandas & NumPy.
- **Modelado Predictivo**: Scikit-learn (Imputación con `SimpleImputer` y algoritmos de ensamblado).
- **Mapeo Relacional**: SQLAlchemy (Patrón _Repository_ implementado en `db_utils.py` para desacoplar consultas de la lógica de negocio).
- **Notificaciones**: Resend SDK para el despacho automatizado de tickets de soporte técnico.

### Capa de Datos (Persistencia) y Despliegue

- **Base de Datos**: PostgreSQL 15 (Variante Alpine optimizada para almacenamiento masivo de series temporales de telemetría punto por segundo).
- **Contenerización**: Docker y Docker Compose para garantizar un entorno idéntico, reproducible y aislado.

---

## 📂 Estructura del Proyecto

```text
the-architect/
├── frontend/             # Single Page Application (Vue 3)
│   ├── src/
│   │   ├── api/          # Cliente Axios centralizado e interceptores
│   │   ├── components/   # Componentes reutilizables de Chart.js
│   │   ├── stores/       # Estados globales de Pinia (User, Activity, Prediction)
│   │   └── views/        # Vistas de la aplicación (Dashboard, Predictor, Profile)
│   └── Dockerfile
├── backend/              # API REST (Flask)
│   ├── artifacts/        # Almacenamiento del modelo serializado (.pkl)
│   ├── logic/            # Scripts standalone de entrenamiento del modelo (tfg_trainer.py)
│   ├── models/           # Modelos ORM de SQLAlchemy (User, Activity, ActivityStream, etc.)
│   ├── routes/           # Blueprints de endpoints lógicos organizados por dominios
│   ├── services/         # Servicios de cálculo de métricas y lógica analítica dura
│   ├── utils/            # Parsers transversales de telemetría
│   └── Dockerfile
└── docker-compose.yml    # Orquestación de servicios (frontend, backend, db, adminer)
```

## 💻 Instalación y Ejecución Local

Gracias a la contenerización del proyecto con **Docker**, no es necesario que dispongas de Python, Node.js ni PostgreSQL instalados de manera nativa en tu máquina anfitriona.

### 📋 Requisitos Previos
* **Git** instalado en el sistema.
* **Docker Desktop** activo (Windows/Mac) o **Docker Engine** + el plugin de **Docker Compose** (Linux).

### ⚙️ Pasos para Inicializar el Entorno

**1. Clonar el repositorio de GitHub**

```text
git clone git@github.com:Jaumeesoleer/tfg-running-analysis.git
cd tfg-running-analysis
```
**2. Configurar las variables de entorno**

Crea un archivo llamado `.env` en la raíz del proyecto (junto a `docker-compose.yml`) y define la siguiente plantilla de configuración técnica:

# Configuración Base de Datos
```text
POSTGRES_USER=new_user
POSTGRES_PASSWORD=new_password
POSTGRES_DB=tfg_running
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
```

# Configuración Seguridad Flask
```text
SECRET_KEY=secret_key
JWT_SECRET_KEY=secret_key
DEBUG=True
FLASK_APP="app.py"
```
# Credenciales de Evaluación Automatizada (Demo)
```text
DEMO_USER_USERNAME="jaumeesoleer"
DEMO_USER_PASSWORD="12345678a"
```
# Integración Correo (Soporte)
```text
PERSONAL_EMAIL="email@mail.com"
RESEND_API_KEY=resend_api_key
```

# Orígenes Cruzados (CORS)
```text
FRONTEND_URL=http://localhost:5173
VITE_API_URL=http://localhost:5000
```

**3. Compilar y levantar los contenedores**

Ejecuta el siguiente comando para orquestar la descarga de imágenes base ligeras (`alpine`/`slim`), instalar las dependencias aisladas de Node/Python y arrancar el stack completo de servicios:
```text
docker compose up --build
```
