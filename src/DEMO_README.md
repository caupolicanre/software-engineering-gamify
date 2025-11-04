# 🎮 Gamify Achievement System - Demo App

## 📋 Descripción

Aplicación Flask de demostración para el sistema de logros de Gamify. Permite visualizar y testear el flujo completo de desbloqueo de logros mediante una interfaz web simple y moderna.

## 🚀 Instrucciones de Ejecución

### Paso 1: Preparar el Backend Django

Asegúrate de que el servidor Django esté corriendo:

```bash
# En una terminal, desde el directorio src/
uv run python manage.py runserver
```

El servidor debe estar disponible en: `http://localhost:8000`

### Paso 2: Crear Datos de Prueba (si no lo has hecho)

```bash
# Crear logros de ejemplo
uv run python manage.py create_sample_achievements

# Crear estadísticas para el superusuario (ID=1)
uv run python manage.py create_test_user_stats --user-id 1
```

### Paso 3: Ejecutar la Demo Flask

En otra terminal, desde el directorio `src/`:

```bash
uv run python demo_app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 🎯 Funcionalidades de la Demo

### 1. **Panel de Estadísticas**
- Visualiza en tiempo real:
  - Tareas completadas
  - Racha actual
  - Logros desbloqueados
  - XP total acumulado

### 2. **Simulación de Tareas**
- Completa 1, 10, o 100 tareas simultáneamente
- Observa cómo se desbloquean logros automáticamente según los criterios

### 3. **Visualización de Logros**
- Ver todos los logros disponibles
- Filtrar por estado (todos, desbloqueados, bloqueados)
- Barra de progreso para cada logro
- Badges de rareza (Common, Rare, Epic, Legendary)
- Recompensas (XP y monedas)

### 4. **Desbloqueo Manual**
- Botón para desbloquear logros manualmente (para testing)
- Útil para probar el flujo sin simular tareas

### 5. **Filtros**
- **Todos**: Muestra todos los logros
- **Desbloqueados**: Solo logros completados
- **Bloqueados**: Solo logros pendientes

## 🎨 Características de la Interfaz

- ✅ **Diseño Responsive**: Funciona en desktop y móvil
- ✅ **Animaciones**: Transiciones suaves al hacer hover
- ✅ **Notificaciones Toast**: Feedback visual de todas las acciones
- ✅ **Colores por Rareza**: Identificación visual rápida
- ✅ **Progress Bars**: Seguimiento del progreso de cada logro
- ✅ **Bootstrap 5**: UI moderna y profesional

## 📊 Flujo de Demostración Recomendado

### Escenario 1: Desbloqueo por Tareas Completadas

1. Abre la demo en `http://localhost:5000`
2. Observa que no hay logros desbloqueados
3. Simula completar **1 tarea**
4. Verás que se desbloquea **"First Steps"** (Common)
5. Simula completar **10 tareas**
6. Se desbloqueará **"Task Master"** (Rare)
7. Simula completar **100 tareas**
8. Se desbloqueará **"Century Club"** (Epic)

### Escenario 2: Verificación de Progreso

1. Después de simular tareas, haz clic en **"Recargar Datos"**
2. Observa cómo se actualiza el contador de estadísticas
3. Verifica las barras de progreso de logros no desbloqueados
4. Usa los filtros para ver solo bloqueados o desbloqueados

### Escenario 3: Desbloqueo Manual (Testing)

1. Selecciona un logro bloqueado
2. Haz clic en el botón **"Desbloquear"**
3. Confirma la acción
4. El logro se desbloqueará inmediatamente
5. Las estadísticas se actualizarán

## 🔧 Estructura de Archivos

```
src/
├── demo_app.py              # Aplicación Flask principal
└── templates/
    └── index.html           # Interfaz HTML con Bootstrap
```

## 📡 API Endpoints Utilizados

La demo consume estos endpoints de la API Django:

- `GET /api/v1/achievements/` - Lista todos los logros
- `GET /api/v1/achievements/all-progress/` - Progreso de logros del usuario
- `POST /api/v1/achievements/unlock/` - Desbloquear logro manualmente

## 🐛 Troubleshooting

### La demo no carga los logros

**Problema**: Aparece mensaje "Error al cargar logros"

**Solución**:
1. Verifica que Django esté corriendo en `http://localhost:8000`
2. Prueba acceder a: `http://localhost:8000/api/v1/achievements/`
3. Si da error 403, verifica que `AllowAny` esté configurado en settings

### No se desbloquean logros al simular tareas

**Problema**: Las tareas se completan pero no se desbloquean logros

**Solución**:
1. Verifica que los comandos de Django estén implementados
2. Asegúrate de tener el superusuario creado (ID=1)
3. Ejecuta: `python manage.py create_sample_achievements`

### Error de CORS

**Problema**: Error de CORS en la consola del navegador

**Solución**:
1. Verifica `CORS_ALLOWED_ORIGINS` en `settings/base.py`
2. Añade `http://localhost:5000` si no está incluido
3. Reinicia el servidor Django

## 💡 Tips para la Demostración

1. **Abre las DevTools** (F12) para ver las peticiones a la API
2. **Usa valores pequeños** primero (1-10 tareas) para ver el flujo
3. **Recarga frecuentemente** para ver actualizaciones en tiempo real
4. **Experimenta con filtros** para mostrar diferentes vistas
5. **Prueba el desbloqueo manual** para simular el flujo completo

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
