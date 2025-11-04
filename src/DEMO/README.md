# 🎮 Gamify Achievement System - Demo App

## 📋 Descripción

Aplicación Flask de demostración para el sistema de logros de Gamify. Permite visualizar y testear el flujo completo de desbloqueo de logros mediante una interfaz web simple y moderna.

## 🚀 Instrucciones de Ejecución

### Paso 1: Preparar el Backend Django

Asegúrate de que el servidor Django esté corriendo:

```bash
# En una terminal, desde el directorio raíz del proyecto
cd src
uv run python manage.py runserver
```

El servidor debe estar disponible en: `http://localhost:8000`

### Paso 2: Crear Datos de Prueba (si no lo has hecho)

```bash
# Desde el directorio src/
# Crear logros de ejemplo
uv run python manage.py create_sample_achievements

# Crear estadísticas para el superusuario (ID=1)
uv run python manage.py create_test_user_stats --user-id 1
```

### Paso 3: Ejecutar la Demo Flask

```bash
# En otra terminal, desde el directorio src/DEMO/
cd DEMO
uv run python demo_app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 🎯 Funcionalidades de la Demo

### 1. **Panel de Estadísticas en Tiempo Real**
- **Tareas Completadas**: Total acumulado de tareas realizadas
- **Racha Actual**: Días consecutivos de actividad
- **Nivel**: Nivel actual del usuario (calculado desde XP)
- **XP Total**: Experiencia total acumulada
- **Logros Desbloqueados**: Cantidad de logros completados

### 2. **Simulación de Tareas (¡NUEVO!)**
- Simula 1 a 100 tareas simultáneamente
- Actualiza automáticamente todas las estadísticas:
  - Incrementa contador de tareas completadas
  - Actualiza racha consecutiva
  - Calcula y actualiza nivel basado en XP
  - Acumula XP (50 XP por tarea)
- **Evaluación automática de logros**:
  - Verifica criterios de todos los logros
  - Desbloquea automáticamente los que cumplan requisitos
  - Muestra notificaciones con los logros desbloqueados
- **Feedback visual instantáneo**:
  - Notificaciones toast con detalles de la simulación
  - Alertas especiales cuando se desbloquean logros
  - Actualización automática de la interfaz

### 3. **Visualización de Logros**
- Ver todos los logros disponibles con información detallada
- **Filtros interactivos**:
  - Todos: Muestra todos los logros
  - Desbloqueados: Solo logros completados
  - Bloqueados: Solo logros pendientes
- **Barra de progreso para cada logro**:
  - Muestra progreso actual vs. requerido
  - Porcentaje visual de completitud
  - Actualización en tiempo real
- **Badges de rareza**: Common, Rare, Epic, Legendary
- **Recompensas visibles**: XP y monedas por cada logro
- **Fecha de desbloqueo** para logros completados

### 4. **Desbloqueo Manual**
- Botón para desbloquear logros manualmente (útil para testing)
- Confirmación antes de desbloquear
- Actualización inmediata de estadísticas

### 5. **Sistema de Notificaciones**
- Notificaciones toast elegantes
- Colores según tipo: success, info, warning, danger
- Auto-cierre después de 3 segundos
- Múltiples notificaciones simultáneas

## 🎨 Características de la Interfaz

- ✅ **Diseño Responsive**: Funciona en desktop y móvil
- ✅ **Animaciones**: Transiciones suaves al hacer hover
- ✅ **Notificaciones Toast**: Feedback visual de todas las acciones
- ✅ **Colores por Rareza**: Identificación visual rápida
- ✅ **Progress Bars**: Seguimiento del progreso de cada logro
- ✅ **Bootstrap 5**: UI moderna y profesional

## 📊 Flujo de Demostración Recomendado

### Escenario 1: Desbloqueo por Tareas Completadas ⭐

1. **Inicio**: Abre la demo en `http://localhost:5000`
2. **Estado inicial**: Observa que tienes 0 tareas completadas y 0 logros desbloqueados
3. **Primera tarea**: 
   - Ingresa `1` en el campo de simulación
   - Haz clic en "Completar Tareas"
   - ✅ Se desbloquea **"First Steps"** (Common) - 100 XP
   - Verás notificación con el logro desbloqueado
4. **Progreso intermedio**:
   - Simula `9` tareas más (total: 10 tareas)
   - ✅ Se desbloquea **"Task Master"** (Rare) - 500 XP
   - Tu nivel aumentará a 1 (150 XP acumulados)
5. **Logro épico**:
   - Simula `90` tareas más (total: 100 tareas)
   - ✅ Se desbloquea **"Century Club"** (Epic) - 2000 XP
   - Tu nivel será 7 (5150 XP acumulados)

### Escenario 2: Verificación de Progreso y Estadísticas 📈

1. **Después de simular tareas**: Haz clic en **"Recargar Datos"**
2. **Observa el panel de estadísticas**:
   - Tareas completadas: Actualizado en tiempo real
   - Racha actual: Incrementada
   - Nivel: Calculado automáticamente (1 + XP ÷ 1000)
   - Logros desbloqueados: Contador actualizado
3. **Verifica progreso de logros pendientes**:
   - Usa filtros para ver solo "Bloqueados"
   - Observa las barras de progreso
   - Ve cuánto falta para desbloquear cada uno
4. **Detalles de logros**:
   - Expande cualquier logro para ver detalles
   - Verifica fecha de desbloqueo de logros completados

### Escenario 3: Simulación Masiva 🚀

1. **Preparación**: Asegúrate de tener logros pendientes
2. **Simulación grande**:
   - Ingresa `100` en el campo
   - Haz clic en "Completar Tareas"
   - Observa múltiples notificaciones de logros desbloqueados
3. **Verifica impacto**:
   - Total de tareas: +100
   - XP ganado: +5000
   - Nivel: Aumentará significativamente
   - Logros desbloqueados: Varios a la vez
4. **Revisión detallada**:
   - Filtra por "Desbloqueados"
   - Revisa todos los nuevos logros
   - Compara barras de progreso

### Escenario 4: Desbloqueo Manual para Testing 🔓

1. **Selecciona un logro bloqueado**
2. **Desbloqueo directo**:
   - Haz clic en el botón "Desbloquear"
   - Confirma la acción
   - ✅ El logro se desbloquea inmediatamente
3. **Verifica estadísticas**:
   - Las estadísticas se actualizan
   - El contador de logros incrementa
   - El logro aparece en "Desbloqueados"

### Escenario 5: Seguimiento de Nivel y XP 📊

1. **Estado inicial**: Nivel 1, 0 XP
2. **Completa 20 tareas**: 1000 XP → Nivel 2
3. **Completa 40 tareas más**: 3000 XP total → Nivel 4
4. **Observa la progresión**:
   - Cada tarea = 50 XP
   - Cada 1000 XP = 1 nivel
   - El nivel se muestra junto con el XP total

## 🔧 Estructura de Archivos

```
src/
├── demo_app.py              # Aplicación Flask principal
└── templates/
    └── index.html           # Interfaz HTML con Bootstrap
```

## 📡 API Endpoints Utilizados

La demo consume estos endpoints de la API Django:

### Endpoints Principales

1. **GET /api/v1/achievements/**
   - Lista todos los logros disponibles
   - Filtra por estado (activo/inactivo)
   
2. **GET /api/v1/achievements/all-progress/?user_id=1**
   - Obtiene progreso detallado de todos los logros para un usuario
   - Incluye: progreso actual, porcentaje, estado de desbloqueo
   
3. **GET /api/v1/achievements/user-stats/?user_id=1** ⭐ NUEVO
   - Obtiene estadísticas del usuario en tiempo real
   - Retorna: tasks_completed, current_streak, longest_streak, current_level, total_xp
   
4. **POST /api/v1/achievements/simulate-tasks/** ⭐ NUEVO
   - Simula completación de múltiples tareas
   - Body: `{ "user_id": 1, "count": 10, "update_streak": true }`
   - Actualiza automáticamente estadísticas y evalúa logros
   - Retorna: estadísticas actualizadas y logros desbloqueados
   
5. **POST /api/v1/achievements/unlock/**
   - Desbloquea un logro manualmente (para testing)
   - Body: `{ "achievement_id": "uuid", "user_id": 1 }`

### Flujo de Datos

```
Frontend → Flask Backend → Django REST API
   ↓
Simulación de tareas
   ↓
Django actualiza DB (UserStatistics)
   ↓
Evalúa criterios de logros (AchievementService)
   ↓
Desbloquea logros automáticamente
   ↓
Retorna respuesta con estadísticas y logros
   ↓
Frontend actualiza UI
```

## 🎓 Logros de Ejemplo Disponibles

### Por Cantidad de Tareas:
- **First Steps** (Common) - 1 tarea → 100 XP
- **Task Master** (Rare) - 10 tareas → 500 XP
- **Century Club** (Epic) - 100 tareas → 2000 XP

### Por Rachas:
- **Week Warrior** (Rare) - 7 días → 300 XP
- **Month Master** (Epic) - 30 días → 1500 XP
- **Year Legend** (Legendary) - 365 días → 10000 XP

### Por Nivel:
- **Level 10** (Rare) - Nivel 10 → 1000 XP
- **Level 50** (Epic) - Nivel 50 → 5000 XP
- **Level 100** (Legendary) - Nivel 100 → 20000 XP

---

**Nota**: Esta es una aplicación de demostración. No requiere autenticación y utiliza el superusuario (ID=1) para todas las operaciones.
